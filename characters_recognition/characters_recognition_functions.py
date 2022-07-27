import syntok.segmenter as segmenter
import re
import csv
import nltk as nltk
nltk.download('maxent_ne_chunker')
nltk.download('words')
import spacy
nlp = spacy.load("en_core_web_md")
nlp.max_length = 2000000

#Our regex-based word tokenizer
clean_tokenizer = nltk.RegexpTokenizer(pattern = "[a-zA-Z'’]+")


#Useful lists in order to check the nature of the names
with open('characters_recognition/not_characters_names/nationalities.csv') as f:
    reader = csv.reader(f)
    nationalities = [row[0].lower() for row in reader]

with open('characters_recognition/not_characters_names/countries.csv') as f:
    reader = csv.reader(f)
    countries = [row[0].lower() for row in reader]




def get_characters(book):
    book = re.sub('\n', ' ', book)
    book = re.sub('--', ' ', book)
    book = re.sub('-', ' ', book)
    book = re.sub('_', ' ', book)
    book = re.sub('- -', ' ', book)
    book = re.sub('\*', ' ', book)
    book = re.sub('\s+', ' ', book)

    nltk_name_set = get_charaters_nltk(book)
    spacy_name_set = get_characters_spacy(book)

    proper_nouns_dict = is_it_proper(book)
    proper_names_set = set([word for word in proper_nouns_dict if proper_nouns_dict[word].get('upper', 0) / (proper_nouns_dict[word].get('upper', 0) + proper_nouns_dict[word].get('lower', 0)) == 1]) #it is possible to set a thrashold to take in consideration only the words that appear more than n-times by adding this before the last "]": and proper_nouns_dict[word]["upper"]>1
    proper_names_set = check_names(proper_names_set)


    return (nltk_name_set | spacy_name_set) & proper_names_set



#we make nltk work with its word_tokenizer while spacy works with its own. Our proper name search, however, will work with syntok and with a regexTokenizer 
def get_charaters_nltk(book):
    nltk_name_set = set()
    tokenized_sentences = nltk.sent_tokenize(book)
    for sent in tokenized_sentences:
        chunked = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))
        for item in chunked:
            if type(item) == nltk.Tree and item.label() == "PERSON":
                nltk_name_set.add(" ".join([token for token, pos in item.leaves()]).lower()) 
    return check_names(nltk_name_set)




def get_characters_spacy(book):
    doc = nlp(book)
    spacy_name_set = set([ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"])
    return check_names(spacy_name_set)




def is_it_proper(book):
    proper_nouns = {}
    list_of_sentences = syntok_list_of_sentences(book)
    for sentence in list_of_sentences:
        next = []   
        tok_sent = clean_tokenizer.tokenize(sentence)
        for word in tok_sent:  #We don't consider the first word so to be sure to not include words that appear only once at the first position
            if len(word) > 1:
                if word[-1] == "’":
                    clean_word = word[:-1]
                    """ elif word[-2:] == "’s":
                    clean_word = word[:-2] """
                else:
                    clean_word = word
            else:
                clean_word = word
                
            current = []
            if word in next or len(clean_word)<=1:
                continue
            else:
                if clean_word[0].isupper() and not(clean_word[0] == "I" and re.match("['’]", clean_word[1])):
                    case = 'upper'
                    current.append(clean_word)
                    upper = True
                    idx = int(tok_sent.index(word))
                     
                    while upper:
                        if idx < len(tok_sent)-1:
                            idx += 1
                        else:
                            break
                        if tok_sent[idx][0].isupper() and len(tok_sent[idx])>1:
                            current.append(tok_sent[idx])
                            next.append(tok_sent[idx])
                        else:
                            upper = False
                else:
                    case = 'lower'

            if current:
                word_lower = " ".join(current).lower()
                case = 'upper'
            else:
                word_lower = clean_word.lower()
                case = 'lower'

            if word_lower not in proper_nouns:
                proper_nouns[word_lower] = {}
                proper_nouns[word_lower]['upper'] = 0
                proper_nouns[word_lower]['lower'] = 0
            
            proper_nouns[word_lower][case]+= 1

    return proper_nouns






def syntok_list_of_sentences(book):
    res = []
    for paragraph in segmenter.process(book):
        for sent in paragraph:
            temp = []
            token_list = []
            for token in sent:
                token_list.append(token.spacing)
                token_list.append(token.value)
            if token_list[0] == ' ':
                token_list.remove(token_list[0])
            temp = ''.join(token_list)
            res.append(temp)
    return res




def check_names(names_set):
    regex_dict = {".+’":("’", ""), ".+!":("!", ""), "[Tt]he\s.+":("[Tt]he\s", ""), "[oO]\s.+": ("[Oo]\s", ""), ".+['’]s": ("['’]s", ""), ".+\s['’]s": ("\s['’]s", ""), "[Pp]rince\s.+": ("[Pp]rince\s", ""), "[Pp]rincess\s.+": ("[Pp]rincess\s", ""), "[Kk]ing\s.+": ("[Kk]ing\s", ""), "[Qq]ueen\s.+": ("[Qq]ueen\s", ""), "[Dd]ame\s.+": ("[Dd]ame\s", ""), "[Ll]ady\s.+": ("[Ll]ady\s", ""), ".+['’,.]": ("['’,.]", "")}
    characters_set = set()
    #"England" etc. "Englishman" "Englishwoman"
    not_names_regex = [".+\schristmas", ".+\sisland", ".+\slake", "lake\s.+", ".+\spark", ".+\schurch", ".+\sstation", ".+\sstreet", ".+\sriver", "river\s.+", ".+\socean", "mount.+", "part\s.+", "chapter\s.+", ".+\sbridge", ".+\slane", ".+\shill", ".+\srepublic", ".+\sroad", ".+\scab", ".+\sschool", ".+\sday", "injuns?"]
    not_names_words = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "christmas", "maecenas", "baby", "sir", "lord", "king", "prince",  "mister", "mr", "father", "uncle", "son", "brother", "lady", "queen", "princess", "dame", "miss", "mrs", "ms", "aunt", "mother", "sister", "daughter", "mamma", "captain", "cap", "i", "me", "you", "destiny", "virtue", "vicar", "englishman", "englishwoman", "quis", "god", "oh", "editor", "project gutenberg"]

    for name in names_set:
        s_name = name.strip()
        for regex in regex_dict:
            if re.match(regex, s_name):
                s_name = re.sub(regex_dict[regex][0], regex_dict[regex][1], s_name)
        person_name = True
        for nnr in not_names_regex:
            if re.match(nnr, s_name):
                person_name = False
                break
        if person_name and (s_name not in countries and s_name not in nationalities and s_name not in not_names_words):
            characters_set.add(s_name.strip())
            
    return characters_set




#PROBLEMI:
#cercare di escludere i soli cognomi
#prima di escludere i cognomi, ricondurre ad essi le parole che indicano la famiglia: es. Mario Bartaldo; the Bartaldos