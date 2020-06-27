# "Solar Project"

**GitHub :** https://github.com/anselmia/p13.git

## **1. Démarche du projet :**

SolarProject est un outil  de conception de projet photovoltaïque qui permet de designer un projet en partant de la puissance photovoltaïque admissible sur une toiture, jusqu'au calcul de production du système. Il permet de comparer différentes configuration afin d'optimiser une installation. 
Une base de données permet à un utilisateur enregistré de sauvegarder son projet.

Ce projet s’oriente pour toutes les personnes désireuses de réaliser un projet photovoltaïque raccordé au réseau ou en ayant l’intention.

L’outil de conception se décompose en 5 phases :

**Définition du projet :**
L’utilisateur donne un nom à son projet, définit la ville où se situera le projet et le modèle de panneau qu’il souhaite utiliser.
La ville contient 3 informations : nom, latitude et longitude. L’utilisateur peut ajouter une nouvelle ville en saisissant son nom et à l’aide de l’API OpenCageData, l’application récupère sa latitude et sa longitude.
Un nouveau modèle de panneau peut également être ajouté à l’application en saisissant les informations qui lui sont liées.

**Définition de la toiture :**
L’utilisateur saisit ensuite les informations relatives à la toiture sur laquelle seront installés les panneaux solaires.
L’application permet de choisir parmi 3 formes de toits (rectangulaire, trapézoïdale et triangulaire) et invite à saisir les dimensions relatives à la forme sélectionnée.
Il faut enfin définir la pente et l’orientation de la toiture (en °).

**Définition de l’implantation du système :**
L’utilisateur définit le mode de pose des panneaux (paysage ou portrait) et l’implantation (côte à côte, espacé ou recouvert).
L’application permet à l’utilisateur de définir la position du système par le biais de valeurs d’espacement par rapport aux bords de la toiture et d’intégrer le système d’abergement.
Un plan en 2d permet de visualiser le résultat de l’implantation.

**Configuration panneaux/onduleurs :**
L’utilisateur définit ensuite les onduleurs qui seront utilisés pour le raccordement de l’installation au réseau électrique, ainsi que l’interconnexion des panneaux.
L’outils oriente l’utilisateur à l’aide de paramètres calculés en fonction de la configuration choisie et indique si la configuration est viable ou non à l’aide d’un code couleur.

**Calcul de la production énergétique :**
L’application affiche alors un résumé des informations saisies précédemment et à l’aide de l’API PVGIS, affiche l’irradiation solaire moyenne mensuelle ainsi que la production du système.

L’utilisateur a alors une vue d’ensemble de la réalisation de son projet et peut comparer plusieurs configurations afin d’obtenir la solution la plus adaptée à son besoin.


## **2. Prérequis :**

Installer les dépendances : "pip install -r requirements.txt"

Utiliser python 3

## **3. Paramétrage :**

**Fichier settings :**
OPEN_CAGE_DATA_API_KEY : Clé pour l'api OpenCageData
