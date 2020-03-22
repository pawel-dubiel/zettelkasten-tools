# Python3
# A naive program that allows rename org notes files, and updates links 
# also we can specify a new title
# Autocompletes file paths
# it makes backup before doing changes (zip)
# specify in .env directories with slash at the end
# NOTES_BACKUP_PATH=""
# NOTES_PATH=""

import os
import sys
import readline
import shutil
import time
from dotenv import load_dotenv

load_dotenv()
NOTES_BACKUP_PATH = os.getenv("NOTES_BACKUP_PATH")
NOTES_PATH = os.getenv("NOTES_PATH")

if not NOTES_BACKUP_PATH or not os.path.exists(NOTES_BACKUP_PATH):
    print("Missing env NOTES_BACKUP_PATH or not readable")
    sys.exit()

if not NOTES_PATH or not os.path.exists(NOTES_PATH):
    print("Missing env NOTES_PATH or not readable")
    sys.exit()

mypath=NOTES_PATH
backup=NOTES_BACKUP_PATH

items = os.listdir(mypath)
fileList = [name for name in items if name.endswith(".org")]

def completer(text, state):
    options = [x for x in fileList if True if x.find(text) != -1 else False]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

print( "search files in "+ mypath + " (tab autocomplete)")
FileName = input("> ")

if (not os.path.exists(mypath+FileName)):
        print("file not exists")
        sys.exit()

newName = input( "rename "+ FileName +" to: ")

readline.set_completer()

with open(mypath+FileName, 'r') as original: content    = original.read()

oldTitle = ""
if content.startswith("#+TITLE:"): 
        oldTitle=content.split("\n")[0]

newTitle = input("old title: " + oldTitle + " provide a new Title (or press enter for no change): ")
process = input ("rename " + FileName + " to " + newName + " with Title: " + newTitle + "(Y) for yes ")

if process != "Y":
    print ("abort")
    sys.exit()

if os.path.exists(mypath+newName):
    print (newName + " file already exists, please try again")
    sys.exit()

shutil.make_archive(backup+"notes"+ str(int(time.time())), 'zip', mypath)

os.rename(mypath+FileName, mypath+newName)

with open(mypath+newName, 'r') as original: data = original.read()

if newTitle:
    print("provided new Title: "+newTitle)
    if data.startswith("#+TITLE:"):
        data = "\n".join(data.split("\n")[1:])
    with open(mypath+newName, 'w') as modified: modified.write("#+TITLE: "+ newTitle +"\n" + data)

newFileList = []
for item in fileList:
    if item == FileName:
        newFileList.append(newName)
    else:
        newFileList.append(item)

for name in newFileList:
    oldText=None
    newText=None
    with open(mypath+name) as f:
        oldText=f.read()
        newText=oldText.replace(FileName, newName)

    if newText:
        if oldText != newText:
            with open(mypath+name, "w") as f:
                print("replaced links in "+ name + " from: " + FileName + " to: " + newName)
                f.write(newText)
