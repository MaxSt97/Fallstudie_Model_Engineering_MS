from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, make_scorer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import pandas as pd

df = pd.read_csv("../PSP_Jan_Feb_2019_preprocessed.csv")

# Feature Auswahl und Zielvariable
features = ['amount', 'PSP', '3D_secured', 'card', 'country', 'weekday', 'day', 'hour', 'minute']
target_variable = ['success']

X = df[features]
y = df[target_variable].values.ravel()

# Verschiedene Modelle testen
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Support Vector Machine': SVC(),
    'Naive Bayes': GaussianNB(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(),
    'Neural Network': MLPClassifier(random_state=42)
}

# Durchführung von Kreuzvalidierung und Vergleich der Modelle
score = 0
for model_name, model in models.items():
    # Verwenden Sie f1_score als Metrik für die cross_val_score
    scores = cross_val_score(model, X, y, cv=5, scoring=make_scorer(f1_score, average='weighted'))
    if scores.mean() > score:
        score = scores.mean()
        highest_score = scores.mean()
        model_name_highest_score = model_name
    print(f'{model_name} F1-Score: {scores.mean()}')

print(f'The highes score is {highest_score} of model {model_name_highest_score}')

model = RandomForestClassifier()
parameters = {'n_estimators': [50, 100, 200, 300]}
grid_search = GridSearchCV(model, parameters, cv=5, scoring='accuracy')
grid_search.fit(X, y)

best_n_estimators = grid_search.best_params_['n_estimators']
print(f'Die beste Anzahl der Bäume ist {best_n_estimators}')

model = RandomForestClassifier()
parameters = {'max_depth': [10, 20, 30]}
grid_search = GridSearchCV(model, parameters, cv=5, scoring='accuracy')
grid_search.fit(X, y)

best_max_depth = grid_search.best_params_['max_depth']
print(f'Die ideale Tiefe ist {best_max_depth}')


# Aufteilung der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell erstellen und trainieren
model = RandomForestClassifier(
    max_depth=best_max_depth,
    n_estimators=best_n_estimators,
    random_state=42)

model.fit(X_train, y_train)

# Vorhersagen
y_pred = model.predict(X_test)

# Auswertung des Modells
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label=1, zero_division=1.0, average='weighted')
recall = recall_score(y_test, y_pred, pos_label=1, zero_division=1.0, average='weighted')
f1_score = f1_score(y_test, y_pred, pos_label=1, zero_division=1.0, average='weighted')

# Ergebnisse ausgeben
print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1-Score: {f1_score}')

# most important features with feauture names
feature_importances = pd.DataFrame(model.feature_importances_,
                                      index=X_train.columns,
                                        columns=['importance']).sort_values('importance', ascending=False)
print(feature_importances)