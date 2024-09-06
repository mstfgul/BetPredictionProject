import pandas as pd  
import os 

master_df = pd.DataFrame()

for file in os.listdir('data'):
    if file.endswith('.csv'):
        try:
            df = pd.read_csv(f'data/{file}', na_values=[''], on_bad_lines='skip')
            master_df = pd.concat([master_df, df], ignore_index=True)
        except pd.errors.ParserError as e:
            print(f"Error parsing {file}: {e}")

master_df.to_csv('master.csv', index=False)