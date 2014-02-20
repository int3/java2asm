import java.lang.instrument.*;
import java.security.*;

class PreMain {
    public static void premain(String args, Instrumentation inst) {
        inst.addTransformer(new Transformer());
    }
}
