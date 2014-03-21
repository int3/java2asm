JAVAC := javac
PATCHES := Test.class
TRANSFORMER_JAR := transformer.jar

$(TRANSFORMER_JAR): build/transformer/Transformer.class build/transformer/ClassAdapterFactory.class MANIFEST.MF
	jar cvf $(TRANSFORMER_JAR) -C build .

rewriter: build/transformer/Rewriter.class build/transformer/ClassAdapterFactory.class

ClassAdapterFactory.java: $(PATCHES) translator.py
	python translator.py $(PATCHES)

build/transformer/Transformer.class: ClassAdapterFactory.java

build/transformer/%.class: %.java
	$(JAVAC) -encoding "UTF-8" -cp asm-4.1.jar:. $^ -d build

clean:
	rm -f *.class
	rm -f ClassAdapterFactory.java
