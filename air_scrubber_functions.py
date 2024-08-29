from collections import Counter

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

# Call all functions required to generate combination lists
def prepare_output(original_combos, all_combos, cfm_target, scrubbers):
    # Clear existing lists to ensure they start empty
    original_combos.clear()
    all_combos.clear()

    # Extend to change original array instead of just changing it locally
    original_combos.extend(find_scrubber_combos(scrubbers, cfm_target)) # Find all combination with cfm total less than target cfm
    all_combos.extend(add_overflow_all(original_combos, scrubbers, cfm_target))  # Generate array containing every combination (contains duplicates)

    # Testing
    print("less than cfm combos", original_combos)
    print("added overflows", add_overflow_all(original_combos, scrubbers, cfm_target))

# Display all combinations and calculations
def display_output(all_combos, air_changes, cfm_target, scrubbers):
    print("\n -----FINAL OUTPUT-----")
    print("\n" + f"To maintain {air_changes} air changes an hour, a total cfm of {cfm_target:.{5}}({cfm_target*0.000471947:.{3}}m³/s) is required" + "\n")
    
    print("ALL COMBINATIONS")
    all_combos = remove_duplicates(all_combos)
    for combo in count_types(all_combos):
        print(combo)
    
    print("\nALL VALID COMBINATIONS")
    valid_combos = count_types(remove_combos(all_combos, scrubbers)) # Contains all combos that meet the users stock
    for valid in valid_combos:
        print(valid)

# Generate a list of combinations that have a cfm total less than or equal to target cfm
def find_scrubber_combos(scrubbers, cfm_target):
    def backtrack(start, path, total):
        if total <= cfm_target:
            result.append(path)
        for i in range(start, len(scrubbers)):
            if total + scrubbers[i].cfm_value <= cfm_target:
                backtrack(i, path + [scrubbers[i]], total + scrubbers[i].cfm_value)
    
    result = []
    backtrack(0, [], 0)
    print(result, "this is the result")
    return result

# Return a list of all combinations that meet purity requirements(contains duplicates)
def add_overflow_all(scrubber_combos, scrubbers, cfm_target):
    all_combos = []
    for combo in scrubber_combos:
        if combo != [cfm_target]:
            for scrubber in scrubbers:
                # Add overflow scrubber only if the combo is one scrubber away from exceeding the cfm target
                if (sum_combos_cfm_values(combo) + scrubber.cfm_value > cfm_target and
                    scrubber.cfm_value != cfm_target and
                    sum_combos_cfm_values(combo) != cfm_target):
                    overflowed_combo = combo + [scrubber]
                    all_combos.append(overflowed_combo)
        else:
            all_combos.append([cfm_target])
    return all_combos

# Sum all cfm values of scrubbers in a combo list
def sum_combos_cfm_values(combo):
    total = 0
    for scrubber in combo:
        total += scrubber.cfm_value
    return total

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
    
# Read in valid inputs from user
def get_valid_input(prompt, is_int=False):
    while True:
        try:
            value = input(prompt)
            if is_int:
                value = int(value)
            else:
                value = float(value)
            return value
        
        except ValueError:
            if is_int:
                print("Invalid input. Please enter a valid integer.")
            else:
                print("Invalid input. Please enter a valid number.")

# Store user inputs pertaining to their current air scrubbers and stock
def get_scrubber_inputs():
    scrubbers = []
    scrubber_types = set()
    
    while True:
        # Make sure any air scrubber type is only entered once
        while True:
            scrubber_type = input("Enter air scrubber type: ")
            if scrubber_type in scrubber_types:
                print("This air scrubber type has already been inputted. Please enter a new one.")
            else:
                scrubber_types.add(scrubber_type)
                break
        
        scrubber_cfm = get_valid_input("Enter air scrubber CFM rating: ")
        scrubber_amount = get_valid_input("Enter air scrubber amount: ", True)
        scrubbers.append(AirScrubber(scrubber_type, scrubber_cfm, scrubber_amount))

        # Check if user wants to add more air scrubbers or not
        while True:
            more_inputs = input("Do you want to add another air scrubber? (yes/no): ").strip().lower()
            if more_inputs in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        if more_inputs != 'yes':
            break
        print(scrubbers, "hehehe")
    return scrubbers # Return list containing users air scrubber objects
    
# Assign user inputs pertaining to cfm calculations
def get_calculation_inputs():
    while True:
        units = input("Enter m for meters or f for feet: ").lower()
        if units == 'm' or units == 'f':
            break
        # For testing
        elif units == 's':
            return 50, 50, 20, 1
    # Check and assign valid user volume and air change inputs
    while True:
        try:
            room_length = get_valid_input("Enter room length: ")
            room_width = get_valid_input("Enter room width: ")
            room_height = get_valid_input("Enter room height: ")
            air_changes = get_valid_input("Enter required air changes:", True)
            print(f"Length: {room_length}, Width: {room_width}, Height: {room_height}, Air Changes: {air_changes}")
            break  # Exit the loop if all inputs are valid
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    # Perform required unit conversions
    room_length, room_width, room_height = meter_to_feet(room_length, room_width, room_height, units)
    
    return room_length, room_width, room_height, air_changes

# Convert room dimensions from meters to feet
def meter_to_feet(room_length, room_width, room_height, units):
    if units == "m":
        room_length *= 3.28084
        room_width *= 3.28084
        room_height *= 3.28084
    return room_length, room_width, room_height

# Calculate cfm value required to meet air purity standards
def calculate_target_cfm(room_length, room_width, room_height, air_changes):
    # Calculate volumes
    room_volume = room_length * room_width * room_height
    total_volume = room_volume * float(air_changes)
    # Return target cfm
    return total_volume / 60

# Return a list of combos without any combo duplicates 
def remove_duplicates(combo_all):
    seen = set()
    unique_arrays = []

    for combo in combo_all:
        sorted_combo = sorted(combo, key=lambda x: x.cfm_value)
        sorted_tuple = tuple(sorted_combo)  # Sort the array and convert to tuple
        if sorted_tuple not in seen:
            seen.add(sorted_tuple)  # Add the tuple to the set
            unique_arrays.append(combo)  # Add the original array to the result

    return unique_arrays

# Return list of combinations that do not exceed users stock
def remove_combos(all_combos, scrubbers):
    scrubber_dict = {}
    valid_combos = []

    # Initialise scrubber dict
    for scrubber in scrubbers:
        scrubber_dict[scrubber.scrubber_type] = 0

    # Correspond each scrubber with the amount of that scrubber ("scrubberType": "scrubberTypeAmount")
    for combo in all_combos: 
        for scrubber in combo:
            scrubber_dict[scrubber.scrubber_type] += 1 
        
        valid = True
        for scrubber in scrubbers: 
            if scrubber_dict[scrubber.scrubber_type] > scrubber.amount:
                valid = False # Disregard combos that have more air scrubbers than users stock
                break
        if valid:
            valid_combos.append(combo) # Accept combos that have air scubber amounts less than or equal to users stock
            
        for scrubber in scrubbers:
            scrubber_dict[scrubber.scrubber_type] = 0 #reset dict
    
    return valid_combos

# Represent combos in [2 as1] format instead of [as1, as1]
def count_types(lst):
    final_list = []
    for combo in lst:
        counts = Counter(combo)
        result = []
        for scrubber in combo:
            if counts[scrubber] > 0:
                result.append(f"{counts[scrubber]} {scrubber}")
                counts[scrubber] = 0  # Ensure we only add the formatted string once for each unique scrubber
        final_list.append(result)
    return final_list