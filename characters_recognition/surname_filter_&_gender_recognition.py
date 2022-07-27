import re

names = {'Injuns', 'Edward', 'Wilson', 'Hastings', 'Stroud', 'Sintram', 'Castilian Amoroso', 'Annie Ridgway', 'Albert Morrison', 'Gabrielle', 'Naval Heroes', 'Redfern', 'Janey', 'Steal', 'Oswald', 'Bastables', 'Miss Dora', 'Young Lady Missing', 'Hildegarde Cunigonde', 'Father Time', 'Horace Octavius', 'Malabar', 'Katinka', 'Dick Turpin', 'Jane', 'Bagheera', 'Mrs Leslie', 'Jim Carlton', 'Bastable', 'Albert', 'Noel', 'Sam Redfern', 'Carlton', 'Noel Bastable', 'Ali Baba', 'Rosenbaum', 'Ellis', 'Lookee', 'Fame', 'Dora', 'Indian Uncle', 'Annie', 'Aunt Emily', 'Count Folko', 'Mary', 'Lewisham', 'Gaboriau', 'Quentin Durward', 'Babel', 'Alice The Princess', 'Pincher', 'Bon', 'Alicia', 'Amoroso', 'Etait', 'Oswald Bastable', 'Dicky', 'Guy Fawkes', 'Pauline', 'Eliza', 'Denny', 'Lord Tottenham', 'Blackheath', 'Hildegarde', 'Nelson', 'Alice', 'Noeloninuris', 'Flings', 'Victoria', 'Daisy', 'Trafalgar', 'Kipling', 'Dickens', 'Balliol', 'Take Noel', 'Dick', 'Gordon', 'Holloway', 'Hardy', 'Claude Duval', 'Little Alice', 'Osrawalddo', 'Bravo', 'Foulkes', 'Dick Diddlington'}


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
    return True








print(filter_surnames(names))

