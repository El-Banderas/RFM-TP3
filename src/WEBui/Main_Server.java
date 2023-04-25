package src.WEBui;

import src.SharedInfo;

import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class Main_Server {
    SharedInfo shared;
    public Main_Server(SharedInfo shared) {
        this.shared = shared;
    }

    public void main () throws IOException {
        ServerSocket Server = new ServerSocket (5000, 10, InetAddress.getByName("127.0.0.1"));
        System.out.println ("TCPServer Waiting for client on port 5000");

        while(true) {
            Socket connected = Server.accept();
            (new HTTP_SERVER(connected, shared)).start();
        }
    }
}
