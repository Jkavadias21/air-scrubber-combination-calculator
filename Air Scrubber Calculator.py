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

#def print_sums(array_of_arrays):
    for sub_array in array_of_arrays:
        array_sum = sum(sub_array)
        print(f"Sum of {sub_array} is {array_sum}")



def findCloseCombos(scrubberCombos, cfmTarget):
    finalArray = []
    toRemove = []
    
    #removes combo from original array that have a cfm sum equal to the target cfm
    for scrubberCombo in scrubberCombos:
        if sum(scrubberCombo) == cfmTarget:
            finalArray.append(scrubberCombo)
            toRemove.append(scrubberCombo)
        if cfmTarget - sum(scrubberCombo) >= 3:
            toRemove.append(scrubberCombo)

    for items in toRemove:
        scrubberCombos.remove(items)
            
            
    print(toRemove, "removed")        
    print(scrubberCombos, "after removal")
    '''
    for scrubberCombo in scrubberCombos:
        if -1 not in scrubberCombo:
            if cfmTarget - sum(scrubberCombo) < 1:
                scrubberCombos.append(scrubberCombo + [1000,-1])
                scrubberCombos.append(scrubberCombo + [2000,-1])
                scrubberCombos.append(scrubberCombo + [3000,-1])
            if cfmTarget - sum(scrubberCombo) < 2 and cfmTarget - sum(scrubberCombo) > 1:
                scrubberCombos.append(scrubberCombo + [2000])
                scrubberCombos.append(scrubberCombo + [3000,-1])
            if cfmTarget - sum(scrubberCombo) < 3 and cfmTarget - sum(scrubberCombo) > 2:
                scrubberCombos.append(scrubberCombo + [3000,-1])
    '''
    return finalArray
            
        
        
        

scrubbersCfms = [1,2]
cfmTarget = 5
scrubberCombos = findScrubberCombos(scrubbersCfms, cfmTarget)
print(scrubberCombos, "original")
final = findCloseCombos(scrubberCombos, cfmTarget)
#print(print_sums(scrubberCombos))

print("\n", scrubberCombos, "original")
print("\n\n", final, "final")

##calculates all combinations less than or equal to target just need to filter out and print