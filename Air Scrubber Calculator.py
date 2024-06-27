
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

#def print_sums(array_of_arrays):
    for sub_array in array_of_arrays:
        array_sum = sum(sub_array)
        print(f"Sum of {sub_array} is {array_sum}")


##call filtering function
def findCloseCombos(scrubberCombos, cfmTarget, original):
    finalArray = []
    toRemove = []
    list = scrubberCombos.copy()
    
    #removes combo from original array that have a cfm sum equal to the target cfm
    for scrubberCombo in scrubberCombos:
        if sum(scrubberCombo) == cfmTarget:
            finalArray.append(scrubberCombo)
            toRemove.append(scrubberCombo)
        if cfmTarget - sum(scrubberCombo) >= 3:
            toRemove.append(scrubberCombo)

    for items in toRemove:
        scrubberCombos.remove(items)
    print (scrubberCombos, "-------------")
    for scrubberCombo in scrubberCombos:
        
        scrubberCombo.append("end")
        integers = [x for x in scrubberCombo if isinstance(x, int)]

        print("this line", scrubberCombo, integers)
        
        
        for cfm in original:
            if sum(integers) + cfm > cfmTarget:
                scrubberCombo[-1] = scrubberCombo[-1] + str(cfm)
                print(sum(integers) + cfm, cfmTarget, "cfm", )
                
                
                    
                
               
        #print (scrubberCombo, cfm, cfmTarget)
                    
        
            
            
    print(toRemove, "removed") 
    print(list, "list")
    print(original, "og")       
    print(scrubberCombos, "after removal")
    return finalArray
            
        
        
        

scrubbersCfms = [1,2,3]
original = [1,2,3]
cfmTarget = 5
scrubberCombos = findScrubberCombos(scrubbersCfms, cfmTarget)
print(scrubberCombos, "original")
final = findCloseCombos(scrubberCombos, cfmTarget, original)
#print(print_sums(scrubberCombos))

print("\n", scrubberCombos, "original")
print("\n\n", final, "final")

##calculates all combinations less than or equal to target just need to filter out and print

#just keep elements that with one addition of any of the cfm values exeed the target(filter out 2 step remaining ones)
# if combo is subset of any other combo get rid of it

# take combo add each cfm to its sum if any of them exeed the target then add that combo example [3] with a goal of 5 if i add 1 (3+1) = 4 < 5 dont add since already registered combo 
#if i add 2 (3+2) = 5 = 5 dont add since this is already a registered combo
#if i ad 3 (3+3) = 6 > 5 add this since it is only 1 step away and exeeds target