# Scrapper

Récupération des infos des films d'une page AlloCiné.

# Pré-requis
```bash
pip3 install scrapy
```

# Utilisation

1.  Définir les **url** à charger dans le fichier `scrapy/download/download/spiders/recents.py`
    ```python
    def start_requests(self):
        urls = [
             'http://www.allocine.fr/film/agenda/sem-2017-12-13/',
             'http://www.allocine.fr/film/agenda/sem-2017-12-20/',
             ]
    ```
2.  Lancement
    ```bash
     scrapy crawl recents -o result.json
    ```
