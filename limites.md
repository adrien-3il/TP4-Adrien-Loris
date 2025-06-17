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
