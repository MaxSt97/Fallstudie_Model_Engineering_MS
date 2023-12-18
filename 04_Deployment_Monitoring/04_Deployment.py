from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Laden Sie das trainierte Modell
model = pickle.load(open('../model.pkl', 'rb'))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Annahme: Das JSON enthält ein Array von Features (Beispiel: [feature1, feature2, ...])
        features = np.array(request.json['features']).reshape(1, -1)

        # Vorhersage mit dem geladenen Modell
        prediction = model.predict(features)

        # Rückgabe der Vorhersage als JSON
        return jsonify({'prediction': str(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    # Hier können Sie den Host und den Port nach Bedarf konfigurieren
    app.run(host='0.0.0.0', port=5000)


import requests

# URL des lokalen Flask-Servers
api_url = 'http://127.0.0.1:5000/predict'

# Benutzeroberfläche im Terminal
while True:
    try:
        # Benutzereingabe für Features
        features_input = input("Geben Sie die Features als kommaseparierte Werte ein (z.B. 1.2,3.4,5.6): ")
        features = [float(f) for f in features_input.split(',')]

        # Senden der POST-Anfrage an die API
        response = requests.post(api_url, json={'features': features})

        # Verarbeitung der API-Antwort
        if response.status_code == 200:
            result = response.json()
            print(f"Vorhersage: {result['prediction']}")
        else:
            print(f"Fehler bei der Anfrage: {response.text}")

    except Exception as e:
        print(f"Fehler: {e}")

    # Benutzerabfrage für eine weitere Anfrage
    another_request = input("Weitere Anfrage senden? (j/n): ").lower()
    if another_request != 'j':
        break
