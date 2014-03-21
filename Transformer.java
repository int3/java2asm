package transformer;

import java.lang.instrument.*;
import java.security.*;
import org.objectweb.asm.*;

public class Transformer implements ClassFileTransformer {

    public byte[] transform(ClassLoader loader, String className, Class<?> clazz,
                            ProtectionDomain pd, byte[] buffer) {
        ClassWriter writer = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        ClassVisitor adapter = ClassAdapterFactory.getClassAdapter(className, Opcodes.ASM4, writer);
        if (adapter == null) return buffer;
        ClassReader reader = new ClassReader(buffer);
        reader.accept(adapter, 0);
        return writer.toByteArray();
    }

}
