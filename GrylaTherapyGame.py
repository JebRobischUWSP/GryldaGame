import os
import sys
import io
import random

random.seed()

#Flags
knownRooms = [None, True, False, False, False, False]; #Index corresponds to room number, once True, text will reflect knowlege of room behind door.
tableSearched = False; # Gives +1 Bonus
chestFound = False;
grylaDead = False;
gotKey = False;

#Stats
currentRoom = 1;
gameState = 0; # Tracks current state: 0-explore, 1-battleGryla

#General Functions
def GetIntInput(message, min, max): #Gets & returns input as int bounded by [min,max]. If input fails, retry until it succeeds.
    result = input(message);
    while(True):
        try:
            result = int(result);
            if min == None or result >= min:
                if max == None or result <= max:
                    break;
                else: #Max is not None and result was greater
                    print("That's too high. Choose a number that's at most " + str(max) + ".");
            else: #Min is not None and result was lesser
                print("That's too low. Choose a number that's at least " + str(min) + ".");
        except:
            print("That isn't a whole number.");
        result = input(message);
    return result;

def RollD20(mod=0): #Rolls a d20, returns the result plus any supplied modifier and the original result as tuple
    result = random.randint(1,20);
    modResult = result + mod;
    #clampResult = max(min(modResult, 20), 1) #Don't know if I need this? Might be good for game balance
    #return modResult, clampResult, result
    return modResult, result;

def pause(): # Shorthand for the enter to continue thing
    input('Press Enter to continue...');
    
def GameOver(message): # Displays message, then prompts to close. Also used for error handling.
    _ = os.system('cls');
    print(message + "\n\n");
    input('Press Enter to close the game ');
    sys.exit();

def FormatActions(*args): # Takes a collection of strings, then returns a printable action list string. Does not handle input.
    result = "Available Actions:\n";
    i = 0;
    for a in args:
        i += 1;
        result += '(' + str(i) + ') ' + a + '\n'; # Example: (1) Open the Door
    return result;

def GetTravelActionText(roomId): # Checks if room (indicated by room number) is known. If it is, provide the known action text. if not, provide the unknown.
    result = "Enter an Unknown Room";
    if knownRooms[roomId]:
        if roomId == 1:
            result = "Exit to the Porch"; #This shouldn't be possible?
        elif roomId == 2:
            result = "Enter the Central Room";
        elif roomId == 3:
            result = "Enter the Kitchen";
        elif roomId == 4:
            result = "Enter the Bedroom";
        elif roomId == 5:
            result = "Descend into the Cellar"; #By the time you can get this message, there's no point in going there
    return result + ' (Room ' + str(roomId) + ')';

def DisplayTextData(fileName):
    path = 'data\\' + fileName + '.txt';
    openFile = io.open(path, 'r', encoding='utf8');
    print(openFile.read());
    openFile.close();

_ = os.system('cls'); #Clears without printing code

#Present Scenario
DisplayTextData('scenario')
pause();

#Game Loop
try:
    while(True):
        _ = os.system('cls');
        if gameState == 0:
            knownRooms[currentRoom] = True; # gain knowlege of room
            if currentRoom == 1: #Open door or flee
                DisplayTextData('1porch');
                DisplayTextData('1porchwindow'); #Why do we need this in a seperate file if it's exclusive to the porch scene?
                print("You are currently on the Porch (Room 1)\n");
                print(  FormatActions(GetTravelActionText(2), "Flee from the Hut (This is your only chance!)")  );
                userIn = GetIntInput("Choose an action: ", 1, 2);
                if userIn == 1:
                    currentRoom = 2;
                elif userIn == 2:
                    GameOver("Before even entering the hut, you turn and flee.\nGrÿla will continue to haunt your mind.\nGame Over!");
            elif currentRoom == 2:
                DisplayTextData('2mainroom');
                if not tableSearched:
                    print("A glimmer from the table catches your eye.\n\nYou are currently in the Central Room (Room 2)\n");
                    print(  FormatActions(GetTravelActionText(3), GetTravelActionText(4), "Search the Messy Table")  );
                    userIn = GetIntInput("Choose an action: ", 1, 3);
                    if userIn == 1:
                        currentRoom = 3;
                    elif userIn == 2:
                        currentRoom = 4;
                    elif userIn == 3:
                        tableSearched = True;
                        _ = os.system('cls');
                        print("You found a small ring with a glowing enchanment!\nIt produces 5ft of dim light in a sphere around you when in unlit areas.\nIn turn, you get +1 to any attack rolls against enemies accustomed to dark environemnts.\n\n")
                        # This item is supposed to play into the facing your fears thing; a gift of light to help face your fear of the dark (with darkness as a theme here, I imagine one of the intended faced fears is of the dark)
                        pause();
                else: # You can't search the table again. Sorry!
                    print("You are currently in the Central Room (Room 2)\n");
                    print(  FormatActions(GetTravelActionText(3), GetTravelActionText(4))  );
                    userIn = GetIntInput("Choose an action: ", 1, 2);
                    if userIn == 1:
                        currentRoom = 3;
                    elif userIn == 2:
                        currentRoom = 4;
            elif currentRoom == 3:
                #Introduce Room
                print("You are currently in the Kitchen (Room 3)\n");
                print(  FormatActions("Search the Room", GetTravelActionText(2), GetTravelActionText(5))  );
                userIn = GetIntInput("Choose an action: ", 1, 3);
                if userIn == 1:
                    _=_
                    #Do search logic
                elif userIn == 2:
                    currentRoom = 2;
                elif userIn == 3:
                    currentRoom = 5;
            elif currentRoom == 4:
                #Introduce room
                print("You are currently in the Bedroom (Room 4)\n");
                print(  FormatActions("Search the Room", GetTravelActionText(2), "Try to Open the Chest")  );
                userIn = GetIntInput("Choose an action: ", 1, 3);
                if userIn == 1:
                    _=_
                    #Do search logic
                elif userIn == 2:
                    currentRoom = 2;
                elif userIn == 3:
                    _=_
                    #Do chest open logic
            elif currentRoom == 5:
                _ = _
        elif gameState == 1:
            _ = _
        else:
            GameOver('ERROR: Game entered a nonexistant state, ' + str(gameState));
except Exception as error:
    GameOver('EXCEPTION: ' + str(error) + '\nPlease report this to the developer!'); 
"""
APPROVED CONCEPTS
io library to display unicode (Mainly umlaut y)
os.system to clear the terminal
functions (just in general)

UNAPPROVED CONCEPTS
Capturing an exception's text in an try/except
Hinting at the existence of the fireplace in room 3 before entering it
Occasionally giving the player a "lucky 1gp" when doing either of the 2 repeatable search actions (Not implemented yet)
Closing opened files (Prevent Memory Leaks)
Using min() and max() (Not actually used UNLESS I add die roll clamping)
Snarky code comments
"""