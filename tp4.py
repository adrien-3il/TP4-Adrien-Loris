# Nécessite l'installation de Flask : pip install Flask
from flask import Flask, request, jsonify, make_response
import datetime

# 1. Initialisation de l'application Flask
app = Flask(__name__)

# 2. "Base de données" en mémoire
# Un set pour les pseudos pour garantir l'unicité et une recherche rapide.
pseudos = set()
# Une liste pour stocker les messages dans l'ordre.
messages = []

# 3. Définition des routes de l'API

@app.route("/")
def index():
    """
    Route d'accueil qui décrit l'API.
    """
    api_info = {
        "description": "API pour un service de chat type IRC (CanaDuck)",
        "version": "1.0",
        "endpoints": {
            "GET /motd": "Affiche le message du jour.",
            "POST /nick": "Enregistre un nouveau pseudo. Corps JSON attendu : {'pseudo': 'votre_nom'}",
            "POST /msg": "Envoie un message. Corps JSON attendu : {'from': 'votre_nom', 'message': 'votre_message'}",
            "GET /msg": "Affiche tous les messages du canal."
        }
    }
    return jsonify(api_info)

@app.route('/motd', methods=['GET'])
def get_motd():
    """
    Étape 1 : Répondre avec un message de bienvenue.
    """
    # jsonify() prépare une réponse JSON avec le bon Content-Type.
    return jsonify({"motd": "Bienvenue sur CanaDuck!"})

@app.route('/nick', methods=['POST'])
def register_nick():
    """
    Étape 2 : Enregistrer un pseudo utilisateur.
    """
    # On récupère les données JSON envoyées dans la requête.
    data = request.get_json()

    # Validation : on vérifie si le JSON et la clé 'pseudo' sont présents.
    if not data or 'pseudo' not in data:
        return jsonify({"error": "Le champ 'pseudo' est manquant dans le corps JSON."}), 400

    pseudo = data['pseudo']

    # Validation supplémentaire : le pseudo ne doit pas être vide.
    if not pseudo or not isinstance(pseudo, str) or not pseudo.strip():
        return jsonify({"error": "Le pseudo ne peut pas être vide."}), 400
        
    # On vérifie si le pseudo est déjà pris.
    if pseudo in pseudos:
        # 409 Conflict est un code plus approprié pour une ressource qui existe déjà.
        return jsonify({"error": f"Le pseudo '{pseudo}' est déjà utilisé."}), 409

    # Si tout est bon, on l'ajoute à notre set.
    pseudos.add(pseudo)
    
    # 200 OK pour une ressource modifiée/créée avec succès.
    return jsonify({"status": "ok", "pseudo_enregistre": pseudo}), 200

@app.route('/msg', methods=['POST'])
def post_message():
    """
    Étape 3 : Envoyer un message.
    """
    data = request.get_json()

    # Validation : on vérifie la présence des clés 'from' et 'message'.
    if not data or 'from' not in data or 'message' not in data:
        return jsonify({"error": "Les champs 'from' et 'message' sont requis."}), 400
    
    sender = data['from']
    message_content = data['message']

    # Validation : on vérifie que l'expéditeur est un pseudo enregistré.
    if sender not in pseudos:
        # 403 Forbidden : l'action est comprise mais refusée.
        return jsonify({"error": f"Le pseudo '{sender}' n'est pas enregistré. Utilisez POST /nick d'abord."}), 403

    # On crée le dictionnaire du message avec un timestamp.
    new_message = {
        "from": sender,
        "message": message_content,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z" # Format ISO 8601
    }
    
    messages.append(new_message)
    
    # 201 Created est le code standard pour une nouvelle ressource créée avec succès.
    return jsonify({"status": "message recu"}), 201

@app.route('/msg', methods=['GET'])
def get_messages():
    """
    Étape 4 (facultative) : Lire tous les messages.
    """
    # On retourne simplement la liste complète des messages.
    return jsonify(messages)

# 4. Lancement du serveur
if __name__ == '__main__':
    # Le serveur écoute sur toutes les interfaces (0.0.0.0) sur le port 8080.
    # debug=True active le rechargement automatique et des messages d'erreur détaillés.
    app.run(host='0.0.0.0', port=8080, debug=True)