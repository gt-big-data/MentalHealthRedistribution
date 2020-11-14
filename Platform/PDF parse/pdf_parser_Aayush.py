# Imports
import re
import pandas as pd

# Dictionary of Regex
rx_dict = {
    'Phone': r'(?<=Phone: ) *\(?\d*\)? *\d*( |-)\d*',
    'State': r'(?<=, )(.*)(?= \d)',
    'City': r'(\w+)(?=,)',
    'Zip': r'(?<=\s)(\d){5}',
    'Address': r'(^((\d|-)+))\s([a-zA-Z0-9]+\s)+'
}

# Parses through file
def parse_file(filepath):
    df = pd.DataFrame(columns=['Address', 'State', 'City', 'Zip', 'Phone'])
    data = []
    with open(filepath, 'r') as file_object:
        i = 0
        missed = 0 # To count potential misses
        for line in file_object:
            for key, value in rx_dict.items():
                match = re.search(value, line)
                if match:
                    data.append(match.group(0))
                    # Checks if the data parsed is correct
                    if len(data) == 5 and key == 'Phone':
                        df.loc[i] = data # Adds to dataframe
                        i += 1
                        data = []
                    elif key == 'Phone' and len(data) != 5:
                        missed += 1
                        data = []

    # Fix formatting of df/clean up
    df['Address'] = df['Address'].apply(lambda x: x[:len(x)-1])
    df = df.reindex(columns=['State', 'City', 'Zip', 'Address', 'Phone'])
    return df, missed # Returns filled dataframe and number of potential misses

        
            
if __name__ == '__main__':
    filepath = 'National_Directory_MH_facilities_301-600.txt'
    df, missed = parse_file(filepath)

    #print(df)
    # Converts to .CSV
    df.to_csv('mental_health_parse_301-600.csv', index = False, header=True)