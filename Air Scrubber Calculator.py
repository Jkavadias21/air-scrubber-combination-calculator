class airScrubber:
    # Constructor method (initializer)
    def __init__(self, scrubberType, cfmValue):
        self.scrubberType = scrubberType
        self.cfmValue = cfmValue
        

    def setFlag(self, flag):
        self.flag = flag

    def __str__(self):
        return f"({self.scrubberType})"
        
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

#filter out undesired combos
def filterAirScrubbers(scrubberCombos, cfmTarget, original):
    finalArray = []
    toRemove = []
    
    for scrubberCombo in scrubberCombos:
        #add combo from original array that have a cfm sum equal to the target cfm to a removal list and a final list
        if sum(scrubberCombo) == cfmTarget:
            finalArray.append(scrubberCombo)
            toRemove.append(scrubberCombo)
        #add combo thats more than one AS away from target to removal list
        if cfmTarget - sum(scrubberCombo) >= max(original):
            toRemove.append(scrubberCombo)
    
    #remove undesired combos
    for items in toRemove:
        scrubberCombos.remove(items)

    #--------------testing ----------------
    toRemove = list(filter(None, toRemove))
    scrubberCombos = list(filter(None, scrubberCombos))
    print("removed      ", toRemove)
    print("after removal", scrubberCombos)
    #--------------testing ----------------
    
    #return array with cfm sums equal to target cfm
    return finalArray

#encode overflow scrubbers into combos
def addOverflowScrubber(scrubberCombos, original):
    i = 1
    for scrubberCombo in scrubberCombos:
        scrubberCombo.append("")
        integers = [x for x in scrubberCombo if isinstance(x, int)]

        #represent overflow scrubbers as strings in the final slot of combo array in a (AS1/AS2) format
        for cfm in original:
            for scrubber in scrubbers:
                if cfm == scrubber.cfmValue:
                    tempCfm = scrubber.scrubberType
            
            if (sum(integers) + cfm > cfmTarget) and (i < len(original)):
                scrubberCombo[-1] = scrubberCombo[-1] + str(tempCfm) + '/'
            elif (sum(integers) + cfm > cfmTarget):
                scrubberCombo[-1] = scrubberCombo[-1] + str(tempCfm)
            i += 1
        i = 1 

scrubbersCfms = []

#list to store all scrubbers the user has at their facility
scrubbers = [airScrubber("pheonix", 485), airScrubber("xPower", 650), airScrubber("thor", 1000)]
#list that stores all the users air scrubbers cfm values 
for scrubber in scrubbers:
    scrubbersCfms.append(scrubber.cfmValue)


cfmTarget = 2000
scrubberCombos = findScrubberCombos(scrubbersCfms, cfmTarget)

#-----testing------
print( "original     ", scrubberCombos)

final = filterAirScrubbers(scrubberCombos, cfmTarget, scrubbersCfms)
addOverflowScrubber(scrubberCombos, scrubbersCfms)
final = final + scrubberCombos

print("final        ", final)

#convert cfm values in combo lists to air scrubber name strings
for i in range(len(final)):
    for j in range(len(final[i])):
        for scrubber in scrubbers:
            if final[i][j] == scrubber.cfmValue:
                final[i][j] = scrubber.scrubberType
final = sorted(final, key=len)

totalValues = []
finalPrintValues = []
for i in range(len(final)):
    total = 0
    split = []
    finalString = []
    toRemove = []
    sumList = []
    tempPrintValues = []
    totalList = []

    print(final[i], "final")
    for j in range(len(final[i])):
        if '/' in final[i][-1]:
            finalString = final[i][-1]
            split = finalString.split("/")
            totalList = final[i] + split
        else:
            split = final[i]
            totalList  = split
        
        
        
        for element in totalList:
            if '/' in element:
                toRemove.append(element)

        for item in toRemove:
            totalList.remove(item)
        toRemove = []

    print(totalList, "total list")
    for scrubber in scrubbers:
        for scrubberName in totalList:
            if scrubberName == scrubber.scrubberType:
                total = total + scrubber.cfmValue
    totalValues.append(total)

    print(total, "total--------------")
    
    #print(split, "split") 

    
    newArray = []
    tempFinal = final[i][:]
    print(final, "---jhfdgsalkjfsaghlkfdsghfdskjghfdskghfdsgfdslkglkhfdsgfslikjfkhdgfdsafdsajmfdsajh")
    print(tempFinal)
    if split == final[i]:
        for scrubber in scrubbers:
            for j in range(len(tempFinal)):
                if scrubber.scrubberType == tempFinal[j]:
                    tempFinal[j] = scrubber.cfmValue
        finalPrintValues.append(sum(tempFinal))
            
    else: 
        for k in range(len(split)):
            for scrubber2 in scrubbers:
                if split[k] == scrubber2.scrubberType:
                    newArray = split[:k] + split[k + 1:]
                    for z in range(len(newArray)):
                        for scrubber2 in scrubbers:
                            if newArray[z] == scrubber2.scrubberType:
                                newArray[z] = scrubber2.cfmValue
                    tempPrintValues.append(total - sum(newArray))
                    print(split, split[k], newArray, "split----------", tempPrintValues, k, len(split))
                    if k == len(split) - 1:
                        print("here")
                        finalPrintValues.append(tempPrintValues)


                
            #print(newArray, "new 2")
            
            
            
            #print(newArray, "new")
            
            #print(printValues, "--print values")
                

            

        
        sumList = []
        
        total = 0
        #print(totalList, "total list")
        #print(totalValues, "----------------------------------------------")
    




i = 0

for combo in final:
    if isinstance(finalPrintValues[i], int):
        print(combo, f"[{finalPrintValues[i]}]")
        i += 1
    else:
        print(combo, finalPrintValues[i])
        i += 1
    
    

#make function that converts all combos into digits

    

