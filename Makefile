JAVAC := javac
PATCHES := Test.class
TRANSFORMER_JAR := transformer.jar
AUX_FILE_DIR :=
AUX_FILES :=
PREMAIN_DIR := .

$(TRANSFORMER_JAR): $(PREMAIN) Transformer.class ClassAdapterFactory.class MANIFEST.MF
	jar cvfm $(TRANSFORMER_JAR) MANIFEST.MF *.class $(if $(AUX_FILE_DIR),$(foreach f,$(AUX_FILES),-C $(AUX_FILE_DIR) $(f)),) -C $(PREMAIN_DIR) PreMain.class

rewriter: Rewriter.class ClassAdapterFactory.class

ClassAdapterFactory.java: $(PATCHES) translator.py
	python translator.py $(PATCHES)

%.class: %.java ClassAdapterFactory.java
	$(JAVAC) -encoding "UTF-8" -cp asm-4.1.jar:. $^

clean:
	rm -f *.class
	rm -f ClassAdapterFactory.java
