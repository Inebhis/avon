#!/bin/python3
import bencode
import datetime
import glob
import hashlib
import logging
import magic
import os
import requests


# RÉCUPÉRATION DE L'HOMEDIR
homedir = os.environ["HOME"]
path_dir = homedir + "/Bureau/Avon/"

bdd = path_dir + "bdd"
dir_notifications = path_dir + "notifications"

shitty_hash = path_dir + "bdd/shitty-hash.txt"
ok_hash = path_dir + "bdd/ok-hash.txt"
notifications = path_dir + "notifications/notifications.log"

# VÉRIFICATION SI LES DOSSIERS EXISTENT
if os.path.isdir(bdd):
    pass
else:
    os.mkdir(bdd)
    
if os.path.isdir(dir_notifications):
    pass
else:
    os.mkdir(dir_notifications)


# VÉRIFICATION SI LES FICHIERS EXISTENT
if os.path.isfile(shitty_hash):
    pass
else:
    with open(shitty_hash, "w"):
        pass

if os.path.isfile(ok_hash):
    pass
else:
    with open(ok_hash, "w"):
        pass

if os.path.isfile(notifications):
    pass
else:
    with open(notifications, "w"):
        pass


def quarantaine(file):
    """
    Mise en quarantaine
    """
    path = path_dir + "Quarantaine"

    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
        # os.chmod(path, 0o644)

    filename = file.rsplit("/", 1)[-1]

    os.replace(file, path + "/" + filename)


def antivirus(path):
    """
    Antivirus
    """
    if os.path.isfile(path):

        # DATE POUR LOG
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

        # FICHIER D'ENREGISTREMENT DES LOGS
        logging.basicConfig(
            filename=path_dir + "notifications/notifications.log", level=logging.DEBUG
        )

        # EXTENSION
        extension = path.rsplit(".", 1)[-1]

        # FILENAME
        filename = path.rsplit("/", 1)[-1]

        # MIME TYPE
        mime = magic.Magic(mime=True)
        true_mime = mime.from_file(path)

        # CHOIX DU HASH EN FONCTION DU TYPE DE FICHIER
        global true_hash
        true_hash = 1

        if extension != "torrent" and true_mime != "application/x-bittorrent":

            # HASH
            true_hash = hashlib.sha256(path.encode("utf-8")).hexdigest()

        else:
            # TORRENT FILE HASH
            torrent_file = open(path, "rb")
            metainfo = bencode.bdecode(torrent_file.read())
            info = metainfo["info"]
            true_hash = hashlib.sha1(bencode.bencode(info)).hexdigest()

        # API VIRUS TOTAL
        params = {
            "apikey": "98f28ece097a7f676e85cfe1148955b9a38eb70e8be7107a6dd3bb4fc824a097",
            "resource": path,
        }
        url = requests.get(
            "https://www.virustotal.com/vtapi/v2/file/report", params=params
        )
        json_response = url.json()
        response = int(json_response.get("response_code"))

        # VÉRIFICATION SI HASH DANS BDD
        if true_hash in open(path_dir + "bdd/shitty-hash.txt").read():

            quarantaine(path)
            logging.warning(
                " ".join(
                    [
                        date_time,
                        ": Le hash du fichier",
                        filename,
                        "est reconnu comme malveillant.",
                    ]
                )
            )

        elif true_hash in open(path_dir + "bdd/ok-hash.txt").read():

            logging.info(
                " ".join([date_time, ": Le hash du fichier", filename, "est sécurisé."])
            )

        else:

            # VÉRIFICATION VIRUS TOTAL
            if response != 0:
                f = open(path_dir + "bdd/shitty-hash.txt", "a")
                f.write(true_hash + "\n")
                quarantaine(path)
                logging.warning(
                    " ".join(
                        [
                            date_time,
                            ": Le hash du fichier",
                            filename,
                            "est reconnu comme malveillant par Virus Total.",
                        ]
                    )
                )

            else:

                # VÉRIFICATION SI EXTENSION = MIME TYPE
                if (
                    extension == "jpeg"
                    and true_mime == "image/jpeg"
                    or extension == "jpg"
                    and true_mime == "image/jpg"
                    or extension == "png"
                    and true_mime == "image/png"
                ):

                    logging.info(
                        " ".join(
                            [
                                date_time,
                                ": Le fichier",
                                filename,
                                "est sécurisé. Hash ajouté à la BDD.",
                            ]
                        )
                    )
                    f = open(path_dir + "bdd/ok-hash.txt", "a")
                    f.write(date_time + " " + path + " : " + true_hash + "\n")

                elif extension == "torrent" and true_mime == "application/x-bittorrent":

                    logging.info(
                        " ".join(
                            [
                                date_time,
                                ": Le fichier .torrent",
                                filename,
                                "est sécurisé. Hash ajouté à la BDD.",
                            ]
                        )
                    )
                    f = open(path_dir + "bdd/ok-hash.txt", "a")
                    f.write(date_time + " " + path + " : " + true_hash + "\n")

                elif (
                    extension == "py"
                    and true_mime in {"text/x-python", "text/plain"}
                    or extension == "pyc"
                    and true_mime == "application/x-python-code"
                ):

                    with open(path) as f:
                        if (
                            "import requests" in f.read()
                            or "import httplib" in f.read()
                            or "import urllib" in f.read()
                            or "os.system" in f.read()
                            or "subprocess." in f.read()
                        ):
                            logging.warning(
                                " ".join(
                                    [
                                        date_time,
                                        ": Le fichier",
                                        filename,
                                        "est malveillant. Hash ajouté à la BDD.",
                                    ]
                                )
                            )
                            f = open(path_dir + "bdd/shitty-hash.txt", "a")
                            f.write(date_time + " " + path + " : " + true_hash + "\n")
                            quarantaine(path)

                        else:
                            logging.info(
                                " ".join(
                                    [
                                        date_time,
                                        ": Le fichier .torrent",
                                        filename,
                                        "est sécurisé. Hash ajouté à la BDD.",
                                    ]
                                )
                            )
                            f = open(path_dir + "bdd/ok-hash.txt", "a")
                            f.write(date_time + " " + path + " : " + true_hash + "\n")

                else:

                    logging.warning(
                        " ".join(
                            [
                                date_time,
                                ": Le fichier",
                                filename,
                                "est malveillant. Hash ajouté à la BDD.",
                            ]
                        )
                    )
                    f = open(path_dir + "bdd/shitty-hash.txt", "a")
                    f.write(date_time + " " + path + " : " + true_hash + "\n")
                    quarantaine(path)

    else:

        logging.error(" ".join(["Aucun fichier de disponible pour Avon"]))


# AVOIR LE DERNIER FICHIER D'UN DOSSIER
list_of_files = glob.glob("/home/nibheis/Bureau/Avon/Testing/*")
latest_file = max(list_of_files, key=os.path.getctime)

tests = path_dir + "bdd/fichiers_testes"
if os.path.isfile(tests):
    pass
else:
    with open(tests, "w"):
        pass

with open(tests) as f:
    if latest_file in f.read():
        pass
    else:
        antivirus(latest_file)
        f = open(tests, "a")
        f.write(latest_file + "\n")
