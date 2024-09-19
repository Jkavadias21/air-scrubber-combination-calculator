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

    def __hash__(self):
        return hash((self.scrubber_type))
    
    def __eq__(self, other):
        return isinstance(other, AirScrubber) and self.scrubber_type == other.scrubber_type
        

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
    return result

# Return a list of all combinations that meet purity requirements(contains duplicates)
def add_overflow_all(scrubber_combos, scrubbers, cfm_target):
    all_combos = []
    
    for combo in scrubber_combos:
        for scrubber in scrubbers:
            # Add overflow scrubber only if the combo is one scrubber away from exceeding or meeting the cfm target
            if (sum_combos_cfm_values(combo) + scrubber.cfm_value >= cfm_target):
                overflowed_combo = combo + [scrubber]
                all_combos.append(overflowed_combo)
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
def prepare_output(original_combos, all_combos, no_subset_combos, cfm_target, scrubbers):
    # Clear existing lists to ensure they start empty
    original_combos.clear()
    all_combos.clear()

    # Extend to add all elements to the end of the lists globally
    original_combos.extend(find_scrubber_combos(scrubbers, cfm_target)) # Find all combination with cfm total less than or equal to target cfm
    all_combos.extend(add_overflow_all(original_combos, scrubbers, cfm_target))  # Generate array containing every combination (contains duplicates)
    no_subset_combos.extend(remove_lists_with_subsets(remove_duplicates(all_combos))) # List that contains all combos with subsets removed(used in final output)
    
    
# Display all combinations and calculations
def display_output(no_subset_combos, air_changes, cfm_target, scrubbers):
    
    print("\n" + f"To maintain {air_changes} air changes an hour, a total cfm of {cfm_target:.5}({cfm_target*0.000471947:.3}m³/s) is required" + "")
    
    print_output_combo(no_subset_combos, "There are no combinations that meet your air purity requirements", "ALL COMBINATIONS WITHOUT SUBSETS") # Print every combo with subsets removed
    
    print_output_combo(remove_invalid_combos(no_subset_combos, scrubbers), "There are no combinations that meet your current stock", "ALL VALID COMBINATIONS") # Print all combos that meet users stock
    sort_outputs(remove_invalid_combos(no_subset_combos, scrubbers), scrubbers)
    
#with count types instead of passing in list of list could pass in each combo list seperately and count type on that
#so we get 
        #for valid in valid_combos
        #   print(count_types(valid))
#instead of what we currently have count_types(valid_combos)
#maybe instead of typing error message just repeat the initial prompt

#further analyse overflow adding, seems to be working fine but need to make sure since its crucial to the operation
#also make sure the intital <= cfm target functionality is correct(find_scrubber_combo)
#maybe could optimise remove_invalid_combos with the use of Counters