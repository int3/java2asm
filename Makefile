JAVAC := javac
PATCHES := Test.class
TRANSFORMER_JAR := transformer.jar

$(TRANSFORMER_JAR): PreMain.class ClassAdapterFactory.class MANIFEST.MF
	jar cvfm $(TRANSFORMER_JAR) MANIFEST.MF *.class

rewriter: Rewriter.class ClassAdapterFactory.class

ClassAdapterFactory.java: $(PATCHES) translator.py
	python translator.py $(PATCHES)

%.class: %.java
	$(JAVAC) -cp asm-4.1.jar:. $^

clean:
	rm -f *.class
