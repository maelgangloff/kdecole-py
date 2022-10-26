from .api_constants import ApiUrl, ApiVersion
from datetime import datetime
from requests import request

class Kdecole:
    def __init__(self, token: str, apiVersion: str = ApiVersion['PROD_MON_BUREAU_NUMERIQUE'], idEtablissement: int = 0, apiUrl: str = ApiUrl['PROD_MON_BUREAU_NUMERIQUE']) -> None:
        self.token = token
        self.apiVersion = apiVersion
        self.apiUrl = apiUrl
        self.idEtablissement = idEtablissement

    @staticmethod
    def login(username: str, password: str, apiVersion: str = ApiVersion['PROD_MON_BUREAU_NUMERIQUE'], apiUrl: str = ApiUrl['PROD_MON_BUREAU_NUMERIQUE']) -> str:
        """
        Demande à l'API de générer un nouveau jeton pour l'utilisateur
        """
        response = request(
            method = 'GET',
            url = apiUrl + f'/activation/{username}/{password}/',
            headers = {
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
        """
        return self.__kdecole('consulterReleves', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getActualites(self, idEleve: str = None) -> list:
        """
        Retourne un tableau des actualités de l'établissement de l'utilisateur
        """
        return self.__kdecole('actualites', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getContenuArticle(self, uid: str) -> dict:
        """
        Retourne le contenu d'un article. 
        Un article est publié par l'établissement.
        """
        return self.__kdecole('contenuArticle', f'article/{uid}').json()
    
    def getContenuInformation(self, uid: str) -> dict:
        """
        Retourne le contenu d'une information. 
        Une information est publiée par la plateforme EMS.
        """
        return self.__kdecole('contenuArticle', f'information/{uid}').json()
    
    def getTravailAFaire(self, idEleve: str = None, notBeforeDate: datetime = None) -> dict:
        """
        Retourne la liste des devoirs de l'élève.
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
        """
        parameter = None if idEleve == None else f'ideleve/{idEleve}'
        return self.__kdecole('contenuactivite', f'{parameter}/{uidSeance}/{uid}')
    
    def setActiviteFinished(self, uidSeance: int, uid: int, flagRealise: bool) -> dict:
        """
        Permet de marquer un devoir comme étant fait.
        """
        return self.__kdecole('contenuActivite', f'idetablissement/{self.idEtablissement}/{uidSeance}/{uid}', 'PUT', {
            'flagRealise': flagRealise
        })

    def getAbsences(self, idEleve: str = None) -> dict:
        """
        Retourne la liste des absences d'un élève
        """
        return self.__kdecole('consulterAbsences', None if idEleve == None else f'ideleve/{idEleve}').json()
    
    def getInfoUtilisateur(self, idEleve: str = None) -> dict:
        """
        Retourne les informations d'un utilisateur (type de compte, nom complet, numéro de l'établissement, etc.)
        """
        return self.__kdecole('infoutilisateur', None if idEleve == None else f'ideleve/{idEleve}').json()

    def getCalendrier(self, idEleve: str = None) -> dict:
        """
        Retourne l'emploi du temps de l'élève à J-7 et J+7
        """
        return self.__kdecole('calendrier', None if idEleve == None else f'ideleve/{idEleve}').json()
    
    def getNotes(self, idEleve: str = None) -> dict:
        """
        Retourne la liste des récentes notes de l'élève
        """
        return self.__kdecole('consulterNotes', None if idEleve == None else f'ideleve/{idEleve}').json()
    
    def getMessagerieInfo(self) -> dict:
        """
        Retourne l'état de la messagerie de l'utilisateur (nombre de mails non lus)
        """
        return self.__kdecole('messagerie/info').json()
    
    def getMessagerieBoiteReception(self, pagination: int = 0) -> dict:
        """
        Retourne les mails présents dans la boîte mail
        Le paramètre `pagination` permet de remonter dans le passé dans la liste des fils de discussions
        """
        return self.__kdecole('messagerie/boiteReception', pagination if pagination != 0 else None).json()
    
    def getCommunication(self, id: int) -> dict:
        """
        Retourne les détails d'un fil de discussion
        """
        return self.__kdecole('messagerie/communication', id)
    
    def reportCommunication(self, id: int):
        """
        Permet de signaler une communication
        """
        return self.__kdecole('messagerie/communication/signaler', id, 'PUT')
    
    def deleteCommunication(self, id: int):
        """
        Supprime la communication
        """
        return self.__kdecole('messagerie/communication/supprimer', id, 'DELETE')
    
    def setCommunicationLu(self, id: int):
        """
        Marquer une communication lue
        """
        return self.__kdecole('messagerie/communication/lu', id, 'PUT', {
            'action': 'lu'
        })
    
    def sendMessage(self, id: int, corpsMessage: str):
        """
        Envoyer un message sur un fil de discussion
        """
        return self.__kdecole('messagerie/communication/nouvelleParticipation', id, 'PUT', {
            'dateEnvoi': datetime.today().timestamp(),
            'corpsMessage': corpsMessage
        })

    def gestionAppels(self) -> dict:
        """
        Retourne les feuilles d'appel.
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
            url = self.apiUrl + (f'/{service}/{parameters}/' if parameters != None else f'/{service}/'),
            headers = {
                'X-Kdecole-Vers': self.apiVersion,
                'X-Kdecole-Auth': self.token,
            },
            method = method,
            json = json
        )
