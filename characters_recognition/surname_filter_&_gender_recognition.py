from genderize import Genderize
import re

from numpy import full, single

names = {'babel', 'osrawalddo', 'rosenbaum', 'naval heroes', 'bon', 'ali baba', 'hastings', 'lord tottenham', 'gaboriau', 'trafalgar', 'pincher', 'etait', 'bravo', 'claude duval', 'foulkes', 'stroud', 'aunt emily', 'alice the princess', 'bagheera', 'annie', 'oswald', 'holloway', 'father time', 'noel', 'nelson', 'victoria', 'quentin durward', 'steal', 'hildegarde', 'katinka', 'miss dora', 'mrs leslie', 'hildegarde cunigonde', 'janey', 'lookee', 'bastable', 'alice', 'take noel', 'edward', 'lewisham', 'daisy', 'gabrielle', 'count folko', 'flings', 'balliol', 'pauline', 'dora', 'alicia', 'guy fawkes', 'ellis', 'annie ridgway', 'mary', 'dick diddlington', 'castilian amoroso', 'malabar', 'jane', 'little alice', 'albert', 'fame', 'gordon', 'denny', 'eliza', 'bastables', 'amoroso', 'albert morrison', 'dicky', 'sam redfern', 'jim carlton', 'carlton', 'wilson', 'redfern', 'blackheath', 'noel bastable', 'noeloninuris', 'hardy', 'oswald bastable', 'dickens', 'young lady missing', 'dick turpin', 'indian uncle', 'dick', 'horace octavius', 'kipling', 'sintram'}

my_names = {"Giovanni", "Gianni", "Gianni Lontri", "Joe", "Mr Joe", "Maria Mucci", "Marta Brodagli", "Mucci", "Giorgio Mucci", "Alberto Grandini", "Mario Grandini", "Grandinis", "Gian Lorenzo Brodagli"}





def filter_surnames(names_set):
    single_names = []
    multiple_names = []

    for name in names_set:
        if re.match("\w+(\s\w+)+", name):
            multiple_names.append((name.split(" ")))
        else:
            single_names.append(name)
    
    for name in single_names:   
        remove = False
        for mult_n in multiple_names:
            if name[-1] == "s":
                if mult_n[-1] == name[:-1]:
                    remove = True
            else:
                if mult_n[-1] == name:
                    remove = True
        if remove:
            single_names.remove(name)
          
    return gender_recognition(single_names, multiple_names)


def gender_recognition(single_names, multiple_names):
    male_words = {"sir", "lord", "king", "prince",  "mister", "mr", "father", "uncle", "son", "brother"}
    female_words = {"lady", "queen", "princess", "dame", "miss", "mrs", "ms", "aunt", "mother", "sister", "daughter"}
    male_characters = []
    female_characters = []
    unknown_gender = []
    sn_char_gender = Genderize().get(single_names)


    for char in sn_char_gender:
        if char["gender"] == "male":
            male_characters.append(char["name"])
        elif char["gender"] == "female":
            female_characters.append(char["name"])
        else:
            unknown_gender.append(char["name"])


##################################
    for full_name in multiple_names:
        if len(set(full_name) & male_words) > 0:
            male_characters.append(" ".join(full_name))
        elif len(set(full_name) & female_words) > 0:
            female_characters.append(" ".join(full_name))
        else:
            already_added = False
            for name in full_name:
                if already_added:
                    continue
                name_gender = Genderize().get(name)
                if name_gender["gender"] == "male":
                    male_characters.append(" ".join(full_name))
                    already_added = True
                elif name_gender["gender"] == "female":
                    female_characters.append(" ".join(full_name))
                    already_added = True
                else:
                    if full_name.index(name) == len(full_name) -1:
                        unknown_gender.append(" ".join(full_name))
                    else:
                        continue # SE ALL'ULTIMA ITERAZIONE è TUTTO UNKNOWN CHE SUCCEDE???????
##################################

    return unknown_gender




#print(filter_surnames(names))


print(Genderize().get(["mary"]))






