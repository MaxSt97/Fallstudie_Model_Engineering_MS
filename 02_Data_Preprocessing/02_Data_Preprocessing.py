import pandas as pd

# Einlesen der Daten PSP_Jan_Feb_2019
df = pd.read_excel("../PSP_Jan_Feb_2019.xlsx")

# Fehlende Werte überprüfen
print(f"Die Anzahl der Fehlenden Werte: " + str(df.isnull().sum()))

# Duplikate überprüfen
print(f"Anzahl der Duplikate: " + str(df.duplicated().sum()))

# Anzahl unterschiedliche Werte Country, Success, PSP, 3D_secured, card
columns_to_count = ['country', 'success', '3D_secured', 'card', 'PSP']

for column in columns_to_count:
    print(f"Anzahl der unterschiedlichen Werte für {column}: " + str(df[column].value_counts()))

# Amount genauer beschreiben
print(df['amount'].describe())


