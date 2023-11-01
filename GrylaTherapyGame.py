import os
import sys
import io

#Flags
knownRooms = [None, True, False, False, False, False]; #Index corresponds to room number, once True, text will reflect knowlege of room behind door.
tableSearched = False;
chestFound = False;
grylaDead = False;
gotKey = False;

#Stats
currentRoom = 1;
gameState = 0; # Tracks current state: 0-explore, 1-battleGryla

_ = os.system('cls') #Clears without printing code
#Present Scenario
openFile = io.open('Data\GrylaScenario.txt', 'r', encoding='utf8');
print(openFile.read());
input('Press Enter to continue...');

#Game Loop
while(True)
    if gameState == 0:
        knownRooms[currentRoom] = True; # gain knowlege of room
        if currentRoom == 1:
            
        elif currentRoom == 2:
            
        elif currentRoom == 3:
            
        elif currentRoom == 4:
            
        elif currentRoom == 5:
            
    elif gameState == 1:
        
    else
        # Exit game, with gameover message as error

"""
APPROVED CONCEPTS
io library to display unicode (Mainly umlaut y)
os.system to clear the terminal
functions (just in general)
"""