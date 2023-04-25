package src;

import java.util.HashMap;
import java.util.Map;

public class SharedInfo {
    public Map<String, String> redes;

    public SharedInfo() {
        this.redes = new HashMap<>();
        this.redes.put("Olá" , "Adeus");
        this.redes.put("Olá2" , "Adeus1");
        this.redes.put("Olá3" , "Adeus2");
        this.redes.put("Olá4" , "Adeus3");
    }
}
