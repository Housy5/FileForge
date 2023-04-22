import os
import psutil
import re

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")


def parse_unit(raw_string):
    unit = ""
    for char in raw_string:
        if char.isalpha():
            unit += char
    return unit.lower()


def parse_value(raw_string):
    result = 0
    for char in raw_string:
        if char.isdigit():
            result = result * 10 + int(char)
    return result


def convert_size_to_bytes(size_str):
    size_str = size_str.lower()
    if size_str.isdigit():
        return int(size_str)

    size_units = {
        "b": 1,
        "kb": 1024,
        "mb": 1048576,
        "gb": 1073741824,
        "tb": 1099511627776
    }
    
    unit = parse_unit(size_str)
    
    if unit not in size_units:
        abort(f"'{unit}' is not a valid size modifier! (b, kb, mb, gb, or tb)")
    
    size_value = parse_value(size_str)
    
    for key, value in size_units.items():
        if unit == key:
            return int(size_value * value)
    return None


def is_valid_name(name):
    invalid_chars_regex = re.compile(r'[\\/:\*\?"<>\|]')
    if invalid_chars_regex.search(name):
        return False
    
    if len(name) > 260:
        return False
    
    return True


def format_number(number):
    return '{:,.0f}'.format(number)


def write_file(path, size):
    block_size = 1024 * 1024  # 1 MB block size
    num_blocks = size // block_size  # number of blocks to write
    remainder = size % block_size  # remaining bytes to write

    with open(path, 'wb') as f:
        for i in range(num_blocks):
            print(f"{i + 1}/{num_blocks} blocks finished.")
            block = os.urandom(block_size)
            f.write(block)

        if remainder > 0:
            block = os.urandom(remainder)
            f.write(block)


def check_memory(size):
    print("Checking memory...")
    available = psutil.disk_usage('/').free
    if size > available:
        abort("There isn't enough memory on this system!")
    print("Memory -> ok!")
        

def abort(message="Aborted!"):
    print(message)
    exit()


def main():
    location = get_desktop_path()
    
    if not os.path.isdir(location):
        abort("Failed to dected the desktop!")

    file_name = input("Please enter a name for the file: ")
    if not is_valid_name(file_name):
        abort("This name is invalid! (Check the windows file name specifications)")
    
    full_path = os.path.join(location, file_name)
    
    if os.path.exists(full_path):
        confirm = input(f"The file '{full_path}' already exists. Do you want to overwrite it? (y/n): ")
        if confirm.lower() != "y":
            abort()
    
    size = convert_size_to_bytes(input("Enter the file size: "))
    if input(f"Are you sure you want to create a file with {format_number(size)} bytes? (y/n): ").lower() != 'y':
        abort()
    
    check_memory(size)
    
    print("Writing....")
    write_file(full_path, size)
    print("Finished!")
    
if __name__ == '__main__':
    main()