import glob
import os
print("Moving Files....")


os.makedirs('templates')

for item in glob.glob("*.html"):
    os.rename(item, 'templates/' + item)
