from sklearn.dummy import DummyClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, make_scorer
from sklearn.model_selection import cross_val_score
import pandas as pd

# Einlesen der Daten PSP_Jan_Feb_2019_preprocessed
df = pd.read_csv("../PSP_Jan_Feb_2019_preprocessed.csv")

# Feature Auswahl und Zielvariable
features = ['amount', 'PSP', '3D_secured', 'card', 'country', 'weekday', 'day', 'hour', 'minute']
target_variable = ['success']

X = df[features]
y = df[target_variable].values.ravel()

# Baseline-Modell erstellen (am häufigsten auftretende Klasse verwenden)
baseline_model = DummyClassifier(strategy='most_frequent')

# Durchführung von Kreuzvalidierung und Bewertung der Baseline
baseline_scores = cross_val_score(baseline_model, X, y, cv=5, scoring=make_scorer(f1_score, average='weighted'))
print(f'Baseline Model F1-Score: {baseline_scores.mean()}')

# Bewertungsmetriken für das Baseline-Modell ausgeben
baseline_model.fit(X, y)
baseline_predictions = baseline_model.predict(X)

accuracy = accuracy_score(y, baseline_predictions)
precision = precision_score(y, baseline_predictions, pos_label=1, zero_division=1.0, average='weighted')
recall = recall_score(y, baseline_predictions, pos_label=1, zero_division=1.0, average='weighted')
f1_score = f1_score(y, baseline_predictions, pos_label=1, zero_division=1.0, average='weighted')

print('Baseline Model Metrics:')
print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1-Score: {f1_score}')
