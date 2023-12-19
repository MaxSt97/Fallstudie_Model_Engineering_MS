from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, make_scorer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
import pandas as pd
import pickle

# Einlesen der Daten PSP_Jan_Feb_2019_preprocessed
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

# Definieren der Hyperparameter-Räume für die zufällige Suche
param_dist = {
    'n_estimators': randint(50, 300),  # Beispiel für eine kontinuierliche Verteilung
    'max_depth': [10, 20, 30,40,50,60],
    'min_samples_split': [2, 3, 4,5,6,7],
    'min_samples_leaf': [1, 2, 3,4,5,6]
}

# Verwenden Sie RandomizedSearchCV anstelle von GridSearchCV
random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=10, cv=5, scoring='accuracy', random_state=42)

# Führen Sie die zufällige Suche durch
random_search.fit(X, y)

# Holen Sie sich die besten Hyperparameter
best_params = random_search.best_params_

# Zuweisen der Parameter
best_n_estimators = best_params['n_estimators']
best_max_depth = best_params['max_depth']
best_min_samples_split = best_params['min_samples_split']
best_min_samples_leaf = best_params['min_samples_leaf']

# Zeigen Sie die besten Hyperparameter an
print("Die besten Hyperparameter sind:", best_params)

# Aufteilung der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell erstellen und trainieren
model = RandomForestClassifier(
    max_depth=best_max_depth,
    n_estimators=best_n_estimators,
    min_samples_split= best_min_samples_split,
    min_samples_leaf=best_min_samples_leaf,
    random_state=42)

model.fit(X_train, y_train)

# Vorhersagen
y_pred = model.predict(X_test)

# Auswertung des Modells
accuracy = round(accuracy_score(y_test, y_pred),2)
precision = round(precision_score(y_test, y_pred, zero_division=1.0, average='weighted'),2)
recall = round(recall_score(y_test, y_pred, zero_division=1.0, average='weighted'),2)
f1_score = round(f1_score(y_pred,y_test,zero_division=1.0,average='weighted'),2)

# Ergebnisse ausgeben
print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1-Score: {f1_score}')

# Relevante Features ausgeben
feature_importances = pd.DataFrame(model.feature_importances_,
                                      index=X_train.columns,
                                        columns=['importance']).sort_values('importance', ascending=False)
print(feature_importances)

# Modell speichern für die weitere Verwendung
pickle.dump(model, open('../model.pkl', 'wb'))

