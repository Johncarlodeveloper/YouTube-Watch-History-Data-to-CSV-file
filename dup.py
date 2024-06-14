import shutil


def duplicate_csv(original_file, new_file):
    try:
        shutil.copyfile(original_file, new_file)
        print(f"Duplicate of {original_file} created as {new_file}")
    except FileNotFoundError:
        print("File not found.")


# Example usage
original_file = 'testing.csv'
new_file = 'save.csv'
duplicate_csv(original_file, new_file)
