import os
import io

#Flags
knownRooms = [True, True, False, False, False, False]; #Index corresponds to room number, once True, text will reflect knowlege of room behind door.
tableSearched = False;


#Stats
currentRoom = 0;
gameState = 0; # Tracks current state: 0-explore, 1-battleGryla

_ = os.system('cls') #Clears without printing code
#Present Scenario
openFile = io.open('Data\GrylaScenario.txt', 'r', encoding='utf8');
print(openFile.read());
input('Press Enter to continue...');

#Game Loop
while(True)
    if gameState == 0:
        
    elif gameState == 1:
        
    else
        # Exit game, with gameover message as error