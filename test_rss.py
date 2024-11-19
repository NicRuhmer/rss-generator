import logging

from rss_generator import TourmagRSSGenerator

# Configuration du logging pour voir les résultats dans la console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=None
)

def test_rss():
    try:
        # Créer une instance du générateur
        generator = TourmagRSSGenerator()
        
        # Générer le flux RSS avec un nom de fichier spécifique
        generator.generate_feed('test_feed.xml')
        
        # Lire et afficher le contenu du fichier généré
        with open('test_feed.xml', 'r', encoding='utf-8') as f:
            print("\nContenu du flux RSS généré :")
            print("-" * 50)
            print(f.read())
            
    except Exception as e:
        print(f"Erreur lors du test : {str(e)}")

if __name__ == "__main__":
    test_rss()