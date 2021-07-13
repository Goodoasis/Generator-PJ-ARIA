from collections import namedtuple
from os import path
from random import randint
from math import floor

from pdf_exporter import EXPORT_PATH, PdfExporter


NOMBRE_TIRAGE = 3
Infos = namedtuple("Infos", ["nom", "metier", "pv", "possessions"])
Carac = namedtuple("Carac", ["force", "dexterite", "endurance", "intelligence", "charisme"])
Compe = namedtuple("Compe", ["artisanat", "combat", "combat_distance",
                                "connais_nature", "connais_secrets",
                                "courir", "discretion", "droit", "esquiver",
                                "intimider", "lire", "mentir", "perception",
                                "piloter", "psychologie", "reflexes",
                                "serrures", "soigner", "survie", "voler"])


class Personnage():

    def __init__(self, metier:str="", name:str="", age = "", possessions:list=[]):
        # Caracteristiques:
        force =         Personnage.random_carac()
        dexterite =     Personnage.random_carac()
        endurance =     Personnage.random_carac()
        intelligence =  Personnage.random_carac()
        charisme =      Personnage.random_carac()
        self.carac = Carac(force, dexterite, endurance, intelligence, charisme)
        # Infos:
        age =   Personnage.verify_age(age)
        pv =    Personnage.set_pv(self)
        self.infos = Infos(name, metier, pv, possessions)
        # Compétences:
        artisanat =         Personnage.comput_competence(dexterite, intelligence)
        combat =            Personnage.comput_competence(force, dexterite)
        combat_distance =   Personnage.comput_competence(dexterite, intelligence)
        connais_nature =    Personnage.comput_competence(dexterite, intelligence)
        connais_secrets =   Personnage.comput_competence(intelligence, charisme)
        courir =            Personnage.comput_competence(dexterite, endurance)
        discretion =        Personnage.comput_competence(dexterite, charisme)
        droit =             Personnage.comput_competence(intelligence, charisme)
        esquiver =          Personnage.comput_competence(dexterite, intelligence)
        intimider =         Personnage.comput_competence(force, charisme)
        lire =              Personnage.comput_competence(intelligence, charisme)
        mentir =            Personnage.comput_competence(intelligence, charisme)
        perception =        Personnage.comput_competence(intelligence, charisme)
        piloter =           Personnage.comput_competence(dexterite, endurance)
        psychologie =       Personnage.comput_competence(endurance, intelligence)
        reflexes =          Personnage.comput_competence(dexterite, intelligence)
        serrures =          Personnage.comput_competence(dexterite, endurance)
        soigner =           Personnage.comput_competence(intelligence, charisme)
        survie =            Personnage.comput_competence(endurance, intelligence)
        voler =             Personnage.comput_competence(dexterite, intelligence)
        self.compe = Compe(artisanat, combat, combat_distance, connais_nature, connais_secrets,
                        courir, discretion, droit, esquiver, intimider, lire, mentir, perception,
                        piloter, psychologie, reflexes, serrures, soigner, survie, voler)

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
    def comput_competence(stat1, stat2):
        return floor((stat1 + stat2)/2) * 5

    @staticmethod
    def random_carac():
        return sum([randint(1, 6) for _ in range(3)])

    @staticmethod
    def set_pv(self):
        return 14 if self.carac.endurance > 14 else self.carac.endurance
    
    @staticmethod
    def comput_total(self):
        return sum(self.carac)
    
    def __str__(self):
        carac = f"\n{self.infos.nom.title()} {self.infos.metier.title()}\n"
        carac += f"Point de vie: {self.infos.pv}\n"
        carac += f"\tCARACTERISTIQUES (total:{Personnage.comput_total(self)})\n"
        for item in self.carac._asdict().items():
            tab = 1
            if len(item[0]) < 12:
                tab += 1
            if len(item[0]) < 6:
                tab += 1
            carac += "\t\t-{}:{}{}\n".format(item[0].capitalize(),'\t'*tab, item[1])
        carac += "\n\tCOMPETENCES\n"
        for item in self.compe._asdict().items():
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

    @staticmethod
    def get_dict_carac(self):
        return self.carac._asdict()

    @staticmethod
    def get_dict_compe(self):
        return self.compe._asdict()

    @staticmethod
    def get_dict_infos(self):
        return self.infos._asdict()

    def get_full_dict(self):
        return {**Personnage.get_dict_infos(self),
                **Personnage.get_dict_carac(self),
                **Personnage.get_dict_compe(self)}


class LotPersonnage():

    @staticmethod   
    def file_name():
        name = "perso_lot"
        file_name = name + ".txt"
        return file_name
    
    @staticmethod
    def save_file(inst):
        file_name = LotPersonnage.file_name()
        path_ = path.join(EXPORT_PATH, file_name)
        with open (path_, "w") as f:
            f.write(inst.lot_str())

    def __init__(self, metier:str = "", nom:str = "", age = "", possessions:list=[]):
        self.persos = {}
        for i in range(NOMBRE_TIRAGE):
            self.persos[f'{nom}_{i+1}'] = Personnage(metier, nom, age, possessions)
        LotPersonnage.save_file(self)
    
    def lot_str(self):
        str_ = ""
        for value in self.persos.values():
            str_ += value.__str__()
        return str_
    
    def export(self):
        for perso in self.persos.values():
            PdfExporter(perso)
    
    def get_full_dict(self):
        persos_dict = {}
        for key, perso in self.persos.items():
            persos_dict[key] = perso.get_full_dict()
        return persos_dict


if __name__ == '__main__':
    from pprint import pprint
    infos = {
        'metier': "Mage d'Aria",
        'nom': "Aleam",
        'age': "23",
        'possessions': ["Allumettes", "mouchoir", "gobelet"]
        }
            
    lot = LotPersonnage(infos['metier'], infos["nom"], infos["age"], infos["possessions"])
    lot.export()