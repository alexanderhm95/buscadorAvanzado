import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate
from termcolor import colored
from urllib.parse import urlparse, unquote
from tqdm import tqdm

def imprimir_resultados(resultados, motor):
    print(colored(f"Resultados de {motor}:", "cyan"))
    tabla_resultados = []
    for resultado in resultados:
        titulo = resultado[0]
        enlace = resultado[1]
        tabla_resultados.append([colored(titulo, "yellow"), colored(enlace, "blue", attrs=["underline"])])
    print(tabulate(tabla_resultados, headers=[colored("Título", "green"), colored("Enlace", "green")], tablefmt="fancy_grid"))
    print()

def buscar_en_google(consulta):
    url = f"https://www.google.com/search?q={consulta}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = soup.select(".g")
    resultados_google = []
    for resultado in resultados:
        titulo = resultado.select_one(".LC20lb").text.strip()
        enlace = resultado.select_one("a")["href"]
        resultados_google.append((titulo, enlace))
    return resultados_google

def buscar_en_bing(consulta):
    try:
        url = f"https://www.bing.com/search?q={consulta}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        resultados = soup.select(".b_algo")
        resultados_bing = []
        for resultado in resultados:
            titulo = resultado.select_one("a").text.strip()
            enlace = resultado.select_one("a")["href"]
            resultados_bing.append((titulo, enlace))
        return resultados_bing
    except Exception as e:
        print(f"Error al buscar en Bing: {str(e)}")
        return []


def buscar_en_yahoo(consulta):
    url = f"https://search.yahoo.com/search?p={consulta}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = soup.select(".algo")
    resultados_yahoo = []
    for resultado in resultados:
        titulo = resultado.select_one(".title").text.strip()
        enlace = resultado.select_one("a")["href"]
        resultados_yahoo.append((titulo, enlace))
    return resultados_yahoo

def buscar_en_duckduckgo(consulta):
    url = f"https://duckduckgo.com/html/?q={consulta}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = soup.select(".result")
    resultados_duckduckgo = []
    for resultado in resultados:
        titulo = resultado.select_one(".result__title").text.strip()
        enlace = resultado.select_one(".result__url").text.strip()
        if re.search(r"\.pdf$", enlace):
            resultados_duckduckgo.append((titulo, enlace))
    return resultados_duckduckgo

def buscar_en_yandex(consulta):
    url = f"https://www.yandex.com/search/?text={consulta}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = soup.select(".serp-item")
    resultados_yandex = []
    for resultado in resultados:
        titulo = resultado.select_one(".organic__title-wrapper").text.strip()
        enlace = resultado.select_one(".link.link_theme_normal").text.strip()
        if re.search(r"\.pdf$", enlace):
            resultados_yandex.append((titulo, enlace))
    return resultados_yandex

def buscar_en_baidu(consulta):
    url = f"https://www.baidu.com/s?wd={consulta}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = soup.select(".result")
    resultados_baidu = []
    for resultado in resultados:
        titulo = resultado.select_one(".t").text.strip()
        enlace = resultado.select_one("a")["href"]
        if re.search(r"\.pdf$", enlace):
            resultados_baidu.append((titulo, enlace))
    return resultados_baidu

def buscar_en_naver(consulta):
    url = f"https://search.naver.com/search.naver?query={consulta}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    resultados = soup.select(".sh_web_top")
    resultados_naver = []
    for resultado in resultados:
        titulo = resultado.select_one(".sh_web_title").text.strip()
        enlace = resultado.select_one("a")["href"]
        if re.search(r"\.pdf$", enlace):
            resultados_naver.append((titulo, enlace))
    return resultados_naver

# Ejemplo de uso
consulta = " Six key strategies for managing the IT infrastructure "

resultados_google = buscar_en_google(consulta)
imprimir_resultados(resultados_google, "Google")

resultados_bing = buscar_en_bing(consulta)
imprimir_resultados(resultados_bing, "Bing")

resultados_yahoo = buscar_en_yahoo(consulta)
imprimir_resultados(resultados_yahoo, "Yahoo")

resultados_duckduckgo = buscar_en_duckduckgo(consulta)
imprimir_resultados(resultados_duckduckgo, "DuckDuckGo")

resultados_yandex = buscar_en_yandex(consulta)
imprimir_resultados(resultados_yandex, "Yandex")

resultados_baidu = buscar_en_baidu(consulta)
imprimir_resultados(resultados_baidu, "Baidu")

resultados_naver = buscar_en_naver(consulta)
imprimir_resultados(resultados_naver, "Naver")

