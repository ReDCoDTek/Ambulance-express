from PIL import Image

# Liste des fichiers PNG à nettoyer
fichiers = ['Audi.png', 'Ambulance.png']

for fichier in fichiers:
    img = Image.open(fichier)
    # Re-sauvegarder sans profils couleur
    img.save(fichier, icc_profile=None)
    print(f"{fichier} nettoyé !")
