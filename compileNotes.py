import os
import zipfile

def log(type, message):
    print("[" + type + "]\t" + message)

def moveFile(file, folder):
    directories = [
        "./Windows/Lab Attacks/",
        "./Windows/Lab Creation/",
        "./Windows/Forensics"
    ]

    log("ASK", "In which directory do you want to save in?")
    for directory in directories:
        log("LIST", str(directories.index(directory)) + " - " + directory)
    
    dirIndex = input("- Choose a directory number: ")
    directoryToSaveIn = directories[int(dirIndex)]
    log("INFO", "Saving notes in " + directoryToSaveIn)
    log("DEBUG","Moving folder: " + folder)
    os.rename("./temp/" + folder, directoryToSaveIn + folder)
    log("DEBUG","Moving file: " + file)
    os.rename("./temp/" + file, directoryToSaveIn + file)

    log("SUCCESS", "Finished compiling notes!")
    log("!!!!!!", "DO NOT FORGET TO REMOVE THE .zip FILE")

def finish(zip):
    files = [f for f in os.listdir("./temp/") if os.path.isfile(os.path.join("./temp", f))]
    for f in files:
        if f.split(".")[1] == "md":
            pageId = ""
            log("INFO", "Found new page in export: " + f)
            log("DEBUG", "Extracting page ID.")
            pageId = f.split(".")[0].split(" ")[-1]
            log("DEBUG", "Found page ID: " + pageId)
            log("DEBUG", "Searching for images directory")
            directoryName = f.split(".")[0]
            directoryExists = os.path.isdir("./temp/" + directoryName)
            if directoryExists:
                log("INFO", "Found Images directory")
                newNameDirectory = directoryName.replace(" " + pageId, "")
                log("DEBUG", "Renaming Images directory from \"" + directoryName + "\" to \"" + newNameDirectory + "\"")
                os.rename("./temp/" + directoryName, "./temp/" + newNameDirectory)
            newNameFile = f.replace(" " + pageId, "")
            log("INFO", "Renaming file from \"" + f + "\" to \"" + newNameFile + "\"")
            os.rename("./temp/" + f, "./temp/" + newNameFile)
            log("INFO", "Relinking image paths in " + newNameFile)

            log("DEBUG", "Opening " + newNameFile)
            mdFile = open("./temp/" + newNameFile, "r")
            contents = mdFile.read()
            log("DEBUG", "Replacing paths in " + newNameFile)
            newContents = contents.replace("%20" + pageId, "")
            log("DEBUG", "Closing file " + newNameFile)
            mdFile.close()
            log("DEBUG", "Writing new contents in " + newNameFile)
            mdFileWrite = open("./temp/" + newNameFile, "w")
            mdFileWrite.write(newContents)
            log("DEBUG", "Closing file " + newNameFile)
            mdFileWrite.close()

            moveFile(newNameFile, newNameDirectory)
            
input("Please put the Export-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.zip file in current directory and press any key to continue.")

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.split(".")[1] == "zip":
        log("INFO", "Found new uncompiled export: " + f)
        log("DEBUG", "Extracting uncompiled export: " + f)
        path_to_zip_file = "./" + f
        directory_to_extract_to = "./temp/"
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
            finish(f)
