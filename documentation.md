# Avon - Documentation
Afin d'utiliser Avon sur votre espace de travail, plusieurs choses sont à prévoir.
### Préparation & mise en place
- Avoir une machine Linux.
- [Python3](https://www.python.org/downloads/) d'installé.
- [pip](https://pip.pypa.io/en/stable/installing/) d'installé.
- [bencode](https://pypi.org/project/bencode.py/) d'installé.
- [python-magic](https://pypi.org/project/python-magic/) d'installé.
- Un dossier nommé `Avon` contenant un dossier `Testing` sur votre Bureau.
- Un fichier nommé `avon.py` dans le dossier `Avon` puis récupérer le contenu du fichier [avon.py](https://github.com/Inebhis/avon/blob/master/avon.py) afin de le mettre à l'intérieur.
- Un fichier `avon.service` puis récupérer le contenu du fichier [avon.service](https://github.com/Inebhis/avon/blob/master/avon.service) afin de le mettre à l'intérieur.
- Un fichier `avon.timer` puis récupérer le contenu du fichier [avon.timer](https://github.com/Inebhis/avon/blob/master/avon.timer) afin de le mettre à l'intérieur.
- Ouvrir un terminal et écrire : `sed 's/ben/{votre nom d'utilisateur}/g' avon.service`
- Toujours avec le terminal d'ouvert, écrire : `sudo mv avon.service /etc/systemd/system/ && sudo mv avon.timer /etc/systemd/system/`
- Écrire : `systemctl daemon-reload` suivi de `systemctl start avon.timer` dans votre terminal toujours ouvert.

Avon est désormais en place.
### Utilisation
L'utilisation d'Avon est extrêmement simple : glissez le fichier un fichier au choix dans le dossier `Testing` puis attendez quelques secondes.
Si le fichier reste dans le dossier, c'est qu'il n'y a priori aucun problème.
Vous pouvez néanmoins vérifier dans le fichier `notifications.log` se trouvant dans `Avalon/notifications/` pour voir s'il a bien été pris en compte.
