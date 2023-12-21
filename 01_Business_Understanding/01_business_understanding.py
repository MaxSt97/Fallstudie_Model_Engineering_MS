import pandas as pd
import matplotlib.pyplot as plt

# Einlesen der Daten PSP_Jan_Feb_2019
df = pd.read_excel("../PSP_Jan_Feb_2019.xlsx")

df['timestamp'] = pd.to_datetime(df['tmsp'])

# Balkendiagramm für Länder
plt.figure()
ax = df['country'].value_counts().plot(kind='bar', rot=0)

# Absolute Werte in der Mitte jedes Balkens anzeigen
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='center', fontsize=8, color='black', padding=2)

plt.title('Anzahl Transaktionen nach Land')
plt.tight_layout()
plt.yticks([])
plt.tight_layout()
plt.show()

# Kreisdiagramm für Erfolg
plt.figure()
success_counts = df['success'].value_counts()
labels = ['erfolgreich' if i == 1 else 'nicht erfolgreich' for i in success_counts.index]
plt.pie(success_counts.values, autopct='%1.1f%%', labels=labels, explode=[0, 0.1])
plt.title('Prozentsatz erfolgreicher/nicht erfolgreicher Transaktionen')
plt.tight_layout()
plt.show()

# Liniendiagramm für Transaktionsbeträge über die Zeit
weekly_avg_amount = df.groupby(df['timestamp'].dt.isocalendar().week)['amount'].mean()
plt.figure()
weekly_avg_amount.plot(marker='o', linestyle='-', color='b')
plt.title('Durchschnittlicher Transaktionsbetrag pro Kalenderwoche')
plt.xlabel('Kalenderwoche')
plt.ylabel('Durchschnittlicher Transaktionsbetrag')
plt.grid(True)
plt.tight_layout()
plt.show()

# Boxplot für Transaktionsbeträge
plt.figure()
df.boxplot(column='amount', vert=False, showfliers=False)
plt.title('Verteilung der Transaktionsbeträge')
plt.xlabel('Transaktionsbetrag')
plt.yticks([])
plt.tight_layout()
plt.show()

# Combine the data for all "PSP" categories
combined_data = df.groupby(['PSP', 'success'])['success'].count().unstack()
combined_data = combined_data[[1, 0]]

# Calculate percentages
combined_data_percentage = combined_data.div(combined_data.sum(axis=1), axis=0) * 100

plt.figure()
ax = combined_data_percentage.plot(kind='bar', stacked=True, color=['C1', 'C0'], rot=0)

# Prozentwerte über jedem Segment anzeigen
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=8, color='black', padding=2)
plt.title('Anteil erfolgreicher/nicht erfolgreicher Transaktionen nach PSP')
plt.xlabel('')
plt.ylabel('')

# Ändern Sie die Legende auf "erfolgreich" und "nicht erfolgreich"
plt.legend(title='Success', labels=['erfolgreich', 'nicht erfolgreich'], loc='upper right')
plt.yticks([])
plt.tight_layout()
plt.show()

# PSP Verteilung nach Land
combined_data = df.groupby(['country', 'PSP'])['PSP'].count().unstack()

combined_data_percentage = combined_data.divide(combined_data.sum(axis=1), axis=0) * 100

# Stacked Bar Chart mit prozentualen Werten in den Beschriftungen
ax = combined_data_percentage.plot(kind='bar', stacked=True, figsize=(10, 6), color=['C3', 'C2', 'C1', 'C0'],rot=0)

# Beschriftungen mit prozentualen Werten hinzufügen
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=8, color='black', padding=2)

plt.title('PSP Verteilung nach Ländern (Prozentuale Anteile)')
plt.xlabel('')
plt.ylabel('')
plt.legend(title='Kategorien')
plt.yticks([])
plt.tight_layout()
plt.show()

# Anzahl Transaktionen nach Tageszeit
df['hour'] = df['timestamp'].dt.hour
df.groupby('hour')['hour'].count().plot(kind='bar', rot=0)
plt.title('Anzahl Transaktionen nach Tageszeit')
plt.xlabel('Stunde')
plt.ylabel('Anzahl Transaktionen')
plt.tight_layout()
plt.show()

# Identische Transaktionen
df['minute'] = df['timestamp'].dt.minute
df['duplicated_transaction'] = df.duplicated(subset=['amount', 'country', 'minute'], keep=False)
df['duplicated_transaction'] = df['duplicated_transaction'].replace(
    {True: 'mehrere Versuche je Transaktion', False: 'ein Versuch je Transaktion'}
)

transaction_counts = df['duplicated_transaction'].value_counts()

plt.figure(figsize=(8,8))
plt.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, explode=[0, 0.1])
plt.title('Anzahl eindeutiger und identischer Transaktionen')
plt.tight_layout()
plt.show()

####
df['minute'] = df['tmsp'].dt.minute
df['hour'] = df['tmsp'].dt.hour
df['day'] = df['tmsp'].dt.day
df['month'] = df['tmsp'].dt.month
df['year'] = df['tmsp'].dt.year
df['weekday'] = df['tmsp'].dt.weekday
df['date'] = df['tmsp'].dt.date

df['transaction_id'] = df.groupby(['amount', 'country', 'minute', 'date', "card"]).ngroup() + 1

#zähle transaktionen die mehrere versuche benötigen bis die Transaktion gelingt
bar = []
for counter in [0,1,2,3,4,5]:
    count = df.groupby('transaction_id').apply(lambda group: (group['success'] == 1).sum() == 1 and (group['success'] == 0).sum() == counter).sum()
    bar.append(count)
    print(count)

#plot bar chart
plt.figure()
bars = plt.bar([0, 1, 2, 3, 4, 5], bar)
plt.title('Anzahl Transaktionen nach Anzahl Versuche')
plt.xlabel('Anzahl Versuche')
plt.ylabel('Anzahl Transaktionen')
for bar, value in zip(bars, bar):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value),
             ha='center', va='bottom', fontsize=8, color='black')
plt.yticks([])
plt.tight_layout()
plt.show()




#####kommt auf die folgeseite data preprocessing
#print amoutn of unique transaction_ids
print(df['transaction_id'].nunique())
#count amount of transaction_ids which never succeed
count = df.groupby('transaction_id').apply(lambda group: (group['success'] == 1).sum() == 0).sum()
print(count)

#count transaction_ids with more than one success and print transaction_id of these entries

count = df.groupby('transaction_id').apply(lambda group: (group['success'] == 1).sum() > 1).sum()
print(f"Number of transaction_ids with more than one success: {count}")

# Print specific transaction_ids with more than one success
transaction_ids_with_more_than_one_success = df.groupby('transaction_id').apply(lambda group: group['transaction_id'].iloc[0] if (group['success'] == 1).sum() > 1 else None).dropna().unique()
print(transaction_ids_with_more_than_one_success)




