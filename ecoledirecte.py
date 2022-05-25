import json
import os
import sys

import requests
import time
import getpass


def login():
    username = str(input("Nom d'utilisateur EcoleDirecte : "))
    password = getpass.getpass(prompt="Mot de passe EcoleDirecte : ")

    connection_url = 'https://api.ecoledirecte.com/v3/login.awp'
    connection_obj = 'data={"identifiant": "' + username + '", "motdepasse": "' + password + '"}'

    connection_request = requests.post(connection_url, data=connection_obj)  # Envoie la requête
    return connection_request;

def getTrimesteData(account_token, account_data):
    trimestre = int(input('Sur quel trimestre vous voudrez voir votre moyenne ?\n1 = Trimestre 1\n2 = Trimestre 2\n3 = Trimestre 3\n4 = Année\n'))

    url = 'https://api.ecoledirecte.com/v3/eleves/' + str(account_data['id']) + '/notes.awp?verbe=get&'
    data = 'data={"token": "' + account_token + '"}'
    request = requests.post(url, data=data)
    data = json.loads(request.text)

    if trimestre == 1:
        getDataOfTrimestre = data['data']['periodes'][0]
    elif trimestre == 2:
        getDataOfTrimestre = data['data']['periodes'][1]
    elif trimestre == 3:
        getDataOfTrimestre = data['data']['periodes'][2]
    elif trimestre == 4:
        getDataOfTrimestre = data['data']['periodes'][3]

    clotured = getDataOfTrimestre['cloture']
    class_average = getDataOfTrimestre['ensembleMatieres']['moyenneClasse']
    general_average = getDataOfTrimestre['ensembleMatieres']['moyenneGenerale']
    max_average = getDataOfTrimestre['ensembleMatieres']['moyenneMax']
    min_average = getDataOfTrimestre['ensembleMatieres']['moyenneMin']

    print("\n\n═════════════════════════════════════════════════════════")
    print("Information - " + getDataOfTrimestre['periode'])
    if clotured:
        print("Trimestre actuellement fermé")
    print("Moyenne de la classe : " + str(class_average))
    print("Ta moyenne générale : " + str(general_average))
    print("Moyenne minimale : " + str(min_average))
    print("Moyenne maximal : " + str(max_average))
    print("═════════════════════════════════════════════════════════\n\n")

    getTrimesteData(account_token, account_data)

def main():
    loginResponse = login()
    if '"code":200' in loginResponse.text:
        connection_data = json.loads(loginResponse.text)

        account_token = connection_data['token']  # Récupération du Jetons de connection
        account_data = connection_data['data']['accounts'][0]  # Récupération des données de l'utilisateur

        getTrimesteData(account_token, account_data)
    else:
        print("\nNom d'utilisateur ou mot de passe invalide !\n")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)