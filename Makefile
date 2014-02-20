JAVAC := javac
PATCHES := Test.class
TRANSFORMER_JAR := transformer.jar

$(TRANSFORMER_JAR): Transformer.class ClassAdapterFactory.class MANIFEST.MF
	jar cvf $(TRANSFORMER_JAR) *.class

rewriter: Rewriter.class ClassAdapterFactory.class

ClassAdapterFactory.java: $(PATCHES) translator.py
	python translator.py $(PATCHES)

Transformer.class: ClassAdapterFactory.java

%.class: %.java
	$(JAVAC) -encoding "UTF-8" -cp asm-4.1.jar:. $^

clean:
	rm -f *.class
	rm -f ClassAdapterFactory.java
