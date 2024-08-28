from collections import Counter
class airScrubber:

    amount = 0
    
    def __init__(self, scrubberType, cfmValue, amount):
        self.scrubberType = scrubberType
        self.cfmValue = int(cfmValue)
        self.amount = int(amount)
        
    def setFlag(self, flag):
        self.flag = flag

    def setAmount(self, amount):
        self.amount = int(amount)

    def __repr__(self):
        return f'scruber(type={self.scrubberType}, cfm={self.cfmValue}, amount={self.amount})'

#returns list of all combinations of airscrubber that cfms sum to the target cfm or less
def findScrubberCombos(scrubbersCfms, cfmTar):
    def backtrack(start, path, total):
        if total <= cfmTar:
            result.append(path)
        for i in range(start, len(scrubbersCfms)):
            if total + scrubbersCfms[i] <= cfmTar:
                backtrack(i, path + [scrubbersCfms[i]], total + scrubbersCfms[i])
    
    result = []
    scrubbersCfms.sort()  # Ensure scrubbersCfms is sorted
    backtrack(0, [], 0)
    return result

#add overflow scrubbers to all combinations that are one air scrubber away from cfm target
def addOverFlowAll(scrubberCombos, scrubbers, cfmTarget):
    allCombos = []
    for combo in scrubberCombos:
        if(combo != [cfmTarget]):
            for scrubber in scrubbers:
                #add overflow scrubber only if the combo is one scrubber away from exeeding the cfm target
                if((sum(combo) + scrubber.cfmValue > cfmTarget) and (scrubber.cfmValue != cfmTarget) and (sum(combo) != cfmTarget)):
                    overflowedCombo = combo + [scrubber.cfmValue]
                    allCombos.append(overflowedCombo)
        else:
            allCombos.append([int(cfmTarget)])
    return allCombos

#convert 2D list of cmf values to list of air scrubber name strings
def cmfToName2D(arr2D, scrubbers):
    for i in range(len(arr2D)):
        for j in range(len(arr2D[i])):
            for scrubber in scrubbers:
                if arr2D[i][j] == scrubber.cfmValue:
                    arr2D[i][j] = scrubber.scrubberType

#convert list from name to cmf values
def nameToCmf1D(arr1D, scrubbers):
        for scrubber in scrubbers:
            for j in range(len(arr1D)):
                if scrubber.scrubberType == arr1D[j]:
                    arr1D[j] = scrubber.cfmValue

#check if a value is a number or not
def isNumber(s):
    try:
        float(s)
        #return true if value is a number
        return True
    except ValueError:
        #return false if value is not a number
        return False
    
#check if a value is an int or not
def isInt(s):
    try:
        int(s)
        #return true if value is an int
        return True
    except ValueError:
        #return false if value is not an int
        return False
    
#function to get a valid input from user
def getValidInput(prompt, isInt = False):
    while True:
        try:
            value = input(prompt)
            if isInt:
                value = int(value)
            else:
                value = float(value)
            return value
        
        except ValueError:
            if isInt:
                print("Invalid input. Please enter a valid integer.")
            else:
                print("Invalid input. Please enter a valid number.")

#assign validated user inputs to respective variables
def getInputs():
    scrubbers = []
    scrubbersCfms = []
    scrubberTypes = set()
    #read in and store users air scrubbers in array
    while True:
        #make sure any air scrubber type is only entered once
        while True: 
            scrubberType = input("Enter air scrubber type: ")
            if scrubberType in scrubberTypes:
                    print("This air scrubber type has already been inputted. Please enter a new one.")
            else:
                scrubberTypes.add(scrubberType)
                break
        
        scrubberCfm = getValidInput("Enter air scrubber CFM rating: ")
        scrubberAmount = getValidInput("Enter air scrubber amount: ", True)
        scrubbers.append(airScrubber(scrubberType, scrubberCfm, scrubberAmount))

        #check if user wants to add more air scrubbers or not
        while True:
            moreInputs = input("Do you want to add another air scrubber? (yes/no): ").strip().lower()
            if moreInputs in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        if moreInputs != 'yes':
            break

    #array that stores all the users air scrubbers cfm values 
    scrubbersCfms.clear()  # clear the list before adding new values
    for scrubber in scrubbers:
        scrubbersCfms.append(scrubber.cfmValue)
    
    #check and assign valid user unit inputs
    while True:
        units = input("Enter m for meters or f for feet: ").lower()
        if units == 'm' or units == 'f':
            break
        #for testing
        elif units == 's':
            return 50, 50, 20, 1, scrubbers, scrubbersCfms
    #check and assign valid user volume and air changes inputs
    while True:
        try:
            roomLength = getValidInput("Enter room length: ")
            roomWidth = getValidInput("Enter room width: ")
            roomHeight = getValidInput("Enter room height: ")
            airChanges = getValidInput("Enter required air changes:", True)
            print(f"Length: {roomLength}, Width: {roomWidth}, Height: {roomHeight}, Air Changes: {airChanges}")
            break  # Exit the loop if all inputs are valid
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    #perform required unit conversions
    roomLength, roomWidth, roomHeight = meterToFeet(roomLength, roomWidth, roomHeight, units)
    
    return roomLength, roomWidth, roomHeight, airChanges, scrubbers, scrubbersCfms 


#convert dimensions from meters to feet
def meterToFeet(roomLength, roomWidth, roomHeight, units):
    if units == "m":
        roomLength = roomLength*3.28084
        roomWidth = roomWidth*3.28084
        roomHeight = roomHeight*3.28084
    return roomLength, roomWidth, roomHeight

#calculate the required cfm for desired air changes
def calculateTargetCfm(roomLength, roomWidth, roomHeight, airChanges):
    #calculate volumes
    roomVolume = roomLength*roomWidth*roomHeight
    totalVolume = roomVolume*float(airChanges)
    #return target cfm
    return totalVolume/60

def removeDuplicates(comboAll):
    seen = set()
    uniqueArrays = []

    for combo in comboAll:
        sortedTuple = tuple(sorted(combo))  # Sort the array and convert to tuple
        if sortedTuple not in seen:
            seen.add(sortedTuple)  # Add the tuple to the set
            uniqueArrays.append(combo)  # Add the original array to the result

    return uniqueArrays

#create an array only containing combinations that a valid for the users stock
def removeCombos(allCombos, scrubbers):
    scrubberDict = {}
    validCombos = []

    for scrubber in scrubbers:
        scrubberDict[scrubber.scrubberType] = 0

    for combo in allCombos:
        for asType in combo:
            for scrubber in scrubbers:
                if scrubber.scrubberType == asType:
                    scrubberDict[scrubber.scrubberType] += 1
        
        valid = True
        for scrubber in scrubbers:
            if scrubberDict[scrubber.scrubberType] > scrubber.amount:
                valid = False
                break
        if valid:
            validCombos.append(combo)
            
        for scrubber in scrubbers:
            scrubberDict[scrubber.scrubberType] = 0
    return validCombos

#convert cominations from [a1,a1] format to [2 a1] format
def countTypes(list):
    finalList = []
    for combo in list:
        counts = Counter(combo)
        result = []
        for scrubber in combo:
            
            if counts[scrubber] > 0:
                result.append(f"{counts[scrubber]} {scrubber}")
                counts[scrubber] = 0  # Ensure we only add the formatted string once for each unique scrubber
        finalList.append(result)
    return finalList

#call all the required functions to calculate combinations and produce the output arrays(filtering, overflow and name to cmf conversions)
def prepareOutput(scrubberCombos, final, allCombos, scrubbersCfms, cfmTarget, scrubbers, finalPrintValues):
    #clear existing lists to ensure they start empty
    scrubberCombos.clear()
    final.clear()
    allCombos.clear()

    #extend to change original array instead of just changing it locally
    scrubberCombos.extend(findScrubberCombos(scrubbersCfms, cfmTarget)) #find all combination with cfm total less than target cfm
    
    print("less than cfm combos", scrubberCombos)
    
    #final.extend(filterAirScrubbers(scrubberCombos, cfmTarget, scrubbersCfms)) #filter out combos that are not one air scrubber away from the target cfm
    
    print( "added overflows", addOverFlowAll(scrubberCombos, scrubbers, cfmTarget))
    
    allCombos.extend(addOverFlowAll(scrubberCombos, scrubbers, cfmTarget))  #generate array containing every combination(not slash format)
   
    
    #cmfToName2D(final, scrubbers) #convert combos from cfm values to scrubber types
    

#display all combos and outputs
def displayOutput(allCombos, airChanges, cfmTarget, scrubbers):
    
    print("\n -----FINAL OUTPUT-----")
    
    print("\n" + f"To maintain {airChanges} airchanges an hour, a total cmf of {cfmTarget:.{5}}({cfmTarget*0.000471947:.{3}}m3/s) is required" + "\n")
    
    print("ALL COMBINATIONS")
    cmfToName2D(allCombos, scrubbers)
    allCombos = removeDuplicates(allCombos) #allCombos in every combination without duplicates(not slash format)
    
    for combo in countTypes(allCombos):
        print(combo)
    
    validCombos = countTypes(removeCombos(allCombos, scrubbers)) #valid combos are all combos that match users stock
    print("\nALL VALID COMBINATIONS")
    for valid in validCombos:
        print(valid)
