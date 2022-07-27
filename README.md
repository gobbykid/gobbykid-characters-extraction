# The GOBBY KID project's text analysis functions
This repository hosts the functions and the runnable code that we've created in order to perform our analyses on the project's corpus.
The directory *characters_recognition* contains:
- The directory containing the corpus.
- A directory with 2 csv files useful to avoid including nationalities or country names among the characters' ones.
- A Python Notebook hosting the code that perform the analysis taking in consideration the results obtained from the same process performed by using both <a href="https://www.nltk.org/" target="blank">NLTK</a> and <a href="https://spacy.io/" target="blank">Spacy</a> and making use of thresholds and arbitrary weights.
- A Python file containing the functions that perform the same analysis as before, but adding a custumed NER pipeline that allowed us to filter the results without adding thresholds or arbitrary weights to the words of interest.
- A Python file hosting the functions that have been used to filter out the surnames from the single-word-based names and to guess the gender of the characters by means of the <a href="https://github.com/SteelPangolin/genderize" target="blank">Gederize</a> library.
