from fiche_perso import LotPersonnage


msg= "Veillez choisir un nom*, un age et une liste d'objets en votre possessions. *Obligatoire."
print(msg)
print("\tNotez vos possessions, séparées par une virgule.")

infos = {
    'nom': " ",
    'age': "",
    'possessions': []
    }

for key in infos.keys():
    msg_ = key.capitalize() + " :\n"
    ipt = input(msg_)
    if key == 'possessions':
        splitted = ipt.split(',')
        print(splitted)
        value = [i.lower().strip() for i in splitted]
    else:
        value = ipt.lower().strip()
    infos[key] = value

lot = LotPersonnage(infos["nom"], infos["age"], infos["possessions"])
print(lot.lot_str())
lot.export()