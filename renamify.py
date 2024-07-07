import glob
import os
import sys


def rename_files(name_lookup, directory_path, text_file):
    current_folder = os.path.splitext(os.path.basename(text_file))[0]
    name = name_lookup[current_folder]

    matches_found = 0
    file_count = 0

    # Create a dictionary for quick lookup
    file_info = parse_text_file(name, text_file)

    # Iterate over files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        file_count = file_count + 1
        # if file_count > 10:
        #     break

        # Check if the file name matches an entry in the text file
        if filename in file_info:
            new_filename = file_info[filename]
            new_file_path = os.path.join(directory_path, new_filename)
            matches_found = matches_found + 1
            os.rename(file_path, new_file_path)
            # print(f"Renamed {filename} to {new_filename}")
        # else:
        #     print(f"No match found for {filename}")
    print(f"Matches found: {matches_found} out of {file_count}")


def parse_text_file(name, text_file):
    file_info = {}
    with open(text_file, 'r') as f:
        # Skip the header line
        next(f)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 5:
                continue  # Skip lines that don't have exactly 5 columns

            media_id, post_id, created, media_url, sha256 = parts
            filename = os.path.basename(media_url)
            extension = os.path.splitext(media_url)[1]
            new_name = f"{name}_{post_id}_{media_id}{extension}"
            file_info[filename] = new_name

    return file_info


def get_name_lookup(key_file):
    # Read the key file
    print(f"key file {key_file}")
    name_lookup = {}
    with open(key_file, 'r') as f:
        # Skip the header line
        next(f)
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) != 2:
                continue  # Skip lines that don't have exactly 2 columns

            code, name = parts
            name_lookup[code] = name

    print(f"Name lookup {name_lookup}")
    return name_lookup


def get_text_file_list(directory_path):
    # Use glob to find all files matching the pattern "b*.txt" in the directory
    pattern = os.path.join(directory_path, 'b*.txt')
    file_list = glob.glob(pattern)

    # Extract the file names from the full paths
    file_names = [file_path for file_path in file_list]

    return file_names


def get_specific_directory_path():
    return f"{directory_path}\\{os.path.basename(text_file).split('.')[0]}"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python renamify.py <key_file> <directory_path>")
        sys.exit(1)

    key_file = sys.argv[1]
    directory_path = sys.argv[2]
    # text_file = sys.argv[3]

    name_lookup = get_name_lookup(key_file)

    counter = 0

    text_file_list = get_text_file_list(directory_path)
    print(f"text file list {text_file_list}")
    for text_file in text_file_list:
        path = get_specific_directory_path()
        counter = counter + 1
        # if counter > 5:
        #     break
        # print(f"path {path}")
        # rename_files(name_lookup, path, text_file)

    for name in name_lookup.keys():
        print(f"rename {directory_path}\\{name} to {directory_path}\\{name_lookup[name]}")
        os.rename(f"{directory_path}\\{name}", f"{directory_path}\\{name_lookup[name]}")

