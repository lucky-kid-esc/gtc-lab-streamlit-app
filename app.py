from __future__ import annotations

import ast
import base64
import html
import io
import os
import re
import runpy
import shlex
import signal
import sys
import threading
import traceback
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = BASE_DIR.parent
IGNORE_DIRS = {".venv", "__pycache__", ".git", ".gemini", "app", "expt2 try"}
IGNORE_FILES = {"streamlit_app.py", "graph_script_template.py", "__init__.py"}
DATA_EXTENSIONS = {".txt", ".json", ".csv"}


@dataclass
class RunResult:
    command: list[str]
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool = False
    error: str | None = None
    figures: list[object] = field(default_factory=list)


@dataclass
class GraphSummary:
    label: str
    nodes: list[str]
    edges: list[tuple[str, ...]]
    directed: bool
    multigraph: bool


def iter_files(base_dir: Path, extensions: set[str]) -> list[Path]:
    files: list[Path] = []
    for root, dirs, filenames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for name in filenames:
            path = Path(root) / name
            if path.suffix.lower() not in extensions:
                continue
            files.append(path)
    return files


def find_python_scripts(base_dir: Path) -> dict[str, Path]:
    scripts = [
        path
        for path in iter_files(base_dir, {".py"})
        if path.name not in IGNORE_FILES
    ]
    scripts.sort(key=lambda p: p.relative_to(base_dir).as_posix().lower())
    return {path.relative_to(base_dir).as_posix(): path for path in scripts}


def find_data_files(base_dir: Path) -> list[Path]:
    files = iter_files(base_dir, DATA_EXTENSIONS)
    files.sort(key=lambda p: p.relative_to(base_dir).as_posix().lower())
    return files


def group_scripts(scripts: dict[str, Path]) -> tuple[dict[str, list[str]], dict[str, str]]:
    groups: dict[str, list[str]] = {}
    labels: dict[str, str] = {}
    for rel in scripts:
        parts = rel.split("/")
        if len(parts) == 1:
            group = "root"
            label = rel
        else:
            group = parts[0]
            label = "/".join(parts[1:])
        groups.setdefault(group, []).append(rel)
        labels[rel] = label
    for group in groups:
        groups[group].sort(key=lambda rel: labels[rel].lower())
    return groups, labels


def read_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        return f"# Unable to read file: {exc}"


@st.cache_data(show_spinner=False)
def load_logo_base64(path: Path) -> str | None:
    try:
        return base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return None


EXP_PATTERN = re.compile(r"exp(\d+)", re.IGNORECASE)


def get_experiment_number(rel_path: str) -> str | None:
    match = EXP_PATTERN.search(rel_path)
    return match.group(1) if match else None


@st.cache_data(show_spinner=False)
def load_theory_markdown(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def run_script(path: Path, args: list[str], stdin_text: str) -> RunResult:
    command = [sys.executable, str(path), *args]
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    result = RunResult(command=command, stdout="", stderr="", exit_code=None)

    original_cwd = os.getcwd()
    original_argv = sys.argv[:]
    original_stdin = sys.stdin
    original_path = sys.path[:]
    original_backend = os.environ.get("MPLBACKEND")
    supports_alarm = (
        hasattr(signal, "SIGALRM")
        and threading.current_thread() is threading.main_thread()
    )
    original_alarm = signal.getsignal(signal.SIGALRM) if supports_alarm else None

    def _handle_timeout(_signum: int, _frame) -> None:
        raise TimeoutError("Timed out after 60 seconds.")

    try:
        os.environ["MPLBACKEND"] = "Agg"
        if supports_alarm:
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(60)

        try:
            import matplotlib

            matplotlib.use("Agg", force=True)
            import matplotlib.pyplot as plt

            plt.close("all")
            # Prevent non-GUI backend warnings; Streamlit renders figures below.
            def _streamlit_show(*_args, **_kwargs) -> None:
                return None

            plt.show = _streamlit_show
        except Exception:
            plt = None

        os.chdir(path.parent)
        sys.argv = [str(path), *args]
        sys.stdin = io.StringIO(stdin_text or "")
        sys.path.insert(0, str(path.parent))

        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            try:
                runpy.run_path(str(path), run_name="__main__")
                result.exit_code = 0
            except SystemExit as exc:
                if exc.code is None:
                    result.exit_code = 0
                elif isinstance(exc.code, int):
                    result.exit_code = exc.code
                else:
                    result.exit_code = 1
            except TimeoutError as exc:
                result.timed_out = True
                result.error = str(exc)
            except Exception:
                result.exit_code = 1
                result.error = traceback.format_exc()
    finally:
        if supports_alarm and original_alarm is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, original_alarm)
        os.chdir(original_cwd)
        sys.argv = original_argv
        sys.stdin = original_stdin
        sys.path = original_path
        if original_backend is None:
            os.environ.pop("MPLBACKEND", None)
        else:
            os.environ["MPLBACKEND"] = original_backend

    result.stdout = stdout_buf.getvalue()
    result.stderr = stderr_buf.getvalue()

    try:
        import matplotlib.pyplot as plt

        result.figures = [plt.figure(num) for num in plt.get_fignums()]
    except Exception:
        result.figures = []

    return result


def _safe_sorted(values: list[object]) -> list[object]:
    try:
        return sorted(values)
    except TypeError:
        return sorted(values, key=lambda value: str(value))


def _format_nodes(nodes: list[object]) -> list[str]:
    return [str(node) for node in _safe_sorted(nodes)]


def _format_edges(edges: list[tuple[object, ...]]) -> list[tuple[str, ...]]:
    formatted = [tuple(str(part) for part in edge) for edge in edges]
    return sorted(formatted, key=lambda edge: str(edge))


def _format_edge_lines(edges: list[tuple[str, ...]], directed: bool) -> list[str]:
    connector = " -> " if directed else " -- "
    lines: list[str] = []
    for edge in edges:
        if len(edge) >= 2:
            line = f"{edge[0]}{connector}{edge[1]}"
            if len(edge) > 2:
                extras = ", ".join(edge[2:])
                line = f"{line} ({extras})"
        else:
            line = ", ".join(edge)
        lines.append(line)
    return lines

def extract_graph_summaries(path: Path) -> tuple[list[GraphSummary], str | None]:
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    summaries: list[GraphSummary] = []
    error: str | None = None

    original_cwd = os.getcwd()
    original_argv = sys.argv[:]
    original_stdin = sys.stdin
    original_path = sys.path[:]
    original_backend = os.environ.get("MPLBACKEND")
    supports_alarm = (
        hasattr(signal, "SIGALRM")
        and threading.current_thread() is threading.main_thread()
    )
    original_alarm = signal.getsignal(signal.SIGALRM) if supports_alarm else None

    def _handle_timeout(_signum: int, _frame) -> None:
        raise TimeoutError("Timed out after 20 seconds.")

    try:
        try:
            import networkx as nx
        except Exception as exc:
            return [], f"NetworkX unavailable ({exc})"

        registry: list[object] = []
        capture_state = {"enabled": True}

        def _run_without_capture(func):
            capture_state["enabled"] = False
            try:
                return func()
            finally:
                capture_state["enabled"] = True
        original_graph = nx.Graph
        original_digraph = nx.DiGraph
        original_multigraph = nx.MultiGraph
        original_multidigraph = nx.MultiDiGraph

        class CapturingGraph(original_graph):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if capture_state["enabled"]:
                    registry.append(self)

            def copy(self, as_view=False):
                return _run_without_capture(lambda: super().copy(as_view=as_view))

            def subgraph(self, nodes):
                return _run_without_capture(lambda: super().subgraph(nodes))

        class CapturingDiGraph(original_digraph):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if capture_state["enabled"]:
                    registry.append(self)

            def copy(self, as_view=False):
                return _run_without_capture(lambda: super().copy(as_view=as_view))

            def subgraph(self, nodes):
                return _run_without_capture(lambda: super().subgraph(nodes))

        class CapturingMultiGraph(original_multigraph):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if capture_state["enabled"]:
                    registry.append(self)

            def copy(self, as_view=False):
                return _run_without_capture(lambda: super().copy(as_view=as_view))

            def subgraph(self, nodes):
                return _run_without_capture(lambda: super().subgraph(nodes))

        class CapturingMultiDiGraph(original_multidigraph):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if capture_state["enabled"]:
                    registry.append(self)

            def copy(self, as_view=False):
                return _run_without_capture(lambda: super().copy(as_view=as_view))

            def subgraph(self, nodes):
                return _run_without_capture(lambda: super().subgraph(nodes))

        nx.Graph = CapturingGraph
        nx.DiGraph = CapturingDiGraph
        nx.MultiGraph = CapturingMultiGraph
        nx.MultiDiGraph = CapturingMultiDiGraph

        try:
            os.environ["MPLBACKEND"] = "Agg"
            if supports_alarm:
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(20)

            try:
                import matplotlib

                matplotlib.use("Agg", force=True)
                import matplotlib.pyplot as plt

                plt.close("all")

                def _streamlit_show(*_args, **_kwargs) -> None:
                    return None

                plt.show = _streamlit_show
            except Exception:
                pass

            os.chdir(path.parent)
            sys.argv = [str(path)]
            sys.stdin = io.StringIO("")
            sys.path.insert(0, str(path.parent))

            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                try:
                    runpy.run_path(str(path), run_name="__main__")
                except SystemExit:
                    pass
        except TimeoutError as exc:
            error = str(exc)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        finally:
            nx.Graph = original_graph
            nx.DiGraph = original_digraph
            nx.MultiGraph = original_multigraph
            nx.MultiDiGraph = original_multidigraph

        seen: set[tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]] = set()
        for graph in registry:
            nodes = _format_nodes(list(graph.nodes()))
            if graph.is_multigraph():
                edges_raw = list(graph.edges(keys=True))
            else:
                edges_raw = list(graph.edges())
            edges = _format_edges(edges_raw)
            signature = (tuple(nodes), tuple(edges))
            if signature in seen:
                continue
            seen.add(signature)
            label = None
            if isinstance(getattr(graph, "graph", None), dict):
                label = graph.graph.get("name")
            summaries.append(
                GraphSummary(
                    label=label or f"Graph {len(summaries) + 1}",
                    nodes=nodes,
                    edges=edges,
                    directed=graph.is_directed(),
                    multigraph=graph.is_multigraph(),
                )
            )
    finally:
        if supports_alarm and original_alarm is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, original_alarm)
        os.chdir(original_cwd)
        sys.argv = original_argv
        sys.stdin = original_stdin
        sys.path = original_path
        if original_backend is None:
            os.environ.pop("MPLBACKEND", None)
        else:
            os.environ["MPLBACKEND"] = original_backend

    return summaries, error


@st.cache_data(show_spinner=False)
def get_graph_summaries(path_str: str, modified_at: float) -> tuple[list[GraphSummary], str | None]:
    return extract_graph_summaries(Path(path_str))


def terminal_block(text: str) -> str:
    escaped = html.escape(text)
    return f"<div class='terminal'><pre>{escaped}</pre></div>"


def clean_stderr(stderr: str) -> str:
    if not stderr:
        return ""
    ignored = ("FigureCanvasAgg is non-interactive",)
    lines = [
        line
        for line in stderr.splitlines()
        if not any(token in line for token in ignored)
    ]
    return "\n".join(lines).strip()


st.set_page_config(page_title="Graph Theory Dashboard", layout="wide")

st.markdown(
    """
<style>
    :root {
        --bg: #0E1117;
        --panel: #262730;
        --panel-2: #1c1e26;
        --text: #FAFAFA;
        --muted: #9296A2;
        --accent: #FF4B4B;
        --accent-2: #FF6666;
        --border: #31333F;
        --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
    .stApp {
        background: var(--bg);
        color: var(--text);
    }
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.5rem;
    }
    div[data-testid="stSegmentedControl"] > div, 
    div[data-testid="stPills"] > div, 
    div[role="radiogroup"] {
        justify-content: center !important;
    }
    .app-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 0 0.85rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 0.75rem;
        margin-top: 0.5rem;
    }
    .app-header .header-left {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
    }
    .app-header .header-title {
        font-size: 1.15rem;
        font-weight: 600;
    }
    .app-header .header-subtitle {
        font-size: 0.9rem;
        color: var(--muted);
    }
    .app-header .header-logo {
        height: 64px;
        border-radius: 8px;
        border: 2px solid var(--border);
        object-fit: contain;
        background: #ffffff;
        padding: 4px;
    }
    section[data-testid="stSidebar"] {
        background: var(--panel);
        border-right: 1px solid var(--border);
    }
    .stButton > button {
        background: var(--accent);
        color: #ffffff;
        border: 1px solid var(--accent);
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: var(--accent-2);
        border-color: var(--accent-2);
        color: #ffffff;
    }
    .terminal {
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 14px;
        font-family: var(--mono);
        font-size: 0.92rem;
        color: var(--text);
        white-space: pre-wrap;
        max-height: 420px;
        overflow: auto;
    }
    code, pre, textarea {
        font-family: var(--mono) !important;
    }
    .muted {
        color: var(--muted);
    }
    .app-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        border-top: 1px solid var(--border);
        background: var(--panel-2);
        position: sticky;
        bottom: 0;
        padding: 0.75rem 0;
        margin-top: 1.5rem;
        z-index: 50;
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)

scripts = find_python_scripts(WORKSPACE_DIR)
if not scripts:
    st.warning("No Python scripts found in this folder.")
    st.stop()

if "selected_script" not in st.session_state:
    st.session_state.selected_script = list(scripts.keys())[0]

# Render Header First
logo_data = load_logo_base64(BASE_DIR / "logo.png")
logo_html = (
    f"<img class='header-logo' src='data:image/png;base64,{logo_data}' alt='logo' />"
    if logo_data
    else ""
)
selected_label = html.escape(st.session_state.selected_script)
st.markdown(
    "<div class='app-header'>"
    f"{logo_html}"
    "<div class='header-left'>"
    "<div class='header-title'>CMP-226 Graph Theory and Combinatorics Lab</div>"
    f"<div class='header-subtitle'>Selected: {selected_label}</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# Render File Explorer
groups, labels = group_scripts(scripts)
valid_groups = [g for g in sorted(groups.keys()) if not (g == "root" and len(groups[g]) == 0)]

current_rel = st.session_state.selected_script
current_group = current_rel.split("/")[0] if "/" in current_rel else "root"
if current_group not in valid_groups:
    current_group = valid_groups[0]

st.markdown("<div style='text-align: center; margin-bottom: 0.5rem;'><b>File Explorer</b></div>", unsafe_allow_html=True)
if hasattr(st, "pills"):
    selected_group = st.pills("Select Folder", options=valid_groups, default=current_group, label_visibility="collapsed")
    if not selected_group:
        selected_group = current_group
else:
    selected_group = st.radio("Select Folder", options=valid_groups, index=valid_groups.index(current_group), horizontal=True, label_visibility="collapsed")

if selected_group != current_group:
    st.session_state.selected_script = groups[selected_group][0]
    st.rerun()

files_in_group = groups[selected_group]
file_labels = [labels[f] for f in files_in_group]
current_rel = st.session_state.selected_script
current_file_label = labels[current_rel] if current_rel in labels else file_labels[0]

if hasattr(st, "pills"):
    selected_file_label = st.pills("Select File", options=file_labels, default=current_file_label, label_visibility="collapsed")
    if not selected_file_label:
        selected_file_label = current_file_label
else:
    selected_file_label = st.radio("Select File", options=file_labels, index=file_labels.index(current_file_label), horizontal=True, label_visibility="collapsed")

new_script = files_in_group[file_labels.index(selected_file_label)]
if st.session_state.selected_script != new_script:
    st.session_state.selected_script = new_script
    st.rerun()

selected_path = scripts[st.session_state.selected_script]
exp_number = get_experiment_number(st.session_state.selected_script)
theory_path = BASE_DIR / "theory" / f"exp{exp_number}.md" if exp_number else None
theory_markdown = load_theory_markdown(theory_path) if theory_path else None
st.divider()

data_files = find_data_files(WORKSPACE_DIR)
data_labels = ["(none)"] + [
    path.relative_to(WORKSPACE_DIR).as_posix() for path in data_files
]

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    tab1, tab2 = st.tabs(["Theory", "Source Code"])
    
    with tab1:
        if theory_markdown:
            st.markdown(theory_markdown)
        else:
            missing_label = f"exp{exp_number}.md" if exp_number else "expX.md"
            st.info(f"No theory file found for this experiment ({missing_label}).")
            
    with tab2:
        st.code(read_source(selected_path), language="python")

if "last_result" not in st.session_state:
    st.session_state.last_result = None

with right_col:
    st.markdown("### Execution")
    with st.expander("Optional input", expanded=False):
        dataset_choice = st.selectbox("Dataset file", options=data_labels)
        cli_args = st.text_input("CLI arguments", placeholder="e.g. --nodes 6 --weighted")
        stdin_text = st.text_area(
            "STDIN (for input())",
            height=140,
            placeholder="Paste input text if the script expects input().",
        )
        st.markdown(
            "<div class='muted'>Dataset selection appends the file path as the last argument.</div>",
            unsafe_allow_html=True,
        )
    run_clicked = st.button("Run Algorithm", type="primary", use_container_width=True)

    if run_clicked:
        args = shlex.split(cli_args) if cli_args else []
        if dataset_choice != "(none)":
            args.append(str(WORKSPACE_DIR / dataset_choice))
        st.session_state.last_result = run_script(selected_path, args, stdin_text)

    result: RunResult | None = st.session_state.last_result
    if result:
        st.markdown(f"**Command:** `{shlex.join(result.command)}`")
        if result.timed_out:
            st.error(result.error or "Process timed out.")
        elif result.exit_code not in (0, None):
            st.error(f"Exit code: {result.exit_code}")
        else:
            st.success("Completed successfully.")

        if result.error and not result.timed_out:
            st.code(result.error, language="text")

        combined = result.stdout.strip()
        cleaned_stderr = clean_stderr(result.stderr)
        if cleaned_stderr:
            combined = f"{combined}\n\n[stderr]\n{cleaned_stderr}".strip()
        if not combined:
            combined = "No output captured."
        st.markdown(terminal_block(combined), unsafe_allow_html=True)

        if result.figures:
            st.markdown("### Visualization")
            for fig in result.figures:
                st.pyplot(fig, use_container_width=True)

st.markdown(
    "<div class='app-footer'><div>Manjunath Gavada</div><div>24B-CO-035</div><div>Sem IV</div></div>",
    unsafe_allow_html=True,
)
