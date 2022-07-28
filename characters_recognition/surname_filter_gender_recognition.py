from genderize import Genderize
from genderComputer import GenderComputer
import re


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

    return single_names, multiple_names







def gender_recognition(names_set):
    gc = GenderComputer()
    single_names, multiple_names = filter_surnames(names_set)
    male_words = {"sir", "lord", "king", "prince",  "mister", "mr", "father", "uncle", "son", "brother"}
    female_words = {"lady", "queen", "princess", "dame", "miss", "mrs", "ms", "aunt", "mother", "sister", "daughter"}
    male_characters = []
    female_characters = []
    unknown_gender = []

    for name in single_names:                   #First check by means of genderComputer on the list of names composed by a single word
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

    
    for full_name in multiple_names:                        #The first block of checks aims at guessing the gender on the basis of genderdized words present in the strings without using any additional library
        joint_name = " ".join(full_name)
        if len(set(full_name) & male_words) > 0:
            male_characters.append(joint_name)
        elif len(set(full_name) & female_words) > 0:
            female_characters.append(joint_name)
        else:                                                       #Now, it is used the same process as before: first we check the gender by meand of genderComputer
            gender = gc.resolveGender(joint_name, None)
            if gender == "male":
                male_characters.append(joint_name)
            elif gender == "female":
                female_characters.append(joint_name)
            else:
                try:                                     #The following block of check is necessary since Genderize does not work with multiple-words names
                    already_added = False
                    for single_name in full_name:
                        if already_added:
                            continue
                        else:
                            if single_name in male_characters:
                                male_characters.append(joint_name)
                                already_added = True
                            elif single_name in female_characters:
                                female_characters.append(joint_name)
                                already_added = True
                            elif single_name in unknown_gender:
                                continue
                            else:
                                name_gender = Genderize().get([single_name])
                                if name_gender[0]["gender"] == "male":
                                    male_characters.append(joint_name)
                                    already_added = True
                                elif name_gender[0]["gender"] == "female":
                                    female_characters.append(joint_name)
                                    already_added = True
                                else:
                                    if full_name.index(single_name) == len(full_name) -1:
                                        unknown_gender.append(joint_name)
                                    else:
                                        continue
                except:
                    unknown_gender.append(joint_name)

    return male_characters, female_characters, unknown_gender





print(gender_recognition({"bloody mary"}))



