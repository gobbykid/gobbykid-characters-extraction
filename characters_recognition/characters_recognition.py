from characters_recognition_functions import *
import os
#import gender_guesser.detector as ggd
#import gender_detector as g_d

directory_paths = ["Corpus/female-writers/", "Corpus/male-writers/"]
file_paths = []

for path in directory_paths:
    for root, directories, files in os.walk(path):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)



#run the code in this way:

#ncl = get_characters(open(file_paths[5]).read())

#or in this way:

"""
characters = dict()
idx = 1
for file_path in file_paths:
    characters["book-"+str(idx)] = get_characters(open(file_path).read())
    idx += 1
"""
