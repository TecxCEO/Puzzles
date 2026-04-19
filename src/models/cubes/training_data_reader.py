import json

def get_nested_value(data, target_key):
    """
    Recursively searches for a target_key in a nested dictionary.
    """
    cst={}
    
    # If the current element is a dictionary, look inside
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "state":
                #yield value
                cst=value
            elif len(key) == 3 and len(value)==20 :
                #yield value
                return value
            # If the value is another dictionary, dive deeper (recursion)
            elif isinstance(value, (dict, list)):
                yield from get_nested_value(value, target_key)
            
            #if key == target_key:
                #yield value
            # If the value is another dictionary, dive deeper (recursion)
            #elif isinstance(value, (dict, list)):
                #yield from get_nested_value(value, target_key)
                
    # If it's a list, check every item in the list
    elif isinstance(data, list):
        for item in data:
            yield from get_nested_value(item, target_key)

# Example Usage:
# for value in get_nested_value(my_json_data, "image_data"):
#     print(value)


def process_adjacent_json(file_path, target_key):
    try:
        with open(file_path, 'r') as f:
            # For massive files on Android, use ijson or read line-by-line
            # If the file fits in RAM, use this:
            data = json.load(f)
            
            # Start the recursive search
            results = list(get_nested_value(data, target_key))
            return results
    except FileNotFoundError:
        print("File not found. Check the path.")
        return []

# Usage for your "Cubicle" states
# states = process_adjacent_json('puzzle_data.json', 'state')
