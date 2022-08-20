from charEx import *
from genderRec import *
import os
from tqdm import tqdm #for progress bar


directory_paths = ["assets/Corpus/female-writers/", "assets/Corpus/male-writers/"]
file_paths = []

for path in directory_paths:
    for root, directories, files in os.walk(path):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)



#run the code in this way:
#for idx, filepath in enumerate(file_paths):
#    print(idx, filepath)

#ncl = gender_recognition(get_characters(open(file_paths[10]).read()))
#print(ncl)


#or in this way:


characters = dict()

idx = 1
for file_path in tqdm(file_paths): #tqdm just displays a progress bar in the terminal
    characters["book-"+file_path] = gender_recognition(get_characters(open(file_path, encoding="utf8").read()))
    idx += 1


#print(characters)

for key in characters:
    print(key, '-->', characters[key])

