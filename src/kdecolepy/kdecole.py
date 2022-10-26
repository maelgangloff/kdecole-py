from .api_constants import ApiUrl, ApiVersion
from datetime import datetime
from requests import request


class Kdecole:
    def __init__(self, token: str, apiVersion: str = ApiVersion['PROD_MON_BUREAU_NUMERIQUE'], idEtablissement: int = 0,
                 apiUrl: str = ApiUrl['PROD_MON_BUREAU_NUMERIQUE']) -> None:
        self.token = token
        self.apiVersion = apiVersion
        self.apiUrl = apiUrl
        self.idEtablissement = idEtablissement

    @staticmethod
    def login(username: str, password: str, apiVersion: str = ApiVersion['PROD_MON_BUREAU_NUMERIQUE'],
              apiUrl: str = ApiUrl['PROD_MON_BUREAU_NUMERIQUE']) -> str:
        """
        Demande à l'API de générer un nouveau jeton pour l'utilisateur
        :param str username: Nom d'utilisateur
        :param str password: Mot de passe temporaire
        :param str apiVersion: Version de l'application mobile
        :param str apiUrl: URL du serveur de l'API
        :rtype str
        :return: Renvoie un jeton d'authentification
        """
        response = request(
            method='GET',
            url=apiUrl + f'/activation/{username}/{password}/',
            headers={
                'X-Kdecole-Auth': '',
                'X-Kdecole-Vers': apiVersion
            }
        ).json()
        if response['success']:
            return response['authtoken']
        raise Exception("L'authentification n'a pas fonctionné.")

    def starting(self) -> True:
        """
        Cet appel est initialement réalisé par l'application mobile pour vérifier si le token et la version de l'app sont valides.
        Le serveur retourne un code de statut `HTTP 204 No Content` si l'utilisateur est correctement authentifié.
        """
        response = self.__kdecole('starting').json()
        if response.status_code == 403:
            raise Exception("L'utilisateur ne semble pas être correctement authentifié.")
        elif response.status_code != 204:
            raise Exception("Erreur d'appel à l'API.")
        return True

    def logout(self) -> True:
        """
        Révoque le jeton d'accès
        """
        response = self.__kdecole('desactivation')
        if not response['success']:
            raise Exception("Une erreur est survenue lors de la déconnexion.")
        return True

    def getReleve(self, idEleve: str = None) -> list:
        """
        Retourne le relevé de notes de l'élève
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype list
        :return: Renvoie une liste contenant les trimestres
        """
        return self.__kdecole('consulterReleves', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getActualites(self, idEleve: str = None) -> list:
        """
        Retourne les actualités de l'établissement de l'utilisateur
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype list
        :return: Renvoie une liste contenant des actualités
        """
        return self.__kdecole('actualites', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getContenuArticle(self, uid: str) -> dict:
        """
        Retourne le contenu d'un article.
        Un article est publié par l'établissement.
        :param str uid: Identifiant unique de l'article
        :rtype dict
        :return: Renvoie les informations d'un article
        """
        return self.__kdecole('contenuArticle', f'article/{uid}').json()

    def getContenuInformation(self, uid: str) -> dict:
        """
        Retourne le contenu d'une information.
        Une information est publiée par la plateforme EMS.
        :param str uid: Identifiant unique d'une information
        :rtype dict
        :return: Renvoie le détail d'une information
        """
        return self.__kdecole('contenuArticle', f'information/{uid}').json()

    def getTravailAFaire(self, idEleve: str = None, notBeforeDate: datetime = None) -> dict:
        """
        Retourne la liste des devoirs de l'élève.
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :param datetime or None notBeforeDate: Ne renvoyer que les devoirs après cette datetime
        :rtype dict
        :return: Renvoie le travail à faire
        """
        if idEleve == None:
            if notBeforeDate == None:
                parameter = f'idetablissement/{self.idEtablissement}'
            else:
                parameter = f'idetablissement/{self.idEtablissement}/{int(notBeforeDate.timestamp() * 1e3)}'
        else:
            if notBeforeDate == None:
                parameter = f'ideleve/{idEleve}'
            else:
                parameter = f'ideleve/{idEleve}/{int(notBeforeDate.timestamp() * 1e3)}'
        return self.__kdecole('travailAFaire', parameter).json()

    def getContenuActivite(self, uidSeance: int, uid: int, idEleve: str = None) -> dict:
        """
        Retourne les détails d'un devoir à faire.
        :param int uidSeance: Identifiant unique de la séance à considérer
        :param int uid: Identifiant unique de l'activité
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype dict
        :return: Renvoie le détail d'une activité
        """
        parameter = None if idEleve == None else f'ideleve/{idEleve}'
        return self.__kdecole('contenuactivite', f'{parameter}/{uidSeance}/{uid}')

    def setActiviteFinished(self, uidSeance: int, uid: int, flagRealise: bool) -> dict:
        """
        Permet de marquer un devoir comme étant fait.
        :param int uidSeance: Identifiant unique de la séance à considérer
        :param int uid: Identifiant unique du travail à faire
        :param bool flagRealise: Réalisé ?
        :rtype dict
        :return: Renvoie la confirmation du changement
        """
        return self.__kdecole('contenuActivite', f'idetablissement/{self.idEtablissement}/{uidSeance}/{uid}', 'PUT', {
            'flagRealise': flagRealise
        })

    def getAbsences(self, idEleve: str = None) -> dict:
        """
        Retourne la liste des absences d'un élève
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype dict
        :return: Renvoie les absences
        """
        return self.__kdecole('consulterAbsences', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getInfoUtilisateur(self, idEleve: str = None) -> dict:
        """
        Retourne les informations d'un utilisateur (type de compte, nom complet, numéro de l'établissement, etc.)
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype dict
        :return: Renvoie les informations de l'utilisateur connecté
        """
        return self.__kdecole('infoutilisateur', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getCalendrier(self, idEleve: str = None) -> dict:
        """
        Retourne l'emploi du temps de l'élève à J-7 et J+7
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype dict
        :return: Renvoie l'emploi du temps de l'élève
        """
        return self.__kdecole('calendrier', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getNotes(self, idEleve: str = None) -> dict:
        """
        Retourne la liste des récentes notes de l'élève
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype dict
        :return: Renvoie les dernière notes
        """
        return self.__kdecole('consulterNotes', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getMessagerieInfo(self) -> dict:
        """
        Retourne l'état de la messagerie de l'utilisateur (nombre de mails non lus)
        :param str or None idEleve: Identifiant de l'élève à sélectionner
        :rtype dict
        :return: Renvoie les infos générales de la messagerie
        """
        return self.__kdecole('messagerie/info').json()

    def getMessagerieBoiteReception(self, pagination: int = 0) -> dict:
        """
        Retourne les mails présents dans la boîte mail
        Le paramètre `pagination` permet de remonter dans le passé dans la liste des fils de discussions
        :param int pagination: Nombre de mails à ne pas renvoyer
        :rtype dict
        :return: Les mails contenus dans la boite de réception
        """
        return self.__kdecole('messagerie/boiteReception', pagination if pagination != 0 else None).json()

    def getCommunication(self, id: int) -> dict:
        """
        Retourne les détails d'un fil de discussion
        :param int id: Identifiant unique du fil de discussion
        :rtype dict
        :return: Le détail d'un fil de discussion
        """
        return self.__kdecole('messagerie/communication', id)

    def reportCommunication(self, id: int):
        """
        Signaler un fil de discussion
        :param int id: Identifiant unique du fil de discussion
        """
        return self.__kdecole('messagerie/communication/signaler', id, 'PUT')

    def deleteCommunication(self, id: int):
        """
        Supprimer un fil de discussion
        :param int id: Identifiant unique du fil de discussion
        """
        return self.__kdecole('messagerie/communication/supprimer', id, 'DELETE')

    def setCommunicationLu(self, id: int):
        """
        Marquer une communication lue
        :param int id: Identifiant unique du fil de discussion
        """
        return self.__kdecole('messagerie/communication/lu', id, 'PUT', {
            'action': 'lu'
        })

    def sendMessage(self, id: int, corpsMessage: str):
        """
        Envoyer un message sur un fil de discussion
        :param int id: Identifiant unique du fil de discussion
        :param corpsMessage: Corps brut du message
        """
        return self.__kdecole('messagerie/communication/nouvelleParticipation', id, 'PUT', {
            'dateEnvoi': datetime.today().timestamp(),
            'corpsMessage': corpsMessage
        })

    def gestionAppels(self) -> dict:
        """
        Retourne les feuilles d'appel.
        :rtype dict
        :return: Renvoie les feuilles d'appel
        """
        return self.__kdecole('gestionAppels')

    def __kdecole(self, service: str, parameters: str = None, method: str = 'GET', json: dict = {}):
        if parameters == None and service not in ['desactivation',
                                                  'messagerie/info',
                                                  'messagerie/communication',
                                                  'messagerie/boiteReception',
                                                  'starting',
                                                  'infoutilisateur'
                                                  ]:
            parameters = f'idetablissement/{self.idEtablissement}'
        return request(
            url=self.apiUrl + (f'/{service}/{parameters}/' if parameters != None else f'/{service}/'),
            headers={
                'X-Kdecole-Vers': self.apiVersion,
                'X-Kdecole-Auth': self.token,
            },
            method=method,
            json=json
        )
