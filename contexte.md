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
