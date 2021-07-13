from fiche_perso import LotPersonnage


msg= """Pour générer une fiche de personnage, veillez entrer les inforamtions correspondantes.
\t-Le métier de votre personnage. (Exemples: aventurier·e ou Mage d'Aria)
\t-Le prénom et nom. (Exemple: Clodomir de Cuivrechamps).
\t-L'âge (5ans ou 172ans).
\t-Les objets en sa possessions, séparés par une virgule (Exemple: "Lanterne, bâton de marche, bourse vide, clef rouillée")."""

infos = {
    'metier': "",
    'nom': "",
    'age': "",
    'possessions': []
    }

print(msg)

for key in infos.keys():
    msg_ = key.capitalize() + " :  "
    ipt = input(msg_)
    if key == 'possessions':
        splitted = ipt.split(',')
        value = [i.lower().strip() for i in splitted]
    else:
        value = ipt.lower().strip()
    infos[key] = value

lot = LotPersonnage(infos["metier"], infos["nom"], infos["age"], infos["possessions"])
print(lot.lot_str())
lot.export()