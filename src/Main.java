package src;

import src.WEBui.HTTP_SERVER;
import src.WEBui.Main_Server;

public class Main {
    public static void main(String[] args) throws Exception {
        SharedInfo shared = new SharedInfo();
        Main_Server webUI = new Main_Server(shared);
        webUI.main();
    }
}
