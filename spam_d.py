import os
import sys
import re

try:
    os.system('clear')

    # Define some variables
    StringToSearch = sys.argv[1]
    WarningStrings = [] # Strings that trigger a warning
    CriticalStrings = [] # Strings that trigger a critical alert
    HelpersArray = ["msgHandle.sh", "critical.strings", "warning.strings"]
    HelpersDirectory = "./helpers/"

    try:
        if sys.argv[2] == '--showdebug':
            ShowDebug = True
        else:
            ShowDebug = False
    except:
        ShowDebug = False

    def warn(warnString):
        os.system(HelpersDirectory + 'msgHandle.sh -w "' + warnString + '"')
    def alert(alertString):
        os.system(HelpersDirectory + 'msgHandle.sh -c "' + alertString + '"')
    def info(infoString):
        os.system(HelpersDirectory + 'msgHandle.sh -i "' + infoString + '"')

    def checkForHelpers():
        HelpersNotFound = 0
        print("--> Running pre checks: Checking for helper scripts...")
        for item in HelpersArray:
            if os.path.isfile(HelpersDirectory + item):
                print('success --> Helper found: ' + item)
            else:
                print('ERR! --> Helper cannot be found: ' + item)
                HelpersNotFound += 1
        if HelpersNotFound == 0:
            print('Well done, all helpers are found! Checks passed. Let\'s move on!')
        else:
            print('ERROR: ' + str(HelpersNotFound) + ' helpers were not found. Please reinstall')
            sys.exit(1)

    def clean(word):
        noDigit = ''.join([i for i in word if not i.isdigit()])
        completelyClean = re.sub(r"[^a-zA-Z0-9]+", ' ', noDigit)
        return completelyClean

    def importStrings():

        print('Importing strings from ' + str(HelpersDirectory) + 'critical.strings')
        critical_f = open(HelpersDirectory + 'critical.strings', 'r') 
        lines = critical_f.readlines() 
        for line in lines:
            if line.strip().startswith("# "):
                pass
            else:
                if line.strip() == '':
                    pass
                else:
                    CriticalStrings.append(line.strip())
        critical_f.close()

        print('Importing strings from ' + str(HelpersDirectory) + 'warning.strings')
        warning_f = open(HelpersDirectory + 'warning.strings', 'r') 
        lines = warning_f.readlines() 
        for line in lines:
            if line.strip().startswith("# "):
                pass
            else:
                if line.strip() == '':
                    pass
                else:
                    WarningStrings.append(line.strip())
        warning_f.close()

    def clearScr():
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')
        

    def showHelp():
        print('spam_d : Detect possible spam by cleaning strings and comparing them to two wordlists.')
        print('Basic Usage: ./spam_d "STRING_TO_SCAN"')
        info("\n-h | --help")
        print('Show this help and exit.')
        info('\n"STRING_TO_SCAN" --showdebug')
        print('Show debug messages (if something goes wrong). WARNING: Gets long for huge pieces of text!')
        sys.exit(0)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        checkForHelpers() # Import modules needed for info()
        clearScr() # Clear screen according to OS
        showHelp()

    checkForHelpers()
    importStrings()

    if ShowDebug:
        print(WarningStrings)
        print(CriticalStrings)

    print('\nAnalysing string provided...')

    StringSplit = StringToSearch.split(' ')
    Sentence = []
    Cleaned = 0
    for item in StringSplit:
        Cleaned += 1
        print('Cleaning ' + str(Cleaned) + ' words of ' + str(len(StringSplit)), end='\r')
        if ShowDebug:
            print('\nWord: ' + str(item))
        itemClean = clean(item)
        if ShowDebug:
            print('Cleaned Variant: ' + itemClean)
        if not itemClean.strip() == '':
            Sentence.append(itemClean)
            Sentence.append(' ')
        if ShowDebug:
            print('Adding to sentence. Current: ' + str(Sentence))
    print('') # stop the \r declared above
    finalString = ''.join(Sentence)
    if ShowDebug:
        print('\n\t--> Original Sentence: ' + StringToSearch)
        print('\t--> Cleaned Sentence: ' + finalString)

    print('\n\nRunning checks...')

    Warnings = 0
    Criticals = 0

    for item in WarningStrings:
        if finalString.__contains__(item):
            warn("The word/phrase '" + str(item) + "' was found in text.")
            Warnings += 1

    for item in CriticalStrings:
        if finalString.__contains__(item):
            alert("The word/phrase '" + str(item) + "' was found in text.")
            Criticals += 1

    print('\nResult: ' + str(Warnings) + ' warnings and ' + str(Criticals) + ' criticals.')

    # WILL EXIT EITHER 1 OR 0 so can be used in script:
    # Return 1 = More than 0 criticals, so bad
    # Return 0 = all good

    # Script may return 1 if there is an execution error, so make sure you test it before relying on it.

    if Criticals != 0:
        sys.exit(1)
    else:
        sys.exit(0)


except KeyboardInterrupt:
    print('\n\n')
    alert('The script was abruptly halted.')
    sys.exit(1)