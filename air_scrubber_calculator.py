from core import*
from input_handlers import*

#read user inputs, produce all air scrubber combinations, output results
def main():
    originalCombos = [] #store all combos that are less than or equal to target cfm(includes [])
    allCombos = [] #store all combinations that meet the air purity requirements(originalCombos with overflows added)
    
    # Testing parameter assignments
    testMode = True;
    if testMode:
        roomLength = 30
        roomWidth = 40
        roomHeight = 30
        airChanges = 6
        scrubbers = [AirScrubber("xpower", 200, 2, -1, 3), AirScrubber("pheonix", 600, 10, 1, -1), AirScrubber("thor", 700, 10, 3, 2)]
        
    else:
        scrubbers = get_scrubber_inputs()
        print([scrubber.no_weight for scrubber in scrubbers], [scrubber for scrubber in scrubbers])
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
#could change the error string to a static string like invalid input please type yes or no
#fix meter to feet