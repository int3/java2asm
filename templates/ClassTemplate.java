class Class<%name%>Adapter extends ClassVisitor {

    public Class<%name%>Adapter(int api, ClassVisitor cv) {
        super(api, cv);
    }

    public void visit(int version, int access, String name, String signature,
            String superName, String[] interfaces) {
        cv.visit(version, access, name, signature, superName, interfaces);
    }

    @Override
    public MethodVisitor visitMethod(int access, String name,
            String desc, String signature, String[] exceptions) {

        MethodVisitor mv = cv.visitMethod(access, name, desc, signature, exceptions);
        <%code%>
    }

    <%method_code%>
}
