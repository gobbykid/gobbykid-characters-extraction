# The GOBBY KID project's text analysis functions
This repository hosts the functions and the runnable code that we've created in order to perform our analyses on the project's corpus.

## Organization and functioning
The *assets* directory:
- *Corpus*: it contains two sub-directories (one for male authors and one for female authors) with the corpus we have analyzed.
- *non_characters_csv*: contains 2 csv files hosting the nationalities and countries' names we have used to manage ambiguous situations dealing with the characters' names extraction.
The *characters_extraction_and_gender_recognition* directory:
- *run.py*: just a Python file to run to get back the desired results.
- *charEx.py*: a Python file containing the functions that perform the Name Entity Recognition on the texts so to extract the names of the books' characters. The extraction has been done by means of two libraries: <a href="https://www.nltk.org/" target="blank">NLTK</a> and <a href="https://spacy.io/" target="blank">Spacy</a>. In particular, dealing with non-contemporary texts created a lot of problems when only one library was used to perform the analysis. Therefore, three different analyses have been carried out, two of which are fully based on those two libraries. The results have been strored in two different sets, whose union was filtered by means of an intersection with the extraction function we have developed using the ```nltk.regexpTokenizer```.
- *genderRec.py*: a Python file hosting the functions that have been used to exclude the surnames from the list of names composed by a single word and to guess the gender of the characters by means of both <a href="https://github.com/tue-mdse/genderComputer.git" target="blank">genderComputer</a> and <a href="https://github.com/SteelPangolin/genderize" target="blank">Gederize</a> libraries.
