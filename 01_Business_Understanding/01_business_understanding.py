import pandas as pd
import matplotlib.pyplot as plt

# Einlesen der Daten PSP_Jan_Feb_2019
df = pd.read_excel("../PSP_Jan_Feb_2019.xlsx")
# Grafiken erstellen
plt.figure(figsize=(10, 6))

# Balkendiagramm für Länder
plt.figure(figsize=(10, 6))
df['country'].value_counts().plot(kind='bar', rot=0)
plt.title('Verteilung der Transaktionen nach Ländern')
plt.show()

# Kreisdiagramm für Erfolg
plt.figure(figsize=(10, 6))
df['success'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Prozentsatz erfolgreicher/nicht erfolgreicher Transaktionen')
plt.show()

# Liniendiagramm für Transaktionsbeträge über die Zeit
plt.figure(figsize=(10, 6))
df['timestamp'] = pd.to_datetime(df['tmsp'])
df.groupby('timestamp')['amount'].sum().plot()
plt.title('Verlauf der Transaktionsbeträge über die Zeit')
plt.show()

# Combine the data for all "PSP" categories
combined_data = df.groupby(['PSP', 'success'])['success'].count().unstack()

combined_data = combined_data[[1, 0]]
# Calculate percentages
combined_data_percentage = combined_data.div(combined_data.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12, 8))
ax = combined_data_percentage.plot(kind='bar', stacked=True, figsize=(12, 8))

# Prozentwerte über jedem Segment anzeigen
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='edge', fontsize=8, color='black', padding=2)
plt.title('Anteil erfolgreicher/nicht erfolgreicher Transaktionen nach PSP')
plt.xlabel('PSP')
plt.ylabel('Prozent')
# Ändern Sie die Legende auf "erfolgreich" und "nicht erfolgreich"
plt.legend(title='Success', labels=['erfolgreich', 'nicht erfolgreich'])
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
    plt.show()






