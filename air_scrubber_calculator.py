from air_scrubber_functions import *

#read user inputs, produce all air scrubber combinations, output results
def main():
    originalCombos = [] #store all combos that are less than or equal to target cfm(includes [])
    allCombos = [] #store all combinations that meet the air purity requirements(originalCombos with overflows added)
    
    # Testing parameter assignments
    testMode = True;
    if testMode:
        roomLength = 30
        roomWidth = 20
        roomHeight = 20
        airChanges = 4
        scrubbers = [AirScrubber("xpower", 800, 2), AirScrubber("pheonix", 600, 2), AirScrubber("thor", 700, 1)]
        
    else:
        scrubbers = get_scrubber_inputs()
        roomLength, roomWidth, roomHeight, airChanges = get_calculation_inputs()
        
       
    cfmTarget = calculate_target_cfm(roomLength, roomWidth, roomHeight, airChanges)
    prepare_output(originalCombos, allCombos, cfmTarget, scrubbers)
    display_output(allCombos, airChanges, cfmTarget, scrubbers)

if __name__ == "__main__":
    main()
    


#to-do
#make some sort of output filtering(only display 1 of the valid outputs, or show the most efficient output) main priority
#maybe seperate get inputs into a 2 methods, get variables and get scrubbers to reduce method size
#remove magic numbers