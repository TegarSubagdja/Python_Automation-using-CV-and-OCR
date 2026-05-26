import pandas as pd

df = pd.read_excel("Data/oriental_name_cleaned.xlsx", dtype=str)

df['No'] = ''
df['status'] = ''
df['code'] = ''
df['description'] = ''

# simpan kembali ke df
df.rename(columns={'Name': 'name'}, inplace=True)

df = df[['No', 'name', 'code', 'status', 'description']]

for idx, row in df.iterrows():
    
    if row['name'].lower().startswith("oriental "):
        textRow = row['name'].split(" ")[1].split("#")[0].split("+")[0]
    else:
        textRow = row['name'].split(" ")[0].split("#")[0].split("+")[0]

    df.loc[idx, 'code'] = textRow
    df.loc[idx, 'name'] = f"ORIENTAL {textRow}"

df.drop_duplicates(subset=['code'], keep='first', inplace=True)
df.drop_duplicates(subset=['name'], keep='first', inplace=True)

df.reset_index(drop=True, inplace=True)

df['No'] = range(1, len(df) + 1)

print(df.info())

df.to_excel("Data/data2.xlsx", index=False)