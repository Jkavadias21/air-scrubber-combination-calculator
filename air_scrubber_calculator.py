from air_scrubber_functions import *

def main():
    finalPrintValues = []
    scrubberCombos = []
    final = []
    allCombos = []
    scrubbers = []
    scrubbersCfms = []
    
    readScrubbers(scrubbers, scrubbersCfms)
    
    roomLength, roomWidth, roomHeight, airChanges = getInputs()
    
    cfmTarget = calculateTargetCfm(roomLength, roomWidth, roomHeight, airChanges)
    
    prepareOutput(scrubberCombos, final, allCombos, scrubbersCfms, cfmTarget, scrubbers, finalPrintValues)
    displayOutput(allCombos, final, airChanges, finalPrintValues, cfmTarget, scrubbers)

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
#make callInputReading function to combine all input reading functionality in one place
#make cmf/volume calclation function
#Testing scrubbers = [airScrubber("pheonix", 485), airScrubber("xPower", 650), airScrubber("thor", 1000)]

#check validity of scrubber quantity inputs and scrubber type inputs (important)