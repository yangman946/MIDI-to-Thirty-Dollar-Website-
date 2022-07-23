# simple user wizard

import midi2tdw
import os 

# todo: add UI?

def getfiles():
    files = []
    # Iterate directory
    for file in os.listdir("in"):
        # check only text files
        if file.endswith('.mid'):
            files.append(file)

    return files

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def wizard():
    cls()
    result = getfiles()
    if (len(result) == 0):
        print(f"NO MIDI FILES FOUND IN: {os.getcwd()}\\in\\")
        input("PRESS ANY KEY TO CONTINUE...")
        quit()

    print(f"MIDI FILES IN: {os.getcwd()}\\in\\")
    for i, item in enumerate(result):
        print(f"{i} - {item}")

    
    
    generating = False
    selectedindex = 0
    while generating == False:
        selectedindex = input(f"SELECT THE FILE YOU WANT TO CONVERT [{0} - {len(result) - 1}] (or Q to quit): ")

        if selectedindex.lower() == "q":
            generating = True
            quit()
        else:
            try:
                if int(selectedindex) >= 0 and int(selectedindex) <= len(result) - 1:
                    print(f"CONVERTING {result[int(selectedindex)]}")
                    generating = True
                else:
                    print(f"INVALID INDEX")
            except ValueError:
                print(f"INPUT AN INTEGER INDEX [{0} - {len(result) - 1}]: ")


    if generating:
        process = midi2tdw.midi2tdw(f"in\\{result[int(selectedindex)]}")
        print(f"FILE CONVERTED AT: {midi2tdw.midi2tdw.getoutput(process)}")
        done = False
        while done == False:
            user = input("CONVERT ANOTHER? (y/n): ")
            if user.lower() == "y":
                done = True
                wizard()
            elif user.lower() == "n":
                done = True
                quit()
            else:
                print("INVALID INPUT")
            

if __name__ == "__main__":
    wizard()



        

