from kdecolepy import Kdecole, ApiUrl, ApiVersion

'''
Programme permettant de générer un jeton d'authentification
'''

username = 'username'
password = 'unique_password'
ent = 'PROD_MON_BUREAU_NUMERIQUE'

token = Kdecole.login(username, password, ApiVersion[ent], ApiUrl[ent])
print(f'''{token}
ATTENTION: Ce token octroie un accès critique à votre compte et ne doit donc jamais être transmis à un tiers.''')
