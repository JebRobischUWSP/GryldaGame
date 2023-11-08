import os
import sys
import io
import random

random.seed()

#Flags
knownRooms = [None, True, True, True, True, True]; #Index corresponds to room number, once True, text will reflect knowlege of room behind door.
#ALTERNATE DIFFERENCE: Grylda already knows all the rooms; it's her house. Technically just a textual change
tableSearched = False; # Gives +1 Bonus
grylaConfronted = False;
grylaPercieved = False;
grylaDead = False;
gotKey = False;

#Stats
currentRoom = 1;
gameState = 0; # Tracks current state: 0-explore, 1-battleGryla
battleState = 0; # 0-notFighting, 1-fighting
grylaHealth = 2; # 20+ sets to 0 (aka -2, double damage), 1- sets to 2 (heal)
playerHealth = 2; # Never recoverss

#General Functions
def GetIntInput(message, min, max, disclude=None): #Gets & returns input as int bounded by [min,max]. If input fails, retry until it succeeds. If it matches a 'discluded' value (list of int), return None
    result = input(message);
    while(True):
        try:
            result = int(result);
            if disclude != None:
                for val in disclude:
                    if result == val:
                        return None;
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
    path = 'dataAlternate\\' + fileName + '.txt';
    openFile = io.open(path, 'r', encoding='utf8');
    print(openFile.read());
    openFile.close();

def KillGryl(message): #I didn't really need to make this a function, but I just came up with the pun and it was too good to pass up.
    global grylaDead, gotKey, gameState;
    print('\n' + message + '\n');
    print("You finally beat that mangy freeloading adventurer!\nWhat's this? As they lie crumpled on the floor, you notice a small, metal object fall out of their pocket. A key!\nYou should go check your bedroom chest! Hopefully that adventurer didn't use your special potion.\n");
    grylaDead = True; # I could've probably just used one flag for this, but whatever.
    gotKey = True;
    gameState = 0; # What's up with python and locally scoping global varibles in functions??? If I'm changing a global variable, I want to change a global variable.
    pause();

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
                print(  FormatActions(GetTravelActionText(2), "Don't even bother; they'll tire and eventually leave your house (Flee)")  );
                userIn = GetIntInput("Choose an action: ", 1, 2);
                if userIn == 1:
                    currentRoom = 2;
                elif userIn == 2:
                    GameOver("Instead of confonting that wretched squatter, you decide to wait it out nearby.\nYou're pretty sure you can hear them trashing up the place.\nDamn, should've intervened.\nGame Over!");
            elif currentRoom == 2:
                DisplayTextData('2mainroom');
                if not tableSearched:
                    print("A glimmer from the table catches your eye.\n\nYou are currently in the Central Room (Room 2)\n");
                    print(  FormatActions(GetTravelActionText(3), GetTravelActionText(4), "Search your Work Table")  );
                    userIn = GetIntInput("Choose an action: ", 1, 3);
                    if userIn == 1:
                        currentRoom = 3;
                    elif userIn == 2:
                        currentRoom = 4;
                    elif userIn == 3:
                        tableSearched = True;
                        _ = os.system('cls');
                        print("Would you look at that, your lucky glowing ring!\nIt produces 5ft of dim light in a sphere around you when in unlit areas. It's also fashionable\nMight be good for landing more accurate punches on that courtesy-lacking freeloader.\n\n")
                        # This item is supposed to play into the facing your fears thing; a gift of light to help face your fear of the dark (with darkness as a theme here, I imagine one of the intended faced fears is of the dark)
                        pause();
                else: # You can't search the table again. Sucks.
                    print("You are currently in the Central Room (Room 2)\n");
                    print(  FormatActions(GetTravelActionText(3), GetTravelActionText(4))  );
                    userIn = GetIntInput("Choose an action: ", 1, 2);
                    if userIn == 1:
                        currentRoom = 3;
                    elif userIn == 2:
                        currentRoom = 4;
            elif currentRoom == 3:
                DisplayTextData('3kitchen');
                print("You are currently in the Kitchen (Room 3)\n");
                print(  FormatActions("Search the Room", GetTravelActionText(2), GetTravelActionText(5))  );
                userIn = GetIntInput("Choose an action: ", 1, 3);
                if userIn == 1:
                    _ = os.system('cls');
                    if random.randint(1,100) == 100:
                        print("You search around the room, and find 1gp!\nYou were wondering where that went!\n\n");
                    else:
                        print("You search around, but nothing's really changed since you left. Well, there's some muddy boot prints. Figures.\n\n");
                    pause();
                elif userIn == 2:
                    currentRoom = 2;
                elif userIn == 3:
                    currentRoom = 5;
            elif currentRoom == 4:
                DisplayTextData('4bedroom');
                print("You are currently in the Bedroom (Room 4)\n");
                print(  FormatActions("Search the Room", GetTravelActionText(2), "Try to Open the Chest")  );
                userIn = GetIntInput("Choose an action: ", 1, 3);
                if userIn == 1:
                    _ = os.system('cls');
                    if random.randint(1,100) == 100: # Lucky penny!
                        print("You search around the room, and find 1gp!\nYou were wondering where that went!\n\n");
                    else:
                        print("You search around, but find nothing of value.\n\n");
                    pause();
                elif userIn == 2:
                    currentRoom = 2;
                elif userIn == 3:
                    if gotKey:
                        print("Alright, let's make sure you don't have to search that adventurer's pockets again.\n...\n\nThe lock clicks open. You peer into the chest...\n")
                        pause();
                        openFile = io.open('dataAlternate\\winner.txt', 'r', encoding='utf8');
                        print();
                        GameOver(openFile.read());
                    else:
                        print("Locked. Maybe the contents are still safe and sound?")
                        pause();
            elif currentRoom == 5:
                if not grylaDead:
                    DisplayTextData('5cellar');
                    input("Press Enter to start the battle! ");
                    gameState = 1;
                else:
                    DisplayTextData('5cellarpostfight');
                    print("You are currently in the Cellar (Room 5)\n");
                    print(  FormatActions(GetTravelActionText(3))  );
                    userIn = GetIntInput("Choose an action: ", 1, 1); #I find this alarmingly funny. Yeah, there's a list of possible actions. Yeah, it's one action. Yeah, you still need to select the action.
                    if userIn == 1:
                        currentRoom = 3;
                    else:
                        print("What??? Huh??? How???");
        elif gameState == 1:
            if battleState == 0:
                print("You are facing a scruffy, good-for-nothing adevnturer!\n\n");
                if grylaConfronted and grylaPercieved:
                    print("Crap, you have no other choice. You have to fight them!\n");
                    print(  FormatActions("Fight them!", "Leave; you don't feel like actually FIGHTING the guy.")  );
                    userIn = GetIntInput("Choose an action: ", 1, 2);
                    if userIn == 1:
                        battleState = 1;
                        pause();
                        continue; # Reset game loop to switch to fighting state
                    elif userIn == 2:
                        GameOver("You sigh dejectedly and make your way back out of the cellar.\nWithin moments, you hear the sound of ransacking from the cellar.\nWell, you already made up your mind. Time to wait this hoodlum out.\nGAME OVER\n\nTip: Beating people up may convince them to leave your property.");
                print(  FormatActions("Fight them!", "Scare them off!", "Talk them down.")  );
                discluded = [] if not grylaConfronted else [2]; # Setup the disclude list in case players already did the other options. Much easier than writing out this section again for each permutation.
                discluded += [] if not grylaPercieved else [3];
                userIn = None;
                while(True):
                    userIn = GetIntInput("Choose an action: ", 1, 3, disclude=discluded);
                    if userIn != None:
                        break;
                    else:
                        print("That didn't work, knucklehead! You have to try something else.");
                if userIn == 1:
                    print("You ready your weapon... it's time to fight this gremlin head-on!\n");
                    battleState = 1;
                    pause(); #Bit janky of a way to do it, requiring a pause here, but otherwise players couldn't read this line, and there's not an easy way i can think of to switch states with an attack round
                elif userIn == 2:
                    _ = os.system('cls');
                    print("This isn't their property! These aren't their belongings!\nYou yell at the adventurer, threatening grand retribution!\n\n");
                    input("Press Enter to roll for Intimidation.");
                    plrDieMod, plrDie = RollD20();
                    grylaDieMod, grylaDie = RollD20(mod = 4);
                    print("\nYou rolled " + str(plrDieMod) + " (" + str(plrDie) + "+0)");
                    print("The Adventurer rolled " + str(grylaDieMod) + " (" + str(grylaDie) + "+4)");
                    if plrDieMod > grylaDieMod: #Note wording in assignment: "If the player rolls HIGHER", not higher or equal.
                        KillGryl("You breate and belittle this perosn so hard, you start to feel a little bad for them.\nAs if struck by a power word: Kill, they crumple up on the floor, defeated by the pen.");
                    else:
                        print("You throw a couple of crude insults their way.\nThe adventurer cackles, makes a couple rude comments back, and readies their weapon.\nDrats.\n");
                        grylaConfronted = True;
                        pause();
                elif userIn == 3:
                    _ = os.system('cls');
                    print("Maybe you could convince this person, however cruel their tresspassing may be, to just leave.\n\n");
                    input("Press Enter to roll for Decpetion.");
                    plrDieMod, plrDie = RollD20();
                    grylaDieMod, grylaDie = RollD20(mod = -2);
                    print("\nYou rolled " + str(plrDieMod) + " (" + str(plrDie) + "+0)");
                    print("The Adventurer rolled " + str(grylaDieMod) + " (" + str(grylaDie) + "-2)");
                    if plrDieMod > grylaDieMod: #"If the player wins" is annoyingly vauge for a description that specified the exact operator ('>') only 3 sentences before
                        KillGryl("You have a \"polite intellectual conversation\" with the Adventurer, and come to the mutual conclusion that they shouldn't be messing with your things.\nThe adventurer apologises, goes to leave, and then trips on a small crack, crumpling to the floor. Looks like they may have gotten a concussion....\n\nWait a second... their pack is filled to the brim with your belongings! Lucky that scoundrel fell victim to his own lack of balance.");
                    else:
                        print("The adventurer seems much more interested in keeping your belongings, it seems. Something about \"nasty old hag\". Maybe you need to try a different approach.");
                        grylaPercieved = True;
                        pause();
            elif battleState == 1:
                print("You attack! Roll an attack die.");
                #Player's Turn
                modAmt = 1 if tableSearched else 0;
                plrDieMod, plrDie = RollD20(mod = modAmt);
                print("\nYou rolled " + str(plrDieMod) + " (" + str(plrDie) + "+" + str(modAmt) + ")");
                if plrDieMod >= 20: #Crit
                    print("(!) You hit a devestating blow!");
                    grylaHealth = 0; # Max health 2, so don't even bother subtracting
                elif plrDie <= 1: #Fail
                    print("(!) You missed horribly! The Adventurer takes this time to drink one of YOUR health potions!");
                    grylaHealth = 2;
                elif plrDieMod >= 12: #Hit
                    print("You hit them!");
                    grylaHealth -= 1;
                else: #Miss
                    print("You missed.");
                #Gryla's Turn
                if grylaHealth <= 0: #End fight
                    KillGryl("\nAs you give a good smack to the Adventurer, they crumple on the ground, defeated.\nYou might have broken one of their ribs... looks painful. Rightfully so!");
                elif plrDie > 1: #Gryla attack (If not heal)
                    print("\nThe Adventurer Goes in for the attack!");
                    grylaDieMod, grylaDie = RollD20(mod = -4);
                    print("They rolled " + str(grylaDieMod) + " (" + str(grylaDie) + "-4)");
                    if grylaDieMod > 12:
                        print("They hit you!\n");
                        playerHealth -= 1;
                    else:
                        print("They Miss!\n");
                    pause();
                if playerHealth <= 0:
                    GameOver("You fall to the ground, bested by that lucky sonnuva- ow.\nDefeatedly, you crawl up the stairs and out the hut. No way you can take on that hoodlum in your current state.\nFrom the hut, you hear the telltale sounds of ransacking. Just great.\nGAME OVER");
            else:
                GameOver('ERROR: Game entered a nonexistant battleState, ' + str(battleState));
        else:
            GameOver('ERROR: Game entered a nonexistant state, ' + str(gameState));
except Exception as error:
    GameOver('EXCEPTION: ' + str(error) + '\nPlease report this to the developer!'); 
"""
APPROVED CONCEPTS
io library to display unicode (Mainly umlaut y)
os.system to clear the terminal
functions (just in general)
Capturing an exception's text in an try/except
Hinting at the existence of the fireplace in room 3 before entering it
Unpacking operator 
Occasionally giving the player a "lucky 1gp" when doing either of the 2 repeatable search actions (Not implemented yet)
Closing opened files (Prevent Memory Leaks)
Using min() and max() (Not actually used UNLESS I add die roll clamping)
"Global" keyword
Ternary Operator (It's not nessecary, but I love inline if statements for reasons I cannot understand. Also, one of the few chances I get to make my code more concise)
EXPANDED ASPECT: More skill checks, mainly perception, and getting fragments of the key/putting them together (gives reason to use searches)

UNAPPROVED CONCEPTS
Snarky code comments
"""

"""
DOCUMENTATION
Written in Notepad++, Tested in Powershell & Command Prompt
Only major difference using IDLE is that the console won't clear from os.system('clr')

For the fight, how I interpret it: 20 or more (5%, or 10% with table item) is a hit so powerful that you defeat Gryla right then and there.
1 or less (since you cannot get a negative modifier for the fight specifically (and the other possiblities don't have crit fail conditions) is considered a "heal" turn for Grylda, which will bring her back to 2 hp (each hit is 1 hp)
The 'heal turn' causes a requirement of >= 3 hits, and is a lot more sensical to implement (Otherwise, crit fail activates only once? That's not ineresting at all).
    Also, Grÿla doesn't attack on heal turns, to make them a little more fair if the player has REALLY bad luck.
So, treating it like this give the player a net benefit, and since critical conditions don't exist for other fight actions, it otherwise doesn't matter.
EXTRA NOTE: Actually, since it's possible to have either +0 or +1, it may be impossible to crit fail. SO, instead, crit fails work off of the unmodified roll, but crit successes are still with modifiers.

_=_ is a placholder so that python doesn't throw a fit over an if/elif/else block not having any body
"""