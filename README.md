# TP4-Adrien-Loris

## 0-contexte

### 3.1 Session, état, communication

1. Dans un modèle TCP, chaque client conserve une connexion ouverte. HTTP, en revanche, est sans mémoire. Comment réconcilier cette absence de session avec un système comme l’IRC, fondé sur un état utilisateur persistant ?
Il faut simuler une session. Cela peut se faire en transmettant une information d’identification (comme un pseudo ou un token) à chaque requête HTTP, puisque HTTP ne maintient pas de connexion continue comme TCP.

2. Peut-on envisager un système où le pseudo est redonné à chaque requête ? Quelles alternatives (cookies, token, paramètre URL) sont envisageables ? Quelles implications en termes de sécurité et d’ergonomie ?
Oui, redonner le pseudo à chaque requête est possible. Sinon, on peut utiliser des cookies, des tokens d’authentification (JWT) ou passer l’identifiant en paramètre URL. Ces solutions demandent des vérifications de sécurité (éviter l’usurpation d’identité) et peuvent affecter l’ergonomie si le client ne gère pas automatiquement l’identification.

3. Dans un serveur TCP, on peut “pousser” des messages. HTTP ne permet pas cela nativement. Quelles solutions techniques peut-on envisager pour permettre aux clients de recevoir de nouveaux messages ?
On peut utiliser du polling (le client interroge régulièrement le serveur), du long-polling (le serveur garde la connexion ouverte jusqu’à ce qu’il ait une réponse), ou encore des WebSockets, qui permettent une communication bidirectionnelle persistante.
3.2 Ressources, verbes, structure

4. Une commande comme /join #pause_cafe devient-elle une requête POST ? Sur quelle route ? Avec quel corps JSON ?
Oui, cela peut devenir une requête POST vers /canaux/pause_cafe/join, avec un corps JSON indiquant le pseudo : { "pseudo": "roger" }.

5. Si /msg devient une ressource, que renvoie un GET /msg ? Tous les messages ? Seulement ceux du canal courant ? Et dans quel ordre ?
Un GET /msg pourrait renvoyer les derniers messages du canal actif de l’utilisateur. L’ordre serait chronologique, du plus ancien au plus récent. La logique métier (filtrage par canal, utilisateur, etc.) serait placée côté serveur, dans le gestionnaire de la route.

6. Comment structurer les URLs ? Quel niveau de hiérarchie est pertinent ? Quelles conventions de nommage adopter ?
Une hiérarchie claire pourrait être : /canaux, /canaux/general, /canaux/general/messages. Cela reflète bien les relations entre ressources. Les noms doivent être en minuscules, sans caractères spéciaux, et refléter les entités manipulées.
3.3 Robustesse, concurrence, évolutivité

7. Si deux utilisateurs envoient un POST /msg en même temps, comment garantir que l’ordre d’arrivée est conservé ?
Il faut gérer un verrou ou une file de traitement côté serveur. Des mécanismes comme des timestamps ou des queues asynchrones peuvent aussi garantir l’ordre.

8. Le serveur TCP conserve tout l’état en mémoire. Un service Web doit-il faire pareil ?
Non. Un service Web devrait persister les données (messages, états) dans une base de données ou un autre stockage pour assurer la continuité entre les requêtes et permettre la scalabilité.

9. Chaque appel HTTP crée une connexion, lit, écrit, ferme. Quel impact sur la charge réseau et CPU ?
Cette mécanique est plus coûteuse que TCP persistant. À partir d’un certain nombre d’utilisateurs simultanés (des centaines ou milliers), cela peut créer une surcharge. Il faut alors optimiser ou utiliser des solutions comme les connexions keep-alive, du caching, ou des serveurs plus performants.


## 1-limites

### 2.1 Structure du code et organisation

1. Si l’API grossit, peut-on continuer à garder tout dans un seul fichier Python ?
Non, cela devient vite illisible et difficile à maintenir. Il est préférable de modulariser.

2. Peut-on regrouper les routes par thème dans des fichiers séparés ?
Oui, c’est même recommandé. On peut séparer les routes en fichiers comme user_api.py, message_api.py, etc.

3. Quels seraient les avantages d’avoir un fichier user_api.py, un message_api.py, etc. ?
Cela améliore la lisibilité, la maintenance, les tests unitaires, et permet à plusieurs personnes de travailler sur le projet sans se gêner.

4. Comment tester uniquement la logique des pseudos sans lancer tout le serveur ?
En isolant cette logique dans une fonction ou une classe testable indépendamment, on peut l’appeler dans des tests unitaires sans serveur HTTP.

5. Peut-on documenter automatiquement une API répartie dans plusieurs fichiers ?
Oui, avec des outils comme Swagger ou FastAPI, qui permettent d’extraire la documentation depuis le code.


### 2.2 Isolation des responsabilités


1. Que se passerait-il si l’on voulait remplacer uniquement la gestion des pseudos ?
Si cette partie est bien isolée, on peut la remplacer facilement sans toucher au reste du code. Sinon, cela casse tout.

2. Est-il possible d’utiliser la même API d’authentification dans une autre application CanaDuck ?
Oui, si elle est conçue comme un composant ou un microservice indépendant.

3. Quels composants doivent absolument partager des données pour fonctionner ?
Les utilisateurs et les canaux ont besoin de connaître les messages ; donc ces composants partagent des données. La synchronisation doit être assurée.

4. Peut-on définir des frontières entre composants indépendants ?
Oui. On peut découper par fonction (authentification, messages…), par équipe (front, back…), ou par métier (utilisateur, canal…).

5. Comment éviter que deux composants interdépendants deviennent un nouveau monolithe caché ?
En définissant des interfaces claires, en limitant les dépendances croisées, et en utilisant des communications asynchrones ou via API explicite.
2.3 Déploiement et scalabilité

   

1. Est-ce qu’on pourrait lancer la gestion des utilisateurs sur un autre port ? Dans un autre fichier ?
Oui, avec un serveur dédié ou un microservice. Cela permet une meilleure isolation et scalabilité.

2. Quels bénéfices à déployer un composant critique (/msg) sur deux serveurs ?
Cela améliore la disponibilité (redondance), permet la répartition de charge, et limite les interruptions de service.

3. Peut-on mettre à jour une partie du code sans relancer toute l’application ?
Oui, si les composants sont bien séparés. Les mises à jour peuvent se faire indépendamment.

4. Si on veut créer une version mobile de l’application, quels morceaux garderait-on ?
On garderait l’API REST. L’interface mobile consommerait les mêmes routes. Seule la partie affichage serait réécrite.

5. Quels outils pourraient aider à orchestrer plusieurs services ?
Des outils comme Docker, Docker Compose, ou Kubernetes permettent de gérer plusieurs services, leur déploiement, et leur communication.


### 2.4 Communication et cohérence


1. Si on découpe les services, comment vont-ils discuter entre eux ?
Ils peuvent communiquer via HTTP, via des files de messages (comme RabbitMQ), ou via une API Gateway.

2. Que devient l’état partagé si chaque service a sa propre mémoire ?
Il faut utiliser une base de données ou un cache commun pour synchroniser les états. Sinon, la cohérence est difficile à maintenir.

3. Faut-il stocker certaines informations dans une base commune ? Dans une file de messages ?
Oui, une base partagée permet d’assurer la persistance. Une file de messages (Kafka, RabbitMQ…) permet une communication asynchrone fiable.

4. Comment gérer les erreurs si un service est indisponible ?
Il faut prévoir des retries automatiques, un système de file d’attente, ou une gestion de dégradation (fallback).

5. Peut-on garantir la cohérence globale sans que chaque service connaisse les autres ?
Oui, à condition d’utiliser des mécanismes de coordination comme des événements ou des contrats d’interface, tout en minimisant les dépendances directes.
