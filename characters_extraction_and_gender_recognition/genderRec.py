from genderize import Genderize
from genderComputer import GenderComputer
import re


def filter_surnames(names_set):
    single_word_names = []
    multiple_words_names = []
    for name in names_set:
        if re.match("\w+(\s\w+)+", name):
            multiple_words_names.append((name.split(" ")))
        else:
            single_word_names.append(name)
    
    for name in single_word_names:   
        remove = False
        for mwn in multiple_words_names:
            if name[-1] == "s":             #Here the family names are removed: e.g. If we find "John Doe", "Lisa Doe", "Does" and "Doe", we remove "Does" and "Doe"
                if mwn[-1] == name[:-1]:
                    remove = True
            else:
                if mwn[-1] == name:
                    remove = True
        if remove:
            single_word_names.remove(name)

    return single_word_names, multiple_words_names






def gender_recognition(names_set):
    gc = GenderComputer()
    single_word_names, multiple_words_names = filter_surnames(names_set)
    male_words = {"sir", "lord", "king", "prince",  "mister", "mr", "father", "uncle", "son", "brother"}
    female_words = {"lady", "queen", "princess", "dame", "miss", "mrs", "ms", "aunt", "mother", "sister", "daughter"}
    male_characters = []
    female_characters = []
    unknown_gender = []

    for name in single_word_names:                   #First check by means of genderComputer on the list of names composed by a single word
        gender = gc.resolveGender(name, None)
        if gender == "male":
            male_characters.append(name)
        elif gender == "female":
            female_characters.append(name)
        else:
            try:                                      #If genderComputer is not able to guess the gender, Genderize is used
                char_info = Genderize().get([name])
                if char_info[0]["gender"] == "male":
                    male_characters.append(name)
                elif char_info[0]["gender"] == "female":
                    female_characters.append(name)
                else:
                    unknown_gender.append(name)
            except:
                unknown_gender.append(name)

    
    for full_name in multiple_words_names:                        #The first block of checks aims at guessing the gender on the basis of genderdized words present in the strings without using any additional library
        joined_name = " ".join(full_name)
        if len(set(full_name) & male_words) > 0:                #By checking the presence of genderdized words in the name we can directly append the name in the right list
            male_characters.append(joined_name)
        elif len(set(full_name) & female_words) > 0:
            female_characters.append(joined_name)
        else:                                                       #Now, it is used the same process as before: first we check the gender by meand of genderComputer
            gender = gc.resolveGender(joined_name, None)
            if gender == "male":
                male_characters.append(joined_name)
            elif gender == "female":
                female_characters.append(joined_name)
            else:                                       #In the following block the detection is based on each word composing the names
                already_added = False
                for single_name in full_name:
                    if already_added:
                        break
                    else:
                        if single_name in male_characters:
                            male_characters.append(joined_name)
                            already_added = True
                        elif single_name in female_characters:
                            female_characters.append(joined_name)
                            already_added = True
                        elif single_name in unknown_gender:
                            continue
                        else:
                            name_gender = gc.resolveGender(single_name, None)
                            if name_gender == "male":
                                male_characters.append(joined_name)
                                already_added = True
                            elif name_gender == "female":
                                female_characters.append(joined_name)
                                already_added = True
                            else:
                                if full_name.index(single_name) == len(full_name) -1:
                                    unknown_gender.append(joined_name)
                                else:
                                    try:                                                #This try except methos is necessary since Genderize has a daily request limit
                                        name_gender = Genderize().get([single_name])
                                        if name_gender[0]["gender"] == "male":
                                            male_characters.append(joined_name)
                                            already_added = True
                                        elif name_gender[0]["gender"] == "female":
                                            female_characters.append(joined_name)
                                            already_added = True
                                        else:
                                            continue
                                    except:
                                        continue
                                


    return male_characters, female_characters, unknown_gender


