from air_scrubber_functions import *

#read user inputs, produce all air scrubber combinations, output results
def main():
    finalPrintValues = []
    scrubberCombos = []
    final = []
    allCombos = []
    

    #testing parameter assignment
    testMode = True;
    if testMode:
        roomLength = 50
        roomWidth = 20
        roomHeight = 20
        airChanges = 4
        scrubbers = [airScrubber("xpower", 500, 3), airScrubber("pheonix", 600, 2), airScrubber("thor", 700, 1)]
        scrubbersCfms = [500, 600, 700]
    else:
        roomLength, roomWidth, roomHeight, airChanges, scrubbers, scrubbersCfms = getInputs()
       
    #program
    cfmTarget = calculateTargetCfm(roomLength, roomWidth, roomHeight, airChanges)
    prepareOutput(scrubberCombos, final, allCombos, scrubbersCfms, cfmTarget, scrubbers, finalPrintValues)
    displayOutput(allCombos, airChanges, cfmTarget, scrubbers)

if __name__ == "__main__":
    main()
    


#to-do

#remove magic numbers
#make some sort of output filtering(only display 1 of the valid outputs, or show the most efficient output)
#ermove more redundancies
#maybe seperate get inputs into a 2 methods, get variables and get scrubbers to reduce method size
#change function names and comments potentially