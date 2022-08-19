import re, csv, spacy, nltk as nltk, syntok.segmenter as segmenter



nlp = spacy.load("en_core_web_md", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
#since the aim here is to find entities, the other processes incuded in the default pipeline are disabled in order to execute a much faster performance


nlp.max_length = 2000000

#If not already downloaded, it may be necessary to execute the download of the following:
#nltk.download('maxent_ne_chunker')
#nltk.download('words')




#Our regex-based word tokenizer
clean_tokenizer = nltk.RegexpTokenizer(pattern = "[a-zA-Z'’]+")

#Useful lists in order to check the nature of the names
with open('assets/non_characters_csv/nationalities.csv') as f:
    reader = csv.reader(f)
    nationalities = [row[0].lower() for row in reader]

with open('assets/non_characters_csv/countries.csv') as f:
    reader = csv.reader(f)
    countries = [row[0].lower() for row in reader]

with open('assets/non_characters_csv/UK_counties.csv') as f:
    reader = csv.reader(f)
    uk_counties = [row[0].lower() for row in reader]

with open('assets/non_characters_csv/UK_cities.csv') as f:
    reader = csv.reader(f)
    uk_cities = [row[0].lower() for row in reader]

with open('assets/non_characters_csv/religious_words.csv') as f:
    reader = csv.reader(f)
    religious_words = [row[0].lower() for row in reader]

with open('assets/non_characters_csv/common_geographical_names.csv') as f:
    reader = csv.reader(f)
    geo_names = [row[0].lower() for row in reader]

with open('assets/non_characters_csv/exclamations.csv') as f:
    reader = csv.reader(f)
    exclamations = [row[0].lower() for row in reader]




def get_characters(book):
    book = re.sub('\w+\n', '. ', book)
    book = re.sub('\n', ' ', book)
    book = re.sub('--', ' ', book)
    book = re.sub('-', ' ', book)
    book = re.sub('_', ' ', book)
    book = re.sub('- -', ' ', book)
    book = re.sub('\*', ' ', book)
    book = re.sub('\s+', ' ', book)

    nltk_characters_set = get_charaters_nltk(book)
    spacy_characters_set = get_characters_spacy(book)

    proper_nouns_dict = get_proper_nouns(book)
    proper_nouns_set = set([word for word in proper_nouns_dict if proper_nouns_dict[word].get('upper', 0) / (proper_nouns_dict[word].get('upper', 0) + proper_nouns_dict[word].get('lower', 0)) == 1 and proper_nouns_dict[word]["upper"] > 1]) #set a threshold: consider only words occuring more than once
    proper_nouns_set = check_names(proper_nouns_set)
    #The returned result is the intersection between the set obtained from our simple extraction (acting as a filter) and the union between the one coming from the extraction with NLTK and the Spacy's one
    return (nltk_characters_set | spacy_characters_set) & proper_nouns_set




#we make nltk work with its word_tokenizer while spacy works with its own. Our extraction, on the other hand, will work with the syntok segmenter and with a regexTokenizer (from NLTK) 
def get_charaters_nltk(book):
    nltk_name_set = set()
    tokenized_sentences = nltk.sent_tokenize(book)
    for sent in tokenized_sentences:
        chunked = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))) #the ne_chunk default value for "binary" attribute is "False", so it returns named entities with their own Class (PERSON, ORGANIZATION, etc.)
        for item in chunked:
            if type(item) == nltk.Tree and item.label() == "PERSON":
                nltk_name_set.add(" ".join([token for token, pos in item.leaves()]).lower()) 
    return check_names(nltk_name_set)



def get_characters_spacy(book):
    doc = nlp(book)
    spacy_name_set = set([ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"])
    return check_names(spacy_name_set)


#The following function's aim is to extract words that have an high probability of being a character's name or surname
def get_proper_nouns(book):
    proper_nouns = {}
    list_of_sentences = syntok_list_of_sentences(book)
    for sentence in list_of_sentences:
        next_words = []   
        tokenized_sent = clean_tokenizer.tokenize(sentence)
        for word in tokenized_sent:
            if len(word) > 1:
                if word[-1] == "’":
                    clean_word = word[:-1]
                elif word[-2:] == "’s":
                    clean_word = word[:-2] 
                else:
                    clean_word = word
            else:
                clean_word = word
                
            full_name = []
            if word in next_words or len(clean_word) <= 1:
                continue
            else:
                if clean_word[0].isupper() and not re.match("(I’.+)|I", clean_word): #We want to avoid including I, I'm, I'll
                    case = 'upper'
                    full_name.append(clean_word)
                    upper = True
                    idx = tokenized_sent.index(word)
                    while upper:
                        if idx < len(tokenized_sent)-1:
                            idx += 1
                        else:
                            break
                        if tokenized_sent[idx][0].isupper() and len(tokenized_sent[idx]) > 1:
                            full_name.append(tokenized_sent[idx])
                            next_words.append(tokenized_sent[idx])
                        else:
                            upper = False
                else:
                    case = 'lower'

            if full_name:
                name_lower = " ".join(full_name).lower()
                case = 'upper'
            else:
                name_lower = clean_word.lower()
                case = 'lower'

            if name_lower not in proper_nouns:
                proper_nouns[name_lower] = {}
                proper_nouns[name_lower]['upper'] = 0
                proper_nouns[name_lower]['lower'] = 0
            proper_nouns[name_lower][case]+= 1

    return proper_nouns




def syntok_list_of_sentences(book):
    list_of_sentences = []
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
            list_of_sentences.append(temp)

    return list_of_sentences




def check_names(names_set):
    characters_set = set()
    substitutions_dict = {".+['’]s$": ("['’]s", ""), ".+’":("’", ""), ".+!":("!", ""), "[Tt]he\s.+":("[Tt]he\s", ""), "[oO]\s.+": ("[Oo]\s", ""), ".+['’]s\s.+": ("['’]s\s", " "),".+\s['’]s": ("\s['’]s", ""), ".+['’,.]": ("['’,.]", ""), "[Dd]oes\s.+": ("[Dd]oes\s", "")}
    not_names_regex = ["(.+)?christmas(.+)?", ".+hall","(.+)?land", "mechlin(\s\w+)?", ".+\sislet?", ".+\sisland", ".+\slake", "lake\s.+", ".+\spark", ".+\schurch", ".+\sstation", ".+\sstreet", ".+\sriver", "river\s.+", ".+\sbrook", "(.+\s)?ocean", ".+\sbeach", ".+\sbay", "mount.+", "part\s.+", "chapter\s.+", ".+\sbridge", ".+\sdock", ".+\shead" ".+\slane", ".+\shill", ".+\srepublic", ".+\sroad", ".+\scastle", "(.+\s?)?court(\s.+)?", ".+\sfarm", ".+\slodge", ".+\scab", "(.+\s)?school", ".+\sday", "injuns?", ".+\stowers?", "first\s.+", "second\s.+", "third\s.+", "fourth\s.+", "fifth\s.+", "sixth\s.+", "seventh\s.+", "(\.+\s)?majesty", ".+\sprince(ss)?", "\w+chnic", "\.+\slaw", "\.+\swords?", "\.+\speople", "st\s\w+", "(.+\s)?gang", "(.+\s)book", "(.+\s)?crew", "(.+\s)?memorial", "(.+\s)?house", "(.+\s)?port(\s.+)?", "(.+\s)?garden", ".+\sgod", ".+\sheaven", ".+\shell", "(.+\s)?terrace", "(.+\s)?town", "dear(\s.+)", "(.+\s)?abbey"]
    not_names_words = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "christmas", "maecenas", "baby", "sir", "lord", "king", "prince", "duke", "mister", "master", "mr", "father", "uncle", "son", "brother", "lady", "queen", "princess", "duchess", "dame", "miss", "mrs", "ms", "aunt", "mother", "sister", "daughter", "mamma", "captain", "doctor", "treasure", "cap", "i", "me", "you", "yrs", "destiny", "virtue", "vicar", "englishman", "englishwoman", "quis", "editor", "project gutenberg", "where", "who", "why", "what", "how", "wont", "mystery", "fruit", "vegetables", "none", "perfessor", "professor", "teacher", "dearest", "lillibullero", "gradus", "latitude", "longitude", "north", "south", "east", "west", "latin"]

    for name in names_set:
        s_name = name.strip()
        for regex in substitutions_dict:
            if re.match(regex, s_name):
                s_name = re.sub(substitutions_dict[regex][0], substitutions_dict[regex][1], s_name) #This line makes use of a dictionary containing tuples useful for the substitutions. It is not necessary since all the items in position 1 are empty strings. However it may be possible that, in order to handle specific cases, someone wants to add a non-empty string to substitute a specific occurrence
        person_name = True
        for nnr in not_names_regex:
            if re.match(nnr, s_name):
                person_name = False
                break
        if person_name and (s_name not in countries and s_name not in nationalities and s_name not in not_names_words and s_name not in uk_cities and s_name not in uk_counties and s_name not in geo_names and s_name not in religious_words and s_name not in exclamations):
            characters_set.add(s_name.strip())
            
    return characters_set
    
