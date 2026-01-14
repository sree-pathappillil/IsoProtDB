# this is to check the ptm site
import pandas as pd

data = pd.read_excel(r'input file name')

# Function to get only the middle character from the cleaned sequence
def get_middle_character(sequence):
    # Remove underscores from the sequence
    cleaned_sequence = sequence.replace("_", "")
    if len(cleaned_sequence) == 0:
        return ""  # Return empty if the cleaned sequence has no characters
    
    mid_index = len(cleaned_sequence) // 2

    # Extract and return the middle character
    middle_character = cleaned_sequence[mid_index]
    return middle_character

# Apply the function to create the new column
data['middle_character'] = data['windowsequence'].apply(get_middle_character)

print(data[['windowsequence', 'middle_character']])
data.to_excel('_sitefetch___new.xlsx')
