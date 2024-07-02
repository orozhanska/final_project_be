import pandas as pd

df = pd.DataFrame({'csv_path': [], 'total_records': [], 'metric': []})
df.at[0, 'csv_path'] = 'vorona.com'

print("Hello")