import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from P2_01_codesource import book_url_info, get_page # importation des fonction dans book.py
import csv
from collections import OrderedDict



# créations des fonctions de categorie
def get_all_pages(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    book_urls = soup.select("h3 a")
    
    books_info_list = []
    for book_url in book_urls:  # boucle de récupération des urls d'une categorie et les urls des images d'une catégorie
        book_url = urljoin(url, book_url['href'])  
        info = book_url_info(get_page(book_url), book_url)
        books_info_list.append(info)
        
#Est-ce qu'il ya une page next ? 
# si c'est le cas alors passe à la page suivante et téléchargement les infos de cette page     
    next = soup.select_one(".next a")
    if next is not None:
        url_next = urljoin(url, next['href'])
        books_info_list += get_all_pages(url_next)
        
    return books_info_list

def main():
    url = "https://books.toscrape.com/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser") 

    categories_list = soup.select(".nav.nav-list li a")
    
    for category in categories_list:
        if category['href'] is not None:
            category_name = category.text.strip()
            category_url = urljoin(url, category['href'])
            books_list = get_all_pages(category_url)
            
            save_tocsv(books_list, category_name)
        
def save_tocsv(books_info_list, category_name):
    header = OrderedDict([      
        ("title",None),
        ("price", None),
        ("review_rating", None),
        ("number_available", None),
        ("product_description", None),
        ("universal_product_code", None),
        ("price_excluding_tax", None),
        ("price_including_tax", None),
        ( "image_url", None)
    
    ])

    with open(category_name +".csv", 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in books_info_list:
            writer.writerow(row)
    
    
if __name__ == "__main__":
    
    main()
    
