import logging
from datetime import datetime

import feedgenerator
import pytz
import requests
from bs4 import BeautifulSoup

# Configuration du logging
logging.basicConfig(
    level=logging.BASIC_FORMAT,  # Changé de INFO à DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='rss_generator.log'
)

class TourmagRSSGenerator:
    def __init__(self):
        self.base_url = "https://www.tourmag.com/airmag/"  # URL mise à jour
        self.feed = feedgenerator.Rss201rev2Feed(
            title="TourMag AirMag - Flux RSS",
            link=self.base_url,
            description="Actualités du transport aérien par TourMag",
            language="fr",
        )
        self.timezone = pytz.timezone('Europe/Paris')

    def fetch_articles(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Utilisation des sélecteurs CSS fournis
            articles = soup.find_all(class_='titre_article')
            
            for article in articles:
                try:
                    # Extraction du titre et du lien
                    title = article.text.strip()
                    link = 'https://www.tourmag.com' + article.find('a')['href']
                    
                    # Remonter à l'élément parent pour trouver les autres éléments
                    article_container = article.find_parent('div', class_='rub_left')
                    
                    # Extraction de l'image
                    image_element = article_container.find('img')
                    image_url = image_element['src'] if image_element else None
                    
                    # Extraction du résumé - modification ici
                    description = article_container.find('div', class_='resume_article')
                    description_text = description.text.strip() if description else ""
                    
                    # Création de la description HTML avec l'image
                    full_description = ""
                    if image_url:
                        if not image_url.startswith('http'):
                            image_url = 'https://www.tourmag.com' + image_url
                        full_description += f'<img src="{image_url}" alt="{title}"/><br/><br/>'
                    full_description += description_text
                    
                    # Utilisation de la date actuelle
                    date_aware = self.timezone.localize(datetime.now())
                    
                    self.feed.add_item(
                        title=title,
                        link=link,
                        description=full_description,
                        pubdate=date_aware,
                        unique_id=link
                    )
                    logging.info(f"Article ajouté: {title}")
                    
                except Exception as e:
                    logging.error(f"Erreur lors du traitement d'un article: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des articles: {str(e)}")
            raise

    def generate_feed(self, output_file='tourmag_feed.xml'):
        try:
            self.fetch_articles()
            with open(output_file, 'w', encoding='utf-8') as f:
                self.feed.write(f, 'utf-8')
            logging.info(f"Flux RSS généré avec succès: {output_file}")
        except Exception as e:
            logging.error(f"Erreur lors de la génération du flux: {str(e)}")
            raise

if __name__ == "__main__":
    generator = TourmagRSSGenerator()
    generator.generate_feed()