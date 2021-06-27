# from io import BytesIO
from os import close, path, listdir
from time import sleep

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# PACKET = BytesIO()

CURRENT_DIR = path.dirname(__file__)
PDF_FOLDER = path.join(CURRENT_DIR, "vierge")
PDF_PATH = path.join(PDF_FOLDER, "vierge.pdf")
EXPORT_PATH = path.join(CURRENT_DIR, "export")

# Taille des polices.
SIZE_METIER = 18
SIZE_NAME = 14
SIZE_PV = 20
SIZE_AGE = 11
SIZE_CARAC = 13
SIZE_COMPE = 10
SIZE_POSSE = 9

# Postition X des types de donnée.
CARAC_X = 200
COMPE_X = 215
POSS_X = 30

# Position du nom, age, point de vie.
perso_pos = {
    'metier': (125, 629),
    'name': (151, 609),
    'age': (146, 595),
    'pv': (438, 644)
    }

# Position des caractéristiques.
carac_pos = {
    'force': (CARAC_X, 544),
    'dexterite': (CARAC_X, 527),
    'endurance': (CARAC_X, 510),
    'intelligence': (CARAC_X, 493),
    'charisme': (CARAC_X, 476)
    }

# Position des compétences.
compe_pos = {
    'artisanat': (COMPE_X, 389),
    'combat': (COMPE_X, 379),
    'combat_distance': (COMPE_X, 369),
    'connais_nature': (COMPE_X, 359),
    'connais_secrets': (COMPE_X, 349),
    'courir': (COMPE_X, 339),
    'discretion': (COMPE_X, 329),
    'droit': (COMPE_X, 319),
    'esquiver': (COMPE_X, 309),
    'intimider': (COMPE_X, 299),
    'lire': (COMPE_X, 289),
    'mentir': (COMPE_X, 280),
    'perception': (COMPE_X, 270),
    'piloter': (COMPE_X, 260),
    'psychologie': (COMPE_X, 250),
    'reflexes': (COMPE_X, 240),
    'serrures': (COMPE_X, 230),
    'soigner': (COMPE_X, 220),
    'survie': (COMPE_X, 210),
    'voler': (COMPE_X, 200)
    }

posse_pos = {
    "possessions": (POSS_X, 150)
}

class PdfExporter():

    @staticmethod
    def define_name(dir):
        counter = PdfExporter.count_export(dir)
        name = f"export_{counter+1}.pdf"
        return name

    @staticmethod
    def count_export(dir):
        # Count number of export file.
        number_files = len([f for f in listdir(dir) if 'export_' in f])
        return number_files

    def __init__(self, personnage):
        """
        PdfExporter écrit toutes les infos du personnages.
        A la manière d'un calque transparent se superpose 
        ensuite au PDF vierge.
        """
        self.personnage = personnage
        # Fusionne tout le dict de positions.
        self.full_pos = {**perso_pos ,**carac_pos, **compe_pos, **posse_pos}
        # get tout les attributs du perso en un dict.
        self.perso_dico = self.personnage.get_full_dict()
        # Initialise le canvas type calques transparents.
        self.can = canvas.Canvas("tmp.pdf", pagesize=letter)
        self.can.setFont("Helvetica-Bold", SIZE_COMPE)
        # Couleur des polices.
        self.can.setFillColorRGB(0.1, 0.44, 0.79)
        # Ecrit les infos sur le calque.
        self.write()
        # Export en pdf.
        self.export_pdf()
    
    def export_pdf(self):
        name = PdfExporter.define_name(EXPORT_PATH)
        path_ = path.join(EXPORT_PATH, name)
        output = PdfFileWriter()
        with open("tmp.pdf", "rb") as f:
            new_pdf = PdfFileReader(f)
        # Read your existing PDF.
            with open(PDF_PATH, "rb") as fi:
                existing_pdf = PdfFileReader(fi)
                # Add the "watermark" (which is the new pdf) on the existing page.
                page = existing_pdf.getPage(0)
                page.mergePage(new_pdf.getPage(0))
                output.addPage(page)
                # Finally, write "output" to a real file.
                with open(path_, "wb") as fr:
                    output.write(fr)

    
    def write(self):
        """
        Parcours du dict fusionné,
        afin de get les coordonnées puis écrire les valeurs.
        """        
        for item in self.perso_dico.items():
            key = item[0]
            value = item[1]
            font_size = SIZE_COMPE 
            if key == "possessions":
                self.write_possessions(value)
                continue
            value = str(value)
            if key in perso_pos: # Le cas le plus récurent.
                if key == "metier":
                    font_size = SIZE_METIER
                elif key == "pv":
                    font_size = SIZE_PV
                elif key == "name":
                    font_size = SIZE_NAME
                elif key == "age":
                    font_size = SIZE_AGE
            if key in carac_pos:
                font_size = SIZE_CARAC
            # Sélection de la taille et du style de la police.
            self.can.setFont("Helvetica-Bold", font_size)
            # Get les positions, lié à la key.
            posx, posy = self.full_pos[key][0], self.full_pos[key][1]
            # Si la valeur n'est que d'un chiffre, on décale X pour centrer.
            if len(value) == 1:
                posx += int(font_size/3)
            # Ecriture.
            self.can.drawString(posx, posy, value)

        # Ecrit le calques sur le disque (non visible).
        self.can.save()
    
    def write_possessions(self, value):
        if not value:
            return None
        step = 11
        posy = 155
        for item in value:
            self.can.setFont("Helvetica", SIZE_POSSE)
            self.can.drawString(POSS_X, posy, item.title())
            # Décrémente posy pour empiler les items.
            posy -= step


if __name__ == '__main__':
    from fiche_perso import Personnage
    poss = ["Dague", "Bourse (560 rois)", "corde abimée", "papier", "chapeau", "statuette dieu ennemi"]
    perso1 = Personnage(metier="Misericordieux",name="Aleam Testis", age="10", possessions=poss)
    perso2 = Personnage("Aleam2 Testis", "20", possessions=poss[1:])
    perso3 = Personnage("Aleam3 Testis", "30", possessions=poss[2:])
    persos = [perso1, perso2, perso3]
    for perso in persos:
        APP = PdfExporter(perso)