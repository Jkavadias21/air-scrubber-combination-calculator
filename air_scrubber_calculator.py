from collections import Counter
from air_scrubber_functions import *

def main():
    finalPrintValues = []
    scrubbersCfms = []
    #list to store all scrubbers the user has at their facility
    scrubbers = [airScrubber("pheonix", 485), airScrubber("xPower", 650), airScrubber("thor", 1000)]
    
    #allows user to input amount of each air scrubber they have independant of scrubber array population
    asAmt = []
    for scrubber in scrubbers:
        scrubber.setAmount(input(f"enter amount of {scrubber.scrubberType} "))
    for scrubber in scrubbers:
        print(scrubber.amount)


    #list that stores all the users air scrubbers cfm values 
    for scrubber in scrubbers:
        scrubbersCfms.append(scrubber.cfmValue)

    units, roomLength, roomWidth, roomHeight, airChanges = getInputs()
    
    roomLength, roomWidth, roomHeight = meterToFeet(roomLength, roomWidth, roomHeight, units)
    
    cfmTarget = calculateTargetCfm(roomLength, roomWidth, roomHeight, airChanges)

    #perform combination finding, cfm total calculations and combination filtering
    scrubberCombos = findScrubberCombos(scrubbersCfms, cfmTarget)
    final = filterAirScrubbers(scrubberCombos, cfmTarget, scrubbersCfms)
    allCombos = final + addOverFlowAll(scrubberCombos, scrubbersCfms, scrubbers, cfmTarget)
    #final originally is all combos who exactly equal the goal
    addOverflowScrubber(scrubberCombos, scrubbersCfms, scrubbers, cfmTarget)
    #final below is all combos
    final = final + scrubberCombos
    print(final)
    cmfToName2D(final, scrubbers)
    
    #sort output from least elements to most elements
    #final = sorted(final, key=len)
    
    getCmfSums(finalPrintValues, final, scrubbers)

    #output air scrubber combinations and cmf total
    i = 0
    print("\n -----FINAL OUTPUT-----")
    #print(f"Length: {roomLength}, Width: {roomWidth}, Height: {roomHeight}, Air Changes: {airChanges}, Units: {units}, CFM: {cfmTarget}")
    finalList = []
    
    #show quantity of airscrubber in output([as1, as1] -> [2 as1])
    for combo in final:
        counts = Counter(combo)
        result = []
        for scrubber in combo:
            if containsSlash(scrubber):
                result.append(scrubber)
            else:
                if counts[scrubber] > 0:
                    result.append(f"{counts[scrubber]} {scrubber}")
                    counts[scrubber] = 0  # Ensure we only add the formatted string once for each unique scrubber
        finalList.append(result)

    print("\n" + f"To maintain {airChanges} airchanges an hour, a total cmf of {cfmTarget:.{5}}({cfmTarget*0.000471947:.{3}}m3/s) is required" + "\n")
    
    for combo in finalList:
        if isinstance(finalPrintValues[i], int):
            print(combo, f"[{finalPrintValues[i]}]")
            i += 1
        else:
            print(combo, finalPrintValues[i])
            i += 1

    print("\n ALL COMBOS")
    
    #print every single combination
    cmfToName2D(allCombos, scrubbers)
    print(allCombos)
    

    allCombos = removeDuplicates(allCombos)
    validCombos = removeCombos(allCombos, scrubbers)
    for valid in validCombos:
        print(valid, "here")

                
if __name__ == "__main__":
    main()
    


#to-do
#add dynamic air scrubber adding from user
#add m^3/s 
#add target cfm and cms to output
#remove magic numbers
#instead of printing [a,b,b,b, a/b] print [a, 2*b]
#remove extra element at the start 
#remove duplicates could have an option to represent as is, or seperate all into seperate lists, then remove duplicates and sort by price
#sort by each as type so group all xpower 1 xpower 2 xpower 3 xpower will be listed based on price then in a different column do other as
#could have search function to verify combination is valid
#add quantities for all