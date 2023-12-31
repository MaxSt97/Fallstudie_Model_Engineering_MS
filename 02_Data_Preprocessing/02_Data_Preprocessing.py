import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Einlesen der Daten PSP_Jan_Feb_2019
df = pd.read_excel("../PSP_Jan_Feb_2019.xlsx")

## Daten werden für das Modell vorbereitet
# transaction_id muss vor Überprüfung hinzugefügt werden
df['minute'] = df['tmsp'].dt.minute
df['hour'] = df['tmsp'].dt.hour
df['day'] = df['tmsp'].dt.day
df['month'] = df['tmsp'].dt.month
df['year'] = df['tmsp'].dt.year
df['weekday'] = df['tmsp'].dt.weekday
df['date'] = df['tmsp'].dt.date

df['transaction_id'] = df.groupby(['amount', 'country', 'minute', 'date', "card"]).ngroup() + 1

## Daten werden überprüft
# Fehlende Werte überprüfen
print("Anzahl der Fehlenden Werte:")
print(f"Die Anzahl der Fehlenden Werte: {df.isnull().sum()}")

# Duplikate überprüfen
print("Anzahl der Duplikate:")
print(f"Anzahl der Duplikate: {df.duplicated().sum()}")

# Anzahl unterschiedliche Werte Country, Success, PSP, 3D_secured, card
columns_to_count = ['country', 'success', '3D_secured', 'card', 'PSP']
for column in columns_to_count:
    print(f"Anzahl der unterschiedlichen Werte für {column}: {df[column].value_counts()}")

# Amount genauer beschreiben
print("Beschreibung der Spalte 'amount':")
print(df['amount'].describe())

# Anzahl der unterschiedlichen Transaktionsids
print("Anzahl der unterschiedlichen Transaktionsids:")
print(df['transaction_id'].nunique())

# Anzahl der Transaktionen ohne Erfolg
count = df.groupby('transaction_id').apply(lambda group: (group['success'] == 1).sum() == 0).sum()
# Print specific transaction_ids with more than one success
transaction_ids_with_more_than_one_success = df.groupby('transaction_id').apply(lambda group: group['transaction_id'].iloc[0] if (group['success'] == 1).sum() > 1 else None).dropna().unique()
print("Transaktionsids welche mehr als eine erfolgreiche Transaktion enthalten:")
print(transaction_ids_with_more_than_one_success)

## Daten werden für das Modell vorbereitet
# Gebühren für Zahlungen werden hinzugefügt
fee_data = {
    'PSP': ['Moneycard', 'Goldcard', 'UK_Card', 'Simplecard'],
    'fee_success': [5, 10, 3, 1],
    'fee_failure': [2, 5, 1, 0.5],
}
fee_df = pd.DataFrame(fee_data)

# Setzen Sie die Gebühren basierend auf der 'success'-Bedingung
df.loc[df['success'] == 1, 'fee'] = pd.merge(df[df['success'] == 1], fee_df, on='PSP', how='left')['fee_success']
df.loc[df['success'] == 0, 'fee'] = pd.merge(df[df['success'] == 0], fee_df, on='PSP', how='left')['fee_failure']

# Feauture Encoding
label_encoder_country = LabelEncoder()
label_encoder_card = LabelEncoder()
label_encoder_PSP = LabelEncoder()
label_encoder_weekday = LabelEncoder()

df['country'] = label_encoder_country.fit_transform(df['country'])
df['card'] = label_encoder_card.fit_transform(df['card'])
df['PSP'] = label_encoder_PSP.fit_transform(df['PSP'])
df['weekday'] = label_encoder_weekday.fit_transform(df['weekday'])

# Entferne duplikate aus der Spalte "transaction_id" bei denen success = 1
for transaction_id in transaction_ids_with_more_than_one_success:
    mask = (df['transaction_id'] == transaction_id) & (df['success'] == 1)
    first_success_index = mask.idxmax()

    # Entferne alle außer dem ersten Vorkommen von 'success=1'
    df = df.drop(df[mask].index.difference([first_success_index]))

# Entfernen von Features die nicht benötigt werden
df = df.drop(['tmsp', 'date', 'Unnamed: 0','transaction_id', 'year', 'month'], axis=1)

# Korrelationsanalyse
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
correlation_matrix = df.corr()
print(correlation_matrix)

# Daten für die weitere Nutzung zwischen speichern
df.to_csv('../PSP_Jan_Feb_2019_preprocessed.csv')



