import requests
import sqlite3
from bs4 import BeautifulSoup
from time import sleep

conn = sqlite3.connect("biblus.sqlite")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE books
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     book_name VARCHARE(30));
     """)


def parsing(url):
    response = requests.get(url)
    sleep(15)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    sleep(15)
    body = soup.find("body")
    sleep(15)
    nuxt = body.find("div", id='__nuxt')
    sleep(15)
    layout = nuxt.find("div", id='__layout')
    sleep(15)
    books = layout.find("div", {'class': "books w-100 w-md-90 mx-auto NUXT"})
    sleep(15)
    mx_auto = books.find("div", {'class': "w-90 w-md-100 mx-auto"})
    sleep(15)
    position = mx_auto.find("div", {'class': "b-overlay-wrap position-relative mt-1_875rem"})
    sleep(15)
    row = position.find("div", {'class': "row"})
    sleep(15)
    all_book = row.find_all("div", {'class': "mb-1_875rem col-sm-4 col-md-3 col-xl-2 col-6"})
    ls = []
    for i in all_book:
        book_name = i.find("div",
                           {'class': "bg-white __product-card d-flex flex-column justify-content-between p-1rem"})
        title = book_name.acronym.text
        taply = (title,)
        ls.append(taply)
        print(title)
    cursor.executemany("INSERT INTO books(book_name) VALUES (?)", ls)
    conn.commit()


def main():
    parsing("https://biblusi.ge/products?category=291&category_id=305&page=1")
    parsing("https://biblusi.ge/products?category=291&category_id=305&page=2")
    conn.close()

main()
