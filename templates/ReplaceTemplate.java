class Method<%name%>Adapter extends MethodVisitor {
    String methodSignature;

    public Method<%name%>Adapter(MethodVisitor mv) {
        super(Opcodes.ASM4, mv);
    }

    @Override
    public void visitCode() {
        <%code%>
        mv.visitCode();
    }
}
