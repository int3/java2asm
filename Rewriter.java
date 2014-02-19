import org.objectweb.asm.*;
import java.io.*;

public class Rewriter {

    public static void main(String[] args) throws Exception {
        ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        ClassVisitor adapter = ClassAdapterFactory.getClassAdapter(args[0], Opcodes.ASM4, writer);
        if (adapter == null) {
            throw new RuntimeException("adapter not found for class " + args[0]);
        }
        File f = new File(args[0] + ".class");
        ClassReader reader = new ClassReader(new FileInputStream(f));
        reader.accept(adapter, 0);
        (new FileOutputStream(f)).write(writer.toByteArray());
    }

}
