import java.io.*;
import java.util.*;

public class ArrayListTest {
    public static void main(String[] args) throws IOException{
        DataInputStream dis=new DataInputStream(System.in);
        FileOutputStream fo=new FileOutputStream("txt.txt");
        System.out.println("enetr @ if end:");
        char ch;
        while((ch=(char)dis.read())!='@'){
            fo.write(ch);

              
        }
        fo.close();
       
    }
}