Generateur de fiche de personnage pour je jeu Aria (FibreTigre - ElderCraft)
L'outil permet de générer et pré-remplir des fiches personnages.

Un personnage possède un certain nombres d'attributs.
 -Nom
 -Age
 -Points de vie
 -Armes x3
 -Blessure
 -Protection
 -Caractéristiques x5
 -Compétences x20
 -Compétences spéciales
 -Possessions
 -Qualité ("je suis genial")
 -Defaut ("société a des problèmes")

Les caractéristiques sont générées grâce à la somme de 3d6 (min3, max18).
Les compétences sont calculées d'après la moyenne de deux caractériques. (cf. "Lien" sur la fiche)

L'outil génère trois tirages (comme prévus par les règles officiels).
Il est possible donner un nom, un age et une liste d'objet
en possessions afin de renseigner plus d'informations sur la fiche.

La console affiche un compte rendu des caractéristiques et compétence de chacun des tirage.
Dans le dossier "export" contient:
    -Un fichier .txt du compte rendu.
    -3 PDF pré-remplis. (champs, "nom", "age" restent vide si non-renseignés).

Astuces:
    Le PDF vierge.pdf est un PDF editable. Il est tout à fait possible de pré-remplir le "vierge.pdf".
    L'arme, les qualités, les défauts et les compétences spéciales, par exemple, peuvent être
    renseignés avant de générer le reste du personnage.


dev on Python 3.8.6
lib:
    pypdf2
    reportlab