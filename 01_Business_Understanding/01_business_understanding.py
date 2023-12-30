import pandas as pd
import matplotlib.pyplot as plt

# Einlesen der Daten PSP_Jan_Feb_2019
df = pd.read_excel("../PSP_Jan_Feb_2019.xlsx")

df['timestamp'] = pd.to_datetime(df['tmsp'])

# Kuchendiagramm für Transaktionen nach Land
percentage_values = df['country'].value_counts(normalize=True) * 100
plt.figure()
plt.pie(percentage_values, labels=percentage_values.index, autopct='%1.1f%%', explode=[0, 0.1, 0.1])
plt.title('Prozentsatz der Transaktionen nach Land')
plt.tight_layout()
plt.show()

# Kuchendiagramm für erfolgreiche/nicht erfolgreiche Transaktionen
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

# Balkendiagramm für Erfolg nach Kartenanbieter
combined_data = df.groupby(['card', 'success'])['success'].count().unstack()
combined_data = combined_data[[1, 0]]
combined_data_percentage = combined_data.div(combined_data.sum(axis=1), axis=0) * 100

plt.figure()
ax = combined_data_percentage.plot(kind='bar', stacked=True, color=['C1', 'C0'], rot=0, width=0.8)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=8, color='black', padding=2)

plt.title('Anteil erfolgreicher/nicht erfolgreicher Transaktionen nach Karte')
plt.xlabel('')
plt.ylabel('')
plt.legend(title='Success', labels=['erfolgreich', 'nicht erfolgreich'], loc='upper right')
plt.yticks([])
plt.tight_layout()
plt.show()

# Balkendiagramm für Erfolg nach PSP
combined_data = df.groupby(['PSP', 'success'])['success'].count().unstack()
combined_data = combined_data[[1, 0]]
combined_data_percentage = combined_data.div(combined_data.sum(axis=1), axis=0) * 100

plt.figure()
ax = combined_data_percentage.plot(kind='bar', stacked=True, color=['C1', 'C0'], rot=0, width=0.8)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=8, color='black', padding=2)

plt.title('Anteil erfolgreicher/nicht erfolgreicher Transaktionen nach PSP')
plt.xlabel('')
plt.ylabel('')
plt.legend(title='Success', labels=['erfolgreich', 'nicht erfolgreich'], loc='upper right')
plt.yticks([])
plt.tight_layout()
plt.show()

# Balkendiagramm für Verteilung PSP nach Ländern
combined_data = df.groupby(['country', 'PSP'])['PSP'].count().unstack()
combined_data_percentage = combined_data.divide(combined_data.sum(axis=1), axis=0) * 100

ax = combined_data_percentage.plot(kind='bar', stacked=True, color=['C3', 'C2', 'C1', 'C0'], rot=0, width=0.8)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='center', fontsize=8, color='black', padding=2)

plt.title('PSP Verteilung nach Ländern (Prozentuale Anteile)')
plt.xlabel('')
plt.ylabel('')
plt.legend(title='Kategorien')
plt.yticks([])
plt.tight_layout()
plt.show()

# Balkendiagramm Transaktionen nach Tageszeit
df['hour'] = df['timestamp'].dt.hour
df.groupby('hour')['hour'].count().plot(kind='bar', rot=0)
plt.title('Anzahl Transaktionen nach Tageszeit')
plt.xlabel('Stunde')
plt.ylabel('Anzahl Transaktionen')
plt.tight_layout()
plt.show()

# Kuchendiagramm ein Versuch/mehrere Versuche je Transaktion
df['minute'] = df['timestamp'].dt.minute
df['duplicated_transaction'] = df.duplicated(subset=['amount', 'country', 'minute'], keep=False)
df['duplicated_transaction'] = df['duplicated_transaction'].replace(
    {True: 'mehrere Versuche je Transaktion', False: 'ein Versuch je Transaktion'}
)

transaction_counts = df['duplicated_transaction'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, explode=[0, 0.1])
plt.title('Anzahl eindeutiger und identischer Transaktionen')
plt.tight_layout()
plt.show()

df['minute'] = df['tmsp'].dt.minute
df['hour'] = df['tmsp'].dt.hour
df['day'] = df['tmsp'].dt.day
df['month'] = df['tmsp'].dt.month
df['year'] = df['tmsp'].dt.year
df['weekday'] = df['tmsp'].dt.weekday
df['date'] = df['tmsp'].dt.date
df['transaction_id'] = df.groupby(['amount', 'country', 'minute', 'date', "card"]).ngroup() + 1

# Balkendiagramm für Anzahl Transaktionen nach Anzahl Versuche
bar = []
for counter in [0, 1, 2, 3, 4, 5]:
    count = df.groupby('transaction_id').apply(
        lambda group: (group['success'] == 1).sum() == 1 and (group['success'] == 0).sum() == counter).sum()
    bar.append(count)

plt.figure()
bars = plt.bar([0, 1, 2, 3, 4, 5], bar, width=0.8)
plt.title('Anzahl Transaktionen nach Anzahl Versuche')
plt.xlabel('Anzahl Versuche')
plt.ylabel('Anzahl Transaktionen')
for bar, value in zip(bars, bar):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value),
             ha='center', va='bottom', fontsize=8, color='black')
plt.xticks([0, 1, 2, 3, 4, 5], ['1', '2', '3', '4', '5', '6'])
plt.yticks([])
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



