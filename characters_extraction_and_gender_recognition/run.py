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

#ncl = gender_recognition(get_characters(open(file_paths[14]).read()))
#print(ncl)


#or in this way:


characters = dict()
"""
idx = 1
for file_path in tqdm(file_paths): #tqdm just displays a progress bar in the terminal
    characters["book-"+file_path] = gender_recognition(get_characters(open(file_path, encoding="utf8").read()))
    idx += 1


#print(characters)

for key in characters:
    print(key, '-->', characters[key])
"""




set0 = {'bill', 'jim', 'avast', 'hunter', 'ben', 'trelawney', 'dick', 'livesey', 'scatter', 'george', 'dogger', 'harry', 'tom', 'benbow', 'obrien', 'alan', 'billy', 'barbecue', 'jack', 'hawkins', 'jim hawkins', 'long john silver', 'captain smollett', 'mr dance', 'capn trelawney', 'george merry', 'mr hands', 'mr arrow', 'mr smollett', 'long john', 'black dog', 'john silver', 'captain kidd', 'mr trelawney', 'benjamin gunn', 'abraham gray', 'captain flint', 'doctor livesey', 'ben gunn', 'capn hawkins', 'tom morgan', 'master silver', 'capn smollett', 'master pew', 'mr hawkins', 'mr silver', 'billy bones', 'davy jones', 'tom redruth', 'job anderson'}
set1 = {'bill', 'ben', 'barbecue', 'morgan', 'jack', 'obrien', 'jim', 'hawkins', 'dogger', 'billy', 'alan', 'hunter', 'george', 'tom', 'pew', 'dick', 'benbow', 'captain kidd', 'captain flint', 'davy jones', 'mr silver', 'black dog', 'capn hawkins', 'long john silver', 'capn trelawney', 'mr smollett', 'george merry', 'tom morgan', 'doctor livesey', 'benjamin gunn', 'mr arrow', 'master silver', 'captain smollett', 'billy bones', 'mr trelawney', 'mr hands', 'mr hawkins', 'jim hawkins', 'john silver', 'capn smollett', 'job anderson', 'long john', 'mr dance', 'abraham gray', 'tom redruth', 'ben gunn'}
print(set0 - set1)
