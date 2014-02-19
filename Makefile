JAVAC := javac
PATCHES := Test.class

transformer.jar: PreMain.class ClassAdapterFactory.class MANIFEST.MF
	jar cvfm transformer.jar MANIFEST.MF *.class

rewriter: Rewriter.class ClassAdapterFactory.class

ClassAdapterFactory.java: $(PATCHES) translator.py
	python translator.py $(PATCHES) > $@

%.class: %.java
	$(JAVAC) -cp asm-4.1.jar:. $^

clean:
	rm -f *.class
