from threading import Thread
import requests
from bs4 import BeautifulSoup
import os


def getChapters(interval):
    chapter = interval[0]
    for k in range((interval[1] - interval[0]) + 1):
        getChapterUrl(chapter)
        chapter += 1


def getChapterUrl(chapter):
    if chapter < 10:
        url = "https://unionmangas.top/leitor/One%20Piece/0{}".format(chapter)

    else:
        url = "https://unionmangas.top/leitor/One%20Piece/{}".format(chapter)
    getPage(url, chapter)


def getPage(url, chapter):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    images = soup.find_all('img', class_="img-manga")
    cont = 0
    ignore = ["https://unionmangas.top/images/banner_scan.png", "https://unionmangas.top/images/banner_forum.png"]
    for image in images:
        url = image.get("src").replace(" ", "%20")
        if url not in ignore:
            getImage(url, chapter, cont)
        cont += 1


def getImage(url, chapter, cont):
    directory = 'Chapter{}'.format(chapter)

    # Inform here directory you want to save this work
    # Replace the D:/OP/ in the bottom row
    # C:/Users/bko3/Downloads/OP/
    # D:/OP/

    path = 'D:/OP/{}/'.format(directory)
    if os.path.isdir(path) is False:
        os.makedirs(path)
    with open('{}{}.jpg'.format(path, cont), 'wb') as handle:
        response = requests.get(url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


def useThreading(chapters, threads):
    cont = 0
    for i in range(threads):
        interval = []
        div = chapters / threads
        interval.append(int(cont))
        if (cont + div) < chapters:
            cont = cont + div
            interval.append(int(cont))
        else:
            interval.append(int(chapters))
        call = Thread(target=getChapters, args=[interval])
        call.start()
        cont += 1


# call passing the interval of chapters "without thread"
# getChapters([1000, 1007])

# called passing the number of chapters and number of threads you want to use
useThreading(600, 20)
