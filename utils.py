from input_handlers import*


class AirScrubber:
    amount = 0
    def __init__(self, scrubber_type, cfm_value, amount):
        self.scrubber_type = scrubber_type
        self.cfm_value = int(cfm_value)
        self.amount = int(amount) # The amount of a specific scrubber a user has
        
    def set_flag(self, flag):
        self.flag = flag

    def set_amount(self, amount):
        self.amount = int(amount)

    def __repr__(self):
        return self.scrubber_type

# Check if value is a number
def is_number(s):
    try:
        float(s)
        return True # Is number
    except ValueError:
        return False # Is not number

# Check if value is an integer 
def is_int(s):
    try:
        int(s)
        return True # Is integer
    except ValueError:
        return False # Is not integer
    
# Sum all cfm values of scrubbers in a combo list
def sum_combos_cfm_values(combo):
    total = 0
    for scrubber in combo:
        total += scrubber.cfm_value
    return total

# Convert room dimensions from meters to feet
def meter_to_feet(room_length, room_width, room_height, units):
    if units == "m":
        room_length *= 3.28084
        room_width *= 3.28084
        room_height *= 3.28084
    return room_length, room_width, room_height

# Print all element of a list in counted types format
def print_output_combo(lst, empty_string, heading_string):
    i = 0
    if(heading_string):
        print("\n" + heading_string) #print the combo list description eg ALL PRICE SORTED COMBOS(newline to seperate from previous output)
    else:
        print()# Print newline character if no title is passed to seperate different combo outputs
        
    from core import count_types
    if lst:
        for combo in lst: #could change from count_types(lst) to print(count_types(element))
            print(combo, totaling_sort(lst[i], "price"), totaling_sort(lst[i], "weight"),) #extra fields are for testing
            i += 1
    else:
        print(empty_string) # Print specified error message if there are no combos in list

def all_have_attribute(scrubbers, attribute):
    return all(getattr(scrubber, attribute) != -1 for scrubber in scrubbers)

# Sort combo lists based various metrics
def sort_outputs(lst, scrubbers):
    from utils import yes_no_check
    sorting_options_dict = {
        "amount": {"prompt": "sort on AMOUNT?", 
            "error": "", 
            "key": lambda x: len(x), 
            "heading": "SORTED ON AMOUNT",
            "can_sort": True # Always allow amount sorting
         }, 
        "weight": {"prompt": "sort on WEIGTH?", 
            "error": "", 
            "key": lambda x: totaling_sort(x, "weight"), 
            "heading": "SORTED ON WEIGHT",
            "can_sort": all_have_attribute(scrubbers, "weight") # Only allow price sorting if no scrubbers have a skipped weight field
         }, 
        "price": {"prompt": "sort on PRICE?", 
            "error": "", 
            "key": lambda x: totaling_sort(x, "price"), 
            "heading": "SORTED ON PRICE",
            "can_sort": all_have_attribute(scrubbers, "price") # Only allow price sorting if no scrubbers have a skipped price field
         }, 

        # Add more sorting options here as needed
    }
     
    type_string = "/".join(sorting_options_dict.keys())
    if yes_no_check("Would you like to sort output combos? ", "Invalid input, please type yes or no "):
        sort_strings = input(f"Please select sorting criteria from {type_string}, seperated by commas: ") # Read desired user sorts
        
        selected_sorts = [
            sort_types.strip() for sort_types in sort_strings.split(",")
            if sort_types.strip() in sorting_options_dict.keys()
        ] # Only accept a sort into selected_sorts if it is a valid sorting option
        
        # Apply all valid sorting options and print output
        for sort in selected_sorts:
            print(sort)
            option = sorting_options_dict.get(sort)
            
            # Re entering skipped input logic
            if not option["can_sort"]: # Check if has skipped any of the fields pertaining to the current sort in selected_sorts
                print(f"You have not assigned a {sort} value to all inputted air scrubbers!")
                
                if yes_no_check("Would you like to add the skipped value: ", "incorrect input: "): # Allow user to input previously skipped field 
                    for skipped_scrubbers in [scrubber for scrubber in scrubbers if getattr(scrubber, sort) == -1]:
                        setattr(skipped_scrubbers, sort, get_valid_input(f"Enter {skipped_scrubbers.scrubber_type} {sort} value: ", True, False))   # Assign new input to previously skipped field
                        option["can_sort"] = True
            
            # Sorting logic
            if(option is not None and option["can_sort"]):
                print_output_combo(sorted(lst, key=option["key"]), "", option["heading"])

# Sort combos based on a totals of scrubber values eg weight or price
def totaling_sort(combo, sort_type):
    total = 0
    for scrubber in combo:
        total += getattr(scrubber, sort_type)
    return total

# Check if any inputs have been skipped and reject those that have 

    
            


#to-do, add methods for sorting based on price and weight now that we have these vairable, for now if any scrubbers hava skipped
#weight or price say to the user that, that sorting criteria is not availbale since fields are missing, then just apply those sorting
#then add those functions to the dictionary where the lambda function normally is and everything should work
#add option to sort by all criterias by inputting "all" when prompted to select sorting criterias
#adjust all yes_no_check error strings, maybe just make it a static string
#add input testing to not allow negative numbers
#add filtering to just print out firx x outputs
#add logic to deal with people typing yes to re entering weight values but not wanting to and deal with all those edge cases
#convert to application, lots of things will probably need to be reworked anyways, could start new repo if i want, just leave program in 
#usable command line state then move on dont need perfection

#print amount, price, weight next to combo in output just for users clarity and selection
#with weight or price just return heighest

    
    
    