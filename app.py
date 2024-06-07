import cohere
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Remplacez par votre propre clé API
co = cohere.Client(api_key="")

@app.route("/hello")
def hello_world():
    result = ""
    for event in co.chat_stream(message="What is an LLM?"):
        if event.event_type == "text-generation":
            result += event.text
        elif event.event_type == "stream-end":
            return result

@app.route("/", methods=["POST"])
def handle_question():
    try:
        # Récupérer le JSON de la requête POST
        data = request.get_json()
        
        # Vérifier que le paramètre 'question' est présent
        if 'question' not in data:
            return jsonify({"error": "Le paramètre 'question' est requis"}), 400
        
        # Extraire la question
        question = data['question']
        
        # Initialiser une chaîne de réponse
        result = ""
        
        # Utiliser le chat_stream de Cohere pour obtenir la réponse
        for event in co.chat_stream(message=question):
            if event.event_type == "text-generation":
                result += event.text
            elif event.event_type == "stream-end":
                break
        # Retourner la réponse en format JSON
        return jsonify({"response": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
