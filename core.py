from collections import Counter
from utils import*
from input_handlers import*

class AirScrubber:
    amount = 0
    def __init__(self, scrubber_type, cfm_value, amount, weight, price):
        self.scrubber_type = scrubber_type
        self.cfm_value = float(cfm_value)
        self.amount = int(amount) # The amount of a specific scrubber a user has
        self.weight = float(weight)
        self.price = float(price) # Price of running the air scrubber
        self.no_weight = (weight == -1)
        self.no_price = (weight == -1)
        
    def set_flag(self, flag):
        self.flag = flag

    def set_amount(self, amount):
        self.amount = int(amount)

    def __repr__(self):
        return self.scrubber_type
    
    
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
    print("this is the result", result)
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
def remove_invalid_combos(all_combos, scrubbers):
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

    # Represent combos in ["2 as1"](strings) format instead of [as1, as1](AirScrubber objects) 
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
    print("\n" + f"To maintain {air_changes} air changes an hour, a total cfm of {cfm_target:.5}({cfm_target*0.000471947:.3}m³/s) is required" + "\n")
    
    all_combos = remove_duplicates(all_combos)
    print_output_combo(all_combos, "There are no combinations that meet your air purity requirements", "ALL COMBINATIONS") # Print every combo
    
    valid_combos = remove_invalid_combos(all_combos, scrubbers)
    print_output_combo(valid_combos, "There are no combinations that meet your current stock", "ALL VALID COMBINATIONS") # Print all valid combos
    sort_outputs(valid_combos, scrubbers)
    
#with count types instead of passing in list of list could pass in each combo list seperately and count type on that
#so we get 
        #for valid in valid_combos
        #   print(count_types(valid))
#instead of what we currently have count_types(valid_combos)
#maybe instead of typing error message just repeat the initial prompt