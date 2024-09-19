from core import*
from input_handlers import*

#read user inputs, produce all air scrubber combinations, output results
def main():
    originalCombos = [] #store all combos that are less than or equal to target cfm(includes [])
    allCombos = [] #store all combinations that meet the air purity requirements(originalCombos with overflows added)
    no_subset_combos = [] #store all combinations that meet air purity requirements without combo subsets/redundancies

    # Testing parameter assignments
    testMode = True;
    if testMode:
        roomLength = 20
        roomWidth = 30
        roomHeight = 50
        airChanges = 3
        scrubbers = [AirScrubber("xpower", 300, 2, 5, -1), AirScrubber("pheonix", 500, 10, 1, -1), AirScrubber("thor", 900, 10, 3, 50)]
        
    else:
        scrubbers = get_scrubber_inputs()
        print([scrubber.no_weight for scrubber in scrubbers], [scrubber for scrubber in scrubbers])
        roomLength, roomWidth, roomHeight, airChanges = get_calculation_inputs()
        
        
       
    cfmTarget = calculate_target_cfm(roomLength, roomWidth, roomHeight, airChanges)
    prepare_output(originalCombos, allCombos, no_subset_combos, cfmTarget, scrubbers)
    display_output(no_subset_combos, airChanges, cfmTarget, scrubbers)

if __name__ == "__main__":
    main()
    


#to-do
#make some sort of output filtering(only display 1 of the valid outputs, or show the most efficient output) main priority
#maybe seperate get inputs into a 2 methods, get variables and get scrubbers to reduce method size
#remove magic numbers
#could change the error string to a static string like invalid input please type yes or no
#fix meter to feet
#change input reading strings to make it more readible

#could try and deal with cases like thor = 700, phoenix = 200, [thor, thor, thor, thor, thor, pheonix] is valid for cfm total of 3600
#but [pheonix, thor, thor, thor, thor, thor] is also valid, but one is not needed due to redundancy