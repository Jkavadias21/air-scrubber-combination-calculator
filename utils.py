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
def print_output_combo(lst, empty_string):
    from core import count_types
    if lst:
        for combo in count_types(lst): #could change from count_types(lst) to print(count_types(element))
            print(combo)
    else:
        print(empty_string)



# Sort combo lists based various metrics
def sort_outputs(lst):
    sorting_options = [
        {"prompt": "Do you want to sort the output from least to most air scrubbers? Please type 'yes' or 'no': ", 
         "error": "Invalid input. Please type 'yes' or 'no': ", 
         "key": lambda x: len(x), 
         "title": "SORTED ON AMOUNT",
         "sort_type": "amount"}, 
        {"prompt": "Do you want to sort the output on weight", 
         "error": "Invalid input. Please type 'yes' or 'no': ", 
         "key": lambda x: len(x), 
         "title": "SORTED ON WEIGHT",
         "sort_type": "weight"}, 

        # Add more sorting options here as needed
    ]

    sort_type_list = [option["sort_type"] for option in sorting_options] # create list of these sorting options, allow user to pick which they want
    #then only loop throught these particular sorting options and sort based on only those
    type_string = "/".join(sort_type_list)
    print(sort_type_list, type_string)

    input(f"select sorting types from {type_string}")

    for option in sorting_options:
        if yes_no_check(option["prompt"], option["error"]):
            print(f"\n{option['title']}")
            print_output_combo(sorted(lst, key=option["key"]), "")
    
    