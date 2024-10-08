from utils import*

# Read in valid inputs from user
def get_valid_input(prompt, is_skipable = False, is_int=False):
    while True:
        try:
            value = input(prompt)
            if is_skipable and value == "": # Skip skipable inputs by typing enter
                print("Input skipped")
                return -1 # If input was skipped assign a place holder value of -1
            
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
    from core import AirScrubber
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
        scrubber_amount = get_valid_input("Enter air scrubber amount: ", False, True)
        scrubber_weight = get_valid_input("Enter air scrubber weight (or press Enter to skip): ", True, False)
        scrubber_price = get_valid_input("Enter air scrubber price (or press Enter to skip): ", True, False)

        scrubbers.append(AirScrubber(scrubber_type, scrubber_cfm, scrubber_amount, scrubber_weight, scrubber_price))
        
        # Check if user wants to add more air scrubbers or not
        while True:
            more_inputs = input("Do you want to add another air scrubber? (yes/no): ").strip().lower()
            if more_inputs in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        if more_inputs != 'yes':
            break
    return scrubbers
   
    
# Assign user inputs pertaining to cfm calculations
def get_calculation_inputs():
    from utils import meter_to_feet
    while True:
        units = input("Enter m for meters or f for feet: ").lower()
        if units == 'm' or units == 'f':
            break
        # For testing
        elif units == 's':
            return 10, 10, 10, 1
    # Check and assign valid user volume and air change inputs
    while True:
        try:
            room_length = get_valid_input("Enter room length: ")
            room_width = get_valid_input("Enter room width: ")
            room_height = get_valid_input("Enter room height: ")
            air_changes = get_valid_input("Enter required air changes:", False, True)
            print(f"Length: {room_length}, Width: {room_width}, Height: {room_height}, Air Changes: {air_changes}")
            break  # Exit the loop if all inputs are valid
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    # Perform required unit conversions
    room_length, room_width, room_height = meter_to_feet(room_length, room_width, room_height, units)
    
    return room_length, room_width, room_height, air_changes

# Read in on valid responses to a yes/no input prompt 
def yes_no_check(input_prompt, error_string):
    first_prompt = True
    
    while True:
        # Display input prompt only on the first iteration otherwise print error message
        if first_prompt:
            user_input = input(input_prompt)
            first_prompt = False
        # Print error string if non yes or no string was typed
        else:
            user_input = input(error_string) #<- could change the error string to a static string like invalid input please type yes or no
        # Exit if yes or no was tpyed
        if user_input.strip().lower() == "yes":
            return True
        elif user_input.strip().lower() == "no":
            return


    

