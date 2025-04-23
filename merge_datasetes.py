import os

root_directory = r"C:/Users/zack/OneDrive/Desktop/coding/python/new bib_rec/People.v1i.yolov11"
# Specify the directory
directory_path_read = root_directory+ r"/test/labels"  # Replace with your directory path
directory_path_write = root_directory+ r"/test/labels_mod"

def list_files_in_directory(directory):
    """
    Lists all files in the specified directory.
    
    :param directory: Path to the directory
    :return: List of file names in the directory
    """
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            print(f"The directory '{directory}' does not exist.")
            return []

        # Get a list of files and folders
        items = os.listdir(directory)

        # Filter the list to include only files
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]

        # print(f"Files in '{directory}':")
        # for file in files:
        #     print(f"- {file}")

        return files



    except Exception as e:
        print(f"An error occurred: {e}")
        return []
def modify_file(filename):
    fullpath = directory_path_read + "/" + filename
    with open(fullpath, 'r') as file:
        lines = file.readlines()
        updated_lines = []
        
        for line in lines:
            parts = line.strip().split(' ')  # Split by a whitespace
            if parts:  # Ensure the line is not empty
                parts[0] = f"{1}"  # Example modification: double the first value
            updated_line = ' '.join(parts) + '\n'  # Reconstruct the line
            updated_lines.append(updated_line)
        print (updated_lines)

    # Write the modified lines back to the file
    with open(directory_path_write +'/'+ filename, 'w') as file:
        file.writelines(updated_lines)
    

# List files in the directory

files = list_files_in_directory(directory_path_read)
if not os.path.exists(directory_path_write):
    os.makedirs(directory_path_write)

for file in files:
    modify_file(file)
            
