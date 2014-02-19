import string
import javatools
import javatools.opcodes as opcodes
from javatools.pack import unpack
import re

def template_name(name):
    import os
    return 'templates' + os.sep + name + 'Template.java'

def escaped_name(name):
    def f(matchobj):
        s = matchobj.group(0)
        hm = {
            '/': '__slash__',
            '(': '__lparen__',
            ')': '__rparen__',
            ';': '__semicolon__',
        }
        return hm[s]
    return re.sub("[/();]", f, name)

def fill_template(template, **kwargs):
    def f(match_name, indent=''):
        return indent + ("\n" + indent).join(str(kwargs[match_name]).split('\n'))
    return re.sub("<%(\w+)%>", lambda m: f(m.group(1)),
           re.sub("(.*)<%(\w+)%>", lambda m: f(m.group(2), m.group(1)), template, flags=re.MULTILINE))

class Method(object):
    def __init__(self, method_info, action_type):
        self.action_type = action_type
        self.info = method_info
        self.code = []

    def escaped_name(self):
        return escaped_name(self.info.get_name()) + '_' + \
                escaped_name(self.info.get_descriptor())

    def java_code(self):
        with open(template_name(self.action_type.capitalize())) as f:
            template = f.read()
        code = '\n'.join('mv.' + line + ';' for line in self.code)
        return fill_template(template, name=self.escaped_name(), code=code)

class Translator(object):

    def __init__(self):
        self.class_codes = {}

    def java_code(self):
        with open(template_name('Factory')) as f:
            template = f.read()
        code = ''
        for name in self.class_codes.keys():
            code += fill_template(
                    'if (name.equals("<%name%>")) return new Class<%escaped_name%>Adapter(api, cv);',
                    name=name, escaped_name=escaped_name(name))
        return fill_template(template, code=code) + '\n'.join(self.class_codes.values())

    def handle_class(self, klass):
        results = []
        for m in klass.methods:
            result = self.handle_method(m)
            if result is not None:
                results.append(result)

        with open(template_name('Class')) as f:
            template = f.read()

        code = ""
        for m in results:
            code += fill_template("""
if (name.equals("<%name%>") && desc.equals("<%desc%>")) {
    if (access != <%access%>) throw new AssertionError("access flag mismatch: Expected " + <%access%> + " but got " + access);
    return new Method<%escaped_name%>Adapter(mv);
}\n""", name=m.info.get_name(), desc=m.info.get_descriptor(),
        access=m.info.access_flags,
        escaped_name=m.escaped_name())
        code += "return mv;"
        class_name = klass.get_this()
        self.class_codes[class_name] = \
            fill_template(template, name=escaped_name(class_name), code=code,
                    method_code="\n".join(m.java_code() for m in results))

    def handle_method(self, method):
        code = method.get_code()
        if code is None:
            return

        m = None
        for ann in method.get_invisible_annotations():
            t = ann.pretty_type().split('.')[-1]
            if t in ['replace', 'prepend']:
                m = Method(method, t)
                break
        else:
            return

        cpool = code.cpool
        for offset, opcode, args in code.disassemble():
            name = opcodes.get_opname_by_code(opcode).upper()
            if m.action_type != 'replace' and 'RETURN' in name:
                continue
            if name in ['NOP', 'ACONST_NULL', 'ICONST_M1', 'ICONST_0',
                    'ICONST_1', 'ICONST_2', 'ICONST_3', 'ICONST_4', 'ICONST_5',
                    'LCONST_0', 'LCONST_1', 'FCONST_0', 'FCONST_1', 'FCONST_2',
                    'DCONST_0', 'DCONST_1', 'IALOAD', 'LALOAD', 'FALOAD',
                    'DALOAD', 'AALOAD', 'BALOAD', 'CALOAD', 'SALOAD', 'IASTORE',
                    'LASTORE', 'FASTORE', 'DASTORE', 'AASTORE', 'BASTORE',
                    'CASTORE', 'SASTORE', 'POP', 'POP2', 'DUP', 'DUP_X1',
                    'DUP_X2', 'DUP2', 'DUP2_X1', 'DUP2_X2', 'SWAP', 'IADD',
                    'LADD', 'FADD', 'DADD', 'ISUB', 'LSUB', 'FSUB', 'DSUB',
                    'IMUL', 'LMUL', 'FMUL', 'DMUL', 'IDIV', 'LDIV', 'FDIV',
                    'DDIV', 'IREM', 'LREM', 'FREM', 'DREM', 'INEG', 'LNEG',
                    'FNEG', 'DNEG', 'ISHL', 'LSHL', 'ISHR', 'LSHR', 'IUSHR',
                    'LUSHR', 'IAND', 'LAND', 'IOR', 'LOR', 'IXOR', 'LXOR',
                    'I2L', 'I2F', 'I2D', 'L2I', 'L2F', 'L2D', 'F2I', 'F2L',
                    'F2D', 'D2I', 'D2L', 'D2F', 'I2B', 'I2C', 'I2S', 'LCMP',
                    'FCMPL', 'FCMPG', 'DCMPL', 'DCMPG', 'IRETURN', 'LRETURN',
                    'FRETURN', 'DRETURN', 'ARETURN', 'RETURN', 'ARRAYLENGTH',
                    'ATHROW', 'MONITORENTER', 'MONITOREXIT']:
                m.code.append('visitInsn(Opcodes.%s)' % name)
            elif name in ['BIPUSH', 'SIPUSH']:
                m.code.append('visitIntInsn(Opcodes.%s, %d)' % args[0])
            elif 'LDC' in name:
                t, v = cpool.get_const(args[0])
                const = cpool.deref_const(args[0])
                if t == javatools.CONST_String:
                    m.code.append('visitLdcInsn("%s")' % const)
                elif t == javatools.CONST_Long:
                    m.code.append('visitLdcInsn(%sL)' % const)
                elif t == javatools.CONST_Double:
                    m.code.append('visitLdcInsn(%sd)' % const)
                else: # TODO
                    m.code.append('visitLdcInsn(%s)' % const)
            elif name[1:-2] in ['LOAD', 'STORE']:
                m.code.append('visitVarInsn(Opcodes.%s, %s)' % (name[:-2], name[-1]))
            elif name in ['GETFIELD', 'PUTFIELD', 'GETSTATIC', 'PUTSTATIC']:
                field = cpool.deref_const(args[0])
                m.code.append('visitFieldInsn(Opcodes.%s, "%s", "%s", "%s")' % (name,
                    field[0], field[1][0], field[1][1]))
            elif 'INVOKE' in name:
                target = cpool.deref_const(args[0])
                m.code.append('visitMethodInsn(Opcodes.%s, "%s", "%s", "%s")' % (name,
                    target[0], target[1][0], target[1][1]))
            elif name in ['NEW', 'ANEWARRAY', 'CHECKCAST', 'INSTANCEOF']:
                t = cpool.deref_const(args[0])
                m.code.append('visitTypeInsn(Opcodes.%s, "%s")' % (name, t))
            else:
                raise Exception('unhandled opcode ' + name)

        return m

if __name__ == '__main__':
    import sys
    translator = Translator()
    for arg in sys.argv:
        jci = javatools.unpack_class(open(sys.argv[1]))
        translator.handle_class(jci)
    print translator.java_code()
