import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os 
from pathlib import Path
from slugify import slugify

# specify the url
url_principal = "http://books.toscrape.com/"

star_rating = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
headers = ["product_page_url",
"universal_product_code",
"title",
"price_including_tax",
"price_excluding_tax",
"number_available",
"product_description",
"category",
"review_rating",
"image_url"]


def get_and_parse_url(url):
	"""Appeler et analyser une page web HTML

    Parameters
    ----------
    url : url de la page à appeler et à analyser

    Returns
    -------
    	Le contenu de la page """

	response = requests.get(url)
	if response.ok:
		
		return(BeautifulSoup(response.content,"html.parser"))


def categories_url(url_principal):
	"""Recupérer dans une liste, toutes les urls de toutes les pages pour chaque catégorie

    Parameters
    ----------
    url : url de la page principale du site Bookstoscrape

    Returns
    -------
    	la liste de toutes les urls  des pages pour chaque catégorie """

	soup_categories = get_and_parse_url(url_principal).select("ul")[2].select("li")
	categories_url = []
	for soup_category in soup_categories:
		category_url = urljoin(url_principal, soup_category.a["href"])
		categories_url.append(category_url)
		next_botton = get_and_parse_url(category_url).find("li", class_="next")

		"""Tant qu'il existe un bouton next
		Recherche du lien de la page suivante
		Ensuite dès qu'il n'y a plus de page arret de la recherche"""
		
		while next_botton:
			page = urljoin(category_url,next_botton.a["href"])
			next_botton = get_and_parse_url(page).find("li",class_="next")	
			categories_url.append(page)

	return(categories_url)


def get_books_urls_page(category_url): 
	"""Récupérer dans une liste toutes les urls des livres pour chaque catégorie

    Parameters
    ----------
    category_url : url de la catégory

    Returns
    -------
    	Liste de toutes les urls de livres pour chaque catégorie """

	book_urls = []
	category_soup = get_and_parse_url(category_url).find_all("div", class_="image_container")    
	for divs_book in category_soup:
		book_urls.append(urljoin(category_url, divs_book.a["href"]))

	return(book_urls)



def get_datas_book(soup):	
	"""Récupérer les valeurs de certaines données demandées pour un livre

    Parameters
    ----------
    soup : contenu de la page html du livre

    Returns
    -------
    	les valeurs pour chaque données cherchées """

	tds = soup.select("td")
	product_page_url = book_url 
	universal_product_code = tds[0].text
	title = soup.h1.text
	title = slugify(title,lowercase=False, separator=" ")
	price_including_tax = tds[2].text
	price_excluding_tax = tds[3].text
	number_available = tds[5].text
	product_description = soup.select_one('#product_description')
		
	if product_description :
		product_description = soup.select("p")[3].text.lower()
		product_description = slugify(product_description, separator=" ")
	else:
		product_description = "none"
	review_rating = soup.find(class_= "star-rating")["class"][1]
	review_rating = star_rating[review_rating]
	image_url = urljoin(url_principal, soup.find("img")["src"])
		
	return([product_page_url,
		universal_product_code,
		title, 
		price_including_tax,
		price_excluding_tax,
		number_available,
		product_description,
		categorie_name,
		review_rating,
		image_url])


def create_csv_file(repertoire, data):
	"""ajouter un fichier csv dans chaque répértoire de chaque catégorie correspondante et y écrire les données pour chaque livres

    Parameters
    ----------
    categorie_name : nom du répertoire de la catégorie
    data : données 

    Returns
    -------
    Ajouter les données dans chaque fichiers csv """

	with open(Path(path, f"{repertoire}.csv"), "a",encoding="utf-8-sig") as file:
		return(file.write(";".join(data) + "\n"))


#Pour chaque url dans la liste catégories url
for category_url in categories_url(url_principal):

	#Appel et analyse de l'url la page catégorie
	category_soup = get_and_parse_url(url=category_url)
	#Recherche du nom de la catégorie grace à l'élément strong
	categorie_name = category_soup.select_one("strong").text 
	path = categorie_name	
	
	if not os.path.exists(categorie_name):
		os.mkdir(categorie_name)	
		create_csv_file(categorie_name, headers)

	for book_url in get_books_urls_page(category_url):	
		print(book_url)
		soup = get_and_parse_url(book_url)

		valeurs = get_datas_book(soup)
				
		create_csv_file(categorie_name, valeurs)

		image = requests.get(valeurs[9]).content
		with open(Path(path, f"{valeurs[2]}.jpg"), "wb") as file:
			file.write(image)





