import pandas as pd  
import os 

# merge data function
def merge_data():
    master_df = pd.DataFrame()
    for file in os.listdir('forairflow/data/allcsv'):
        if file.endswith('.csv'):
            try:
                df = pd.read_csv(f'fixture_project/data/allcsv/{file}', na_values=[''], on_bad_lines='skip')
                master_df = pd.concat([master_df, df], ignore_index=True)
            except pd.errors.ParserError as e:
                print(f"Error parsing {file}: {e}")
    master_df.to_csv('/Users/mustafagul/Desktop/fixture_project/data/mergeddata/masterupdateafter2000.csv', index=False)
    return master_df


