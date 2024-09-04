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
    if(heading_string):
        print("\n" + heading_string) #print the combo list description eg ALL PRICE SORTED COMBOS(newline to seperate from previous output)
    else:
        print()# Print newline character if no title is passed to seperate different combo outputs
        
    from core import count_types
    if lst:
        for combo in count_types(lst): #could change from count_types(lst) to print(count_types(element))
            print(combo)
    else:
        print(empty_string)



# Sort combo lists based various metrics
def sort_outputs(lst):
    sorting_options_dict = {
        "amount": {"prompt": "sort on AMOUNT?", 
            "error": "", 
            "key": lambda x: len(x), 
            "heading": "SORTED ON AMOUNT",
         }, 
        "weight": {"prompt": "sort on WEIGTH?", 
            "error": "", 
            "key": lambda x: len(x), 
            "heading": "SORTED ON WEIGHT",
         }, 
        "price": {"prompt": "sort on PRICE?", 
            "error": "", 
            "key": lambda x: len(x), 
            "heading": "SORTED ON PRICE",
         }, 

        # Add more sorting options here as needed
    }

    type_string = "/".join(sorting_options_dict.keys())
    if yes_no_check("Would you like to sort output combos? ", "Invalid input, please type yes or no "):
        sort_strings = input(f"Please select sorting criteria from {type_string}, seperated by commas: ")
        selected_sorts = [sort_types.strip() for sort_types in sort_strings.split(",")]
        

        for sort in selected_sorts:
            option = sorting_options_dict.get(sort)
            if(option is not None):
                print_output_combo(sorted(lst, key=option["key"]), "", option["heading"])
            else:
                print(sort, "is none")
        
            
        
        #for option in sorting_options:
           # if yes_no_check(option["prompt"], option["error"]):
               # print(f"\n{option['title']}")
                #print_output_combo(sorted(lst, key=option["key"]), "")
    

    
    
    