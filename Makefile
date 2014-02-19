transformer.jar: PreMain.class ClassAdapterFactory.class MANIFEST.MF
	jar cvfm transformer.jar MANIFEST.MF *.class

rewriter: Rewriter.class ClassAdapterFactory.class

ClassAdapterFactory.java: Test.class translator.py
	python translator.py Test.class > $@

%.class: %.java
	javac -cp asm-4.1.jar:. $^

clean:
	rm -f *.class
