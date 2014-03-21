java2asm
========

Simple tool to make generation of [ASM][1] API calls easier.

Basically, it parses `javac`'s classfile output and creates a
`ClassFileTransformer` that appends and / or replaces method calls.

Dependencies
------------

[My fork of python-javatools.][2] Put it somewhere on your PYTHONPATH.

[asm-4.1.jar][3]. Put this in the source directory.

Limitations
-----------

No branching / exception handling opcodes have been implemented. But you can
insert method calls to external functions and do all your control flow there, so
this shouldn't be a real issue.

Example
-------

`Example.java:`

    @interface prepend {}
    @interface replace {}

    public class Example {
        
        @prepend
        public void foo() {
            System.out.println("Hello world");
        }

        @replace
        public void bar() {
            System.out.println("Hello world");
        }
    }

`javac Example.java && PATCHES=Example.class make`

[1]:http://asm.ow2.org/
[2]:https://github.com/int3/python-javatools
[3]:http://forge.ow2.org/project/download.php?group_id=23&file_id=18542
