from kdecolepy import Kdecole, ApiUrl, ApiVersion

'''
Programme pour lister les moyennes de l'élève à chaque matière
'''

token = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
ent = 'PROD_MON_BUREAU_NUMERIQUE'
idEtablissement = 0

idEleve = None

user = Kdecole(token, ApiVersion[ent], idEtablissement, ApiUrl[ent])
releve = user.getReleve(idEleve)

for trimestre in releve:
    for matiere in trimestre['matieres']:
        print(f'{trimestre["periodeLibelle"]} > {matiere["matiereLibelle"]}, Moyenne: {matiere["moyenneEleve"]}/{matiere["bareme"]}')
