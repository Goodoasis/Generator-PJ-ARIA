from os import path
from random import randint
from math import floor

from pdf_exporter import EXPORT_PATH, PdfExporter

NOMBRE_TIRAGE = 3


class Personnage():

    @staticmethod
    def verify_age(age):
        """Return "" if name not an interger"""
        try:
            age_ = int(age)
            if age_ < 1:
                age_ = age_ * -1
        except ValueError:
            age_ = ""

        return str(age_)

    @staticmethod
    def artisanat(inst):
        return floor((inst.carac["dexterite"] + inst.carac["intelligence"])/2) *5

    @staticmethod
    def combat(inst):
        return floor((inst.carac["force"] + inst.carac["dexterite"])/2) *5

    @staticmethod
    def combat_distance(inst):
        return floor((inst.carac["dexterite"] + inst.carac["intelligence"])/2) *5

    @staticmethod
    def connais_nature(inst):
        return floor((inst.carac["dexterite"] + inst.carac["intelligence"])/2) *5

    @staticmethod
    def connais_secrets(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def courir(inst):
        return floor((inst.carac["dexterite"] + inst.carac["endurance"])/2) *5

    @staticmethod
    def discretion(inst):
        return floor((inst.carac["dexterite"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def droit(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def esquiver(inst):
        return floor((inst.carac["dexterite"] + inst.carac["intelligence"])/2) *5

    @staticmethod
    def intimider(inst):
        return floor((inst.carac["force"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def lire(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def mentir(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def perception(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def piloter(inst):
        return floor((inst.carac["dexterite"] + inst.carac["endurance"])/2) *5
        
    @staticmethod
    def psychologie(inst):
        return floor((inst.carac["endurance"] + inst.carac["intelligence"])/2) *5

    @staticmethod
    def reflexes(inst):
        return floor((inst.carac["dexterite"] + inst.carac["intelligence"])/2) *5

    @staticmethod
    def serrures(inst):
        return floor((inst.carac["dexterite"] + inst.carac["endurance"])/2) *5

    @staticmethod
    def soigner(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def survie(inst):
        return floor((inst.carac["endurance"] + inst.carac["intelligence"])/2) *5
    
    @staticmethod
    def voler(inst):
        return floor((inst.carac["intelligence"] + inst.carac["charisme"])/2) *5

    @staticmethod
    def random_carac():
        return sum([randint(1, 6) for _ in range(3)])

    @staticmethod
    def set_pv(inst):
        value = inst.carac["endurance"]
        pv = 14 if value > 14 else value
        return pv
    
    def __init__(self, metier:str="", name:str="", age = "", possessions:list=[]):
        self.metier = metier
        self.name = name
        self.age = Personnage.verify_age(age)
        self.possessions = possessions
        self.carac = {
            "force": Personnage.random_carac(),
            "dexterite": Personnage.random_carac(),
            "endurance": Personnage.random_carac(),
            "intelligence": Personnage.random_carac(),
            "charisme": Personnage.random_carac()
            }

        self.compe = {
            "artisanat": Personnage.artisanat(self),
            "combat": Personnage.combat(self),
            "combat_distance": Personnage.combat_distance(self),
            "connais_nature": Personnage.connais_nature(self),
            "connais_secrets": Personnage.connais_secrets(self),
            "courir": Personnage.courir(self),
            "discretion": Personnage.discretion(self),
            "droit": Personnage.droit(self),
            "esquiver": Personnage.esquiver(self),
            "intimider": Personnage.intimider(self),
            "lire": Personnage.lire(self),
            "mentir": Personnage.mentir(self),
            "perception": Personnage.perception(self),
            "piloter": Personnage.piloter(self),
            "psychologie": Personnage.psychologie(self),
            "reflexes": Personnage.reflexes(self),
            "serrures": Personnage.serrures(self),
            "soigner": Personnage.soigner(self),
            "survie": Personnage.survie(self),
            "voler" : Personnage.voler(self)
            }
        self.pv = Personnage.set_pv(self)


    def comput_total(self):
        return sum([value for value in self.carac.values()])
    
    def __str__(self):
        carac = '\n' + self.metier.title() + self.name.title() + '\n'
        carac += f"Point de vie: {self.pv}\n"
        carac += f"\tCARACTERISTIQUES (total:{self.comput_total()})\n"
        for item in self.carac.items():
            tab = 1
            if len(item[0]) < 12:
                tab += 1
            if len(item[0]) < 6:
                tab += 1
            carac += "\t\t-{}:{}{}\n".format(item[0].capitalize(),'\t'*tab, item[1])
        carac += "\n\tCOMPETENCES\n"
        for item in self.compe.items():
            tab = 1
            if len(item[0]) < 13:
                tab = 2
            if len(item[0]) < 10:
                tab = 3
            if len(item[0]) < 6:
                tab = 4
            carac += "\t\t-{}:{}{} %\n".format(item[0].capitalize(),'\t'*tab, item[1])

        carac += "_" * 60 + '\n'
        return carac
    
    def get_dict_carac(self):
        return self.carac
    
    def get_dict_compe(self):
        return self.compe
    
    def get_full_dict(self):
        full_dict= {**self.carac, **self.compe}
        full_dict['metier'] = self.metier.title()
        full_dict['name'] = self.name.title()
        full_dict['pv'] = self.pv
        full_dict['age'] = self.age
        full_dict['possessions'] = self.possessions
        return full_dict


class LotPersonnage():

    @staticmethod   
    def file_name():
        name = f"perso_lot"
        file_name = name + ".txt"
        return file_name
    
    @staticmethod
    def save_file(inst):
        file_name = LotPersonnage.file_name()
        path_ = path.join(EXPORT_PATH, file_name)
        with open (path_, "w") as f:
            f.write(inst.lot_str())

    def __init__(self, metier:str = "", name:str = "", age = "", possessions:list=[]):
        self.dico = {}
        for i in range(NOMBRE_TIRAGE):
            self.dico[f'name_{i+1}'] = Personnage(metier=metier, name=name, age=age, possessions=possessions)
        LotPersonnage.save_file(self)
    
    def lot_str(self):
        str_ = ""
        for value in self.dico.values():
            str_ += value.__str__()
        return str_
    
    def export(self):
        for perso in self.dico.values():
            PdfExporter(perso)


if __name__ == '__main__':
    infos = {
        'metier': "Mage d'Aria",
        'nom': "Test",
        'age': "23",
        'possessions': ["Allumettes", "mouchoir", "gobelet"]
        }
            
    lot = LotPersonnage(infos['metier'], infos["nom"], infos["age"], infos["possessions"])
    print(lot.lot_str())
    lot.export()