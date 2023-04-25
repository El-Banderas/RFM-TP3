package src.WEBui;

import src.SharedInfo;

import java.util.Map;

public class RenderInfo {

    public static void renderMap(SharedInfo shared, StringBuffer outString){
        outString.append("<ul>");
        for (Map.Entry<String, String> entry : shared.redes.entrySet()) {
            //System.out.println(entry.getKey() + "/" + entry.getValue());
            outString.append("<li>"+entry.getKey()+" - " +entry.getValue()+"</li>");
        }
        outString.append(" </ul> ");
    }
}
