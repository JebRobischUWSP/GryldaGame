import os
import sys
import io
import random

random.seed()

#Flags
knownRooms = [None, True, False, False, False, False]; #Index corresponds to room number, once True, text will reflect knowlege of room behind door.
tableSearched = False; # Gives +1 Bonus
grylaConfronted = False;
grylaPercieved = False;
grylaDead = False;
gotKey = False;
keyBit1 = False;
keyBit2 = False;

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
    path = 'data\\' + fileName + '.txt';
    openFile = io.open(path, 'r', encoding='utf8');
    print(openFile.read());
    openFile.close();

def KillGryl(message): #I didn't really need to make this a function, but I just came up with the pun and it was too good to pass up.
    global grylaDead, gotKey, gameState;
    print('\n' + message + '\n');
    print("You have successfully overcame your fears and have beaten Grÿla!\nWhat's this? As she disintegrates, you notice a small, metal object. A key!\nYou should figure out what this unlocks before leaving. A witch as powerful as Grÿla must have something valuable lying around.\n");
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
                print('You try to look in from the outside...');
                plrDie, _ = RollD20();
                print("\nYou rolled " + str(plrDie));
                if plrDie > 8:
                    DisplayTextData('1porchwindow');
                else:
                    print("It's too dark to see into the hut. You have no idea what could be behind this door. Maybe it's Grÿla? That would be horrifying!"); 
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
                        if playerHealth <= 1:
                            print("You'd rather not--you're already pretty hurt, and the table is a little treacherous.");
                            pause();
                            continue;
                        print("You search around the table. It's a bit of a mess, and there's a lot of sharp instruments, but you might be able to find whatever's causing that glow...");
                        input("Press Enter to roll for Constitution. ")
                        plrDie, _ = RollD20();
                        print("\nYou rolled " + str(plrDie));
                        if plrDie > 8: # Now it's a risk-reward instead of an objectively good choice
                            tableSearched = True;
                            _ = os.system('cls');
                            print("You found a small ring with a glowing enchanment!\nIt produces 5ft of dim light in a sphere around you when in unlit areas.\nIn turn, you get +1 to any attack rolls against enemies accustomed to dark environemnts.\n\n")
                            # This item is supposed to play into the facing your fears thing; a gift of light to help face your fear of the dark (with darkness as a theme here, I imagine one of the intended faced fears is of the dark)
                            pause();
                        else:
                            _ = os.system('cls');
                            print("Ow! You cut yourself on one of the various broken flasks and poked your hand into a couple of dangerous-looking bits of metal.\nYou feel weaker than before. Best not to try that again.");
                            playerHealth = 1;
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
                    if gotKey and not keyBit2:
                        print("You search around for one of the missing key bits...\n");
                        input("Press Enter to roll for Perception. ")
                        plrDie, _ = RollD20();
                        print("\nYou rolled " + str(plrDie));
                        if plrDie > 10:
                            print("A-ha! That's one of the bits!");
                            if not keyBit1:
                                print("You should go look somewhere else for the other bit.");
                            else:
                                print("You have all the bits! Let's go unlock that chest!");
                            keyBit2 = True;
                        else:
                            print("Nothing. Maybe you need to look a little closer?");
                    else:
                        if random.randint(1,100) == 100: # Lucky penny! Not a perception roll, just an easter egg
                            print("You search around the room, and find 1gp!\nLucky you!\n\n");
                        else:
                            print("You search around, but find nothing of value.\n\n");
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
                    if gotKey and not keyBit1:
                        print("You search around for one of the missing key bits...\n");
                        input("Press Enter to roll for Perception. ")
                        plrDie, _ = RollD20();
                        print("\nYou rolled " + str(plrDie));
                        if plrDie > 10:
                            print("A-ha! That's one of the bits!");
                            if not keyBit2:
                                print("You should go look somewhere else for the other bit.");
                            else:
                                print("You have all the bits! Let's go unlock that chest!");
                            keyBit1 = True;
                        else:
                            print("Nothing. Maybe you need to look a little closer?");
                    else:
                        if random.randint(1,100) == 100:
                            print("You search around the room, and find 1gp!\nLucky you!\n\n");
                        else:
                            print("You search around, but find nothing of value.\n\n");
                    pause();
                elif userIn == 2:
                    currentRoom = 2;
                elif userIn == 3:
                    if gotKey:
                        if keyBit1 and keyBit2: #EXPANDED CONTENT: Key's broke, fix it
                            print("You hold the key and the 2 bits in place, and they magically fuse together! Neat!");
                            print("Maybe now that you repaired the key, it fits this chest.\n...\n\nHey, it worked! You peer into the chest...\n")
                            pause();
                            openFile = io.open('data\\winner.txt', 'r', encoding='utf8');
                            print();
                            GameOver(openFile.read());
                        elif keyBit1 or keyBit2:
                            print("I don't think you can open a lock with a half-complete key.\nTry searching another searchable room.\n");
                            pause();
                        else:
                            print("Time to find what Grÿla's been hiding!\n...\nHey, this key doesn't work! Looks like the 2 bits on the end have been snapped off, rendering it useless.\nMaybe if you search around the house, you could find them?\n");
                            pause();
                    else:
                        print("The chest is locked tight. It's sturdy, too. No way you're getting into it without a key.")
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
                print("You are facing Grÿla, the witch of your nightmares!\n\n");
                if grylaConfronted and grylaPercieved:
                    print("You have no other choice. You must fight her!\n");
                    print(  FormatActions("Fight the Witch!", "It's no use; Run!")  );
                    userIn = GetIntInput("Choose an action: ", 1, 2);
                    if userIn == 1:
                        battleState = 1;
                        pause();
                        continue; # Reset game loop to switch to fighting state
                    elif userIn == 2:
                        GameOver("With 2 failiures under your belt and little confidence in your ability to confront Grÿla, you turn tail and run.\nAs you burst out of the hut, you hear wicked cackling from the cellar.\nThis will not be the last you hear of this wicked witch.\nGAME OVER\n\nTip: Gryla is strong against pacifist techniques. Fighting is bound to be more effective, especially if you search around a bit beforehand.");
                print(  FormatActions("Fight the Witch!", "Confront your fear!", "Look for her weaknesses!")  );
                discluded = [] if not grylaConfronted else [2]; # Setup the disclude list in case players already did the other options. Much easier than writing out this section again for each permutation.
                discluded += [] if not grylaPercieved else [3];
                userIn = None;
                while(True):
                    userIn = GetIntInput("Choose an action: ", 1, 3, disclude=discluded);
                    if userIn != None:
                        break;
                    else:
                        print("That didn't work! You have to try something else.");
                if userIn == 1:
                    print("You ready your weapon... it's time to fight Grÿla head-on!\n");
                    battleState = 1;
                    pause(); #Bit janky of a way to do it, requiring a pause here, but otherwise players couldn't read this line, and there's not an easy way i can think of to switch states with an attack round
                elif userIn == 2:
                    _ = os.system('cls');
                    print("You don't fear her! You don't fear anything!\nYou yell out to Grÿla, confronting her with the power of your confidence!\n\n");
                    input("Press Enter to roll for Intelligence.");
                    plrDieMod, plrDie = RollD20();
                    grylaDieMod, grylaDie = RollD20(mod = 4);
                    print("\nYou rolled " + str(plrDieMod) + " (" + str(plrDie) + "+0)");
                    print("Grÿla rolled " + str(grylaDieMod) + " (" + str(grylaDie) + "+4)");
                    if plrDieMod > grylaDieMod: #Note wording in assignment: "If the player rolls HIGHER", not higher or equal.
                        KillGryl("You let it be known that you do not fear her! She has no power on you! She may be terrifying, but she cannot hurt you!\nHearing these words, Gryla siezes and slowly petrifies, crumbling to powerless ash.");
                        # Get wicked witch of the west'd, gryllo! (Not really, it's to dust instead of melting, but whatever)
                    else:
                        print("You try to convince her of your fearlessness, but it doesn't work.\nShe stands as haughtily as ever, confident in her grip over your mind.\n");
                        grylaConfronted = True;
                        pause();
                elif userIn == 3:
                    _ = os.system('cls');
                    print("You examine the witch a little more closely, trying to find any exploitable weaknesses.\n\n");
                    input("Press Enter to roll for Empathy.");
                    plrDieMod, plrDie = RollD20();
                    grylaDieMod, grylaDie = RollD20(mod = -2);
                    print("\nYou rolled " + str(plrDieMod) + " (" + str(plrDie) + "+0)");
                    print("Grÿla rolled " + str(grylaDieMod) + " (" + str(grylaDie) + "-2)");
                    if plrDieMod > grylaDieMod: #"If the player wins" is annoyingly vauge for a description that specified the exact operator ('>') only 3 sentences before
                        KillGryl("Looking more closely, you notice that Gryla is unusually unwell. You ask her about her health, and she suddenly softens, claiming that she's been cursed to stay in the mortal plane, bound to cruelly haunt adventurers for centuries.\nYou know some curse-breaking! You offer to help, and she begrudgingly accepts.\nThe curse proves difficult to defeat, but you manage, and Gryla starts to fade, giving apologies for all the harm she's caused.");
                    else:
                        print("Drats! You can't find anything particularly weak about her. You figure your best bet is to attack before she can get the upper hand.");
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
                    print("(!) You missed horribly! Grÿla's using this chance to heal!");
                    grylaHealth = 2;
                elif plrDieMod >= 12: #Hit
                    print("You hit her!");
                    grylaHealth -= 1;
                else: #Miss
                    print("You missed.");
                #Gryla's Turn
                if grylaHealth <= 0: #End fight
                    KillGryl("\nAs you hit Grÿla, she crumples on the ground, defeated.\nShe groans, and slowly fades to dust.");
                elif plrDie > 1: #Gryla attack (If not heal)
                    print("\nGrÿla Goes in for the attack!");
                    grylaDieMod, grylaDie = RollD20(mod = -4);
                    print("She rolled " + str(grylaDieMod) + " (" + str(grylaDie) + "-4)");
                    if grylaDieMod > 12:
                        print("She hits you!\n");
                        playerHealth -= 1;
                    else:
                        print("She Misses!\n");
                    pause();
                if playerHealth <= 0:
                    GameOver("You fall to the ground, bested by Grÿla's magical might.\nIn a panic, you scramble up the stairs and out the hut, but you're distraught knowing she will continue to haunt you.\nGAME OVER");
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