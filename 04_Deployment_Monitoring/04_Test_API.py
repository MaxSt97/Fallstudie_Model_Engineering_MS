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
