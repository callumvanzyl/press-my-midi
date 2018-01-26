import errno, json, mido, os, random, thread, time

from mido import MidiFile
from _sendkeys import char2keycode, key_up, key_down

def press_key(keyString):
    isUpper = keyString.isupper()
    isSpecial = keyString in specialBindings

    if isSpecial:
        keyString = str(specialBindings[keyString])

    if isSpecial or isUpper:
        key_down(16)
            
    key_down(char2keycode(keyString.lower()))
    key_up(char2keycode(keyString.lower()))
            
    if isSpecial or isUpper:
        key_up(16)
    
def process_message(message):
    if ((message.type == "note_on") and (message.velocity > 0)):
        try:
            try:
                keyString = str(bindings[str(message.note)])
            except:
                print("The MIDI note %d has not been bound to a key. Skipping.") % (message.note)
                return
            press_key(keyString)    
        except:
            print("The application has encountered an error.")
        
def play_track(path):
    print("Your MIDI file will begin playing in 3 seconds.\nPlease be sure that your targeted window is in focus!")

    time.sleep(3)

    for m in MidiFile(path).play():
        thread.start_new_thread(process_message, (m,))
        
def init():
    try:
        os.makedirs("MIDI Files/")
        print("Created empty MIDI Files directory.")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            print("Encountered an error while opening MIDI Files directory.")
            time.sleep(3)
            return

    possibleFiles = []
    
    for i, v in enumerate(os.listdir("MIDI Files/")):
        possibleFiles.insert(i, v)
        time.sleep(0.005)
        print("%d: %s") %(i, v)

    if len(possibleFiles) == 0:
        print("You have no MIDI tracks available to play.")
        time.sleep(3)
        return
        
    print("Please choose a MIDI track to play...")
    index = int(raw_input("> "))
    
    if (index < 0) or (index >= len(possibleFiles)):
        print("YOUR INPUT IS NOT VALID!")
        time.sleep(1.5)
        init()

    chosenFile = possibleFiles[index]

    if (chosenFile.endswith(".midi") or chosenFile.endswith(".mid")):
        play_track(("MIDI Files/%s") % (chosenFile))
    else:
        print("THE FILE THAT YOU HAVE CHOSEN IS NOT A MIDI TRACK!")
        time.sleep(1)
        init()

    print("The track has finishing playing.")
    time.sleep(1.5)
    init()

if __name__ == "__main__":
    print("PressMyMIDI")
    print("--------------------------------")
    print("--------------------------------")
    
    gotFiles = True
        
    try:
        global bindings
        bindings = json.loads(open("bindings.json").read())
    except:
        print("The file bindings.json is missing or cannot be read.")
        time.sleep(3)
        gotFiles = False

    try:
        global specialBindings
        specialBindings = json.loads(open("special_bindings.json").read())
    except:
        print("The file special_bindings.json is missing or cannot be read.")
        time.sleep(3)
        gotFiles = False
        
    if gotFiles:
        time.sleep(0)
        init()
