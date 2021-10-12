# Projet2 : Bookstoscrape

## 1/Présentation

C'est un programme qui permet de scraper les informations du site [books.toscrape.com](http://books.toscrape.com/). Il récupère pour chaque livre les informations suivantes:
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

Ces informations sont enregistrées dans un fichier csv (un pour chaque catégorie). Les images des livres sont également récupérées dans un fichier image. 

## 2/Installation

Le programme nécessite des prérequis. Il est aussi recommandé de l'installer dans un environnement virtuel, voir procédure ci-dessous.

### Prérequis

Ce programme utilise python3, il est nécessaire qu'il soit installé.
Pour télécharger python c'est [ici](https://www.python.org/downloads/) !


### Environnement virtuel

1. Pour créer et activer un environnement

Pour créer un environnement, 
utilisez la commande python3 -m venv env.
Notez que env est un nom que l'on choissis par convention.

**Pour Windows:**

Création:
	
```cmd
python3 -m venv env
```
Activation:
```cmd
env/Scripts/activate.bat
```	

**Linux/macOS:**

Création:
	
```cmd
python3 -m venv env
```
Activation:
```cmd
source env\bin\activate
```

2. installer les modules via la commande:
```cmd
pip3 install -r requirements.txt
```

3. Lancer le programme:
```cmd
python3 Bookstoscrape.py
```

	

