import pandas as pd
import matplotlib.pyplot as plt

# Einlesen der Daten PSP_Jan_Feb_2019
df = pd.read_excel("../PSP_Jan_Feb_2019.xlsx")

# Balkendiagramm für Länder
plt.figure()
df['country'].value_counts().plot(kind='bar', rot=0)
plt.title('Verteilung der Transaktionen nach Ländern')
plt.tight_layout()
plt.show()

# Kreisdiagramm für Erfolg
plt.figure()
success_counts = df['success'].value_counts()
labels = ['erfolgreich' if i == 1 else 'nicht erfolgreich' for i in success_counts.index]
plt.pie(success_counts.values, autopct='%1.1f%%', labels=labels)
plt.title('Prozentsatz erfolgreicher/nicht erfolgreicher Transaktionen')
plt.tight_layout()
plt.show()

# Liniendiagramm für Transaktionsbeträge über die Zeit
plt.figure()
df['timestamp'] = pd.to_datetime(df['tmsp'])
df.groupby('timestamp')['amount'].sum().plot()
plt.title('Verlauf der Transaktionsbeträge über die Zeit')
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
ax = combined_data_percentage.plot(kind='bar', stacked=True, color=['C1', 'C0'])

# Prozentwerte über jedem Segment anzeigen
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='edge', fontsize=8, color='black', padding=2)
plt.title('Anteil erfolgreicher/nicht erfolgreicher Transaktionen nach PSP')
plt.xlabel('PSP')
plt.ylabel('Prozent')

# Ändern Sie die Legende auf "erfolgreich" und "nicht erfolgreich"
plt.legend(title='Success', labels=['erfolgreich', 'nicht erfolgreich'], bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.show()

# PSP Verteilung nach Land
combined_data = df.groupby(['country', 'PSP'])['PSP'].count().unstack()

for country in combined_data.index:
    print(country)
    country_data = combined_data.loc[country]
    colors = plt.cm.Paired(range(len(country_data)))
    country_data.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(6, 6), colors=colors)

    plt.title(f'PSP Verteilung in {country}')
    plt.ylabel('')  # Entfernt die y-Achsenbeschriftung
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
plt.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
plt.title('Anzahl eindeutiger und identischer Transaktionen')
plt.tight_layout()
plt.show()







