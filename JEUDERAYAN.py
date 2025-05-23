import pygame
import random
import sys
import os

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
LARGEUR = 600
HAUTEUR = 800
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))  # Crée la fenêtre
pygame.display.set_caption("Ambulance Express")  # Titre de la fenêtre
clock = pygame.time.Clock()  # Pour contrôler la vitesse du jeu

# Définition des couleurs
VERT = (16, 0, 0)
GRIS = (50, 50, 50)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Chargement des images pour les différents éléments du jeu
ambulance_img = pygame.transform.scale(pygame.image.load("Ambulance.png"), (40, 50))
voiture_img = pygame.transform.scale(pygame.image.load("Audi.png"), (80, 90))
bonus_img = pygame.transform.scale(pygame.image.load("Bonus.png"), (20, 20))
invincibility_img = pygame.transform.scale(pygame.image.load("Invincibility.png"), (20, 20))
Vie_img = pygame.transform.scale(pygame.image.load("Vie.png"), (20, 20))
gameover_img = pygame.transform.scale(pygame.image.load("gameover.png"), (600, 1000))
menu_img = pygame.transform.scale(pygame.image.load("menu.png"), (900, 812))

# Chargement de la police pour le texte
police = pygame.font.SysFont("Comic Sans MS", 22)

# Initialisation des sons
pygame.mixer.init()
pygame.mixer.music.load("ambulance.mp3")  # Musique de fond
pygame.mixer.music.play(-1)  # Joue la musique en boucle
collision_sound = pygame.mixer.Sound("crash.wav")  # Son de collision
bonus_sound = pygame.mixer.Sound("bonus.mp3")  # Son de collecte de bonus

# Fichier pour sauvegarder le meilleur score
FICHIER_SCORE = "best_score.txt"

# Fonction pour lire le meilleur score depuis le fichier
def lire_meilleur_score():
    if not os.path.exists(FICHIER_SCORE):  # Si le fichier n'existe pas
        return 0  # Retourne 0 comme meilleur score
    with open(FICHIER_SCORE, "r") as f:
        try:
            return int(f.read())  # Lit et retourne le meilleur score
        except:
            return 0  # En cas d'erreur, retourne 0

# Fonction pour sauvegarder le meilleur score
def sauver_meilleur_score(score):
    meilleur = lire_meilleur_score()  # Lit le meilleur score actuel
    if score > meilleur:  # Si le score actuel est meilleur
        with open(FICHIER_SCORE, "w") as f:
            f.write(str(score))  # Sauvegarde le nouveau meilleur score

# Fonction pour dessiner le fond de la route
def dessiner_fond():
    ecran.fill(VERT)  # Remplit l'écran avec la couleur verte
    route_x = (LARGEUR - 300) // 2  # Calcule la position de la route
    pygame.draw.rect(ecran, GRIS, (route_x, 0, 300, HAUTEUR))  # Dessine la route
    for y in range(0, HAUTEUR, 60):  # Dessine les lignes blanches sur la route
        pygame.draw.rect(ecran, BLANC, (LARGEUR//2 - 5, y, 10, 30))
    pygame.draw.rect(ecran, BLANC, (route_x, 0, 5, HAUTEUR))  # Bord gauche de la route
    pygame.draw.rect(ecran, BLANC, (route_x + 295, 0, 5, HAUTEUR))  # Bord droit de la route

# Fonction pour afficher le menu principal
def afficher_menu():
    meilleur_score = lire_meilleur_score()  # Lit le meilleur score
    en_menu = True  # Variable pour contrôler l'affichage du menu
    while en_menu:
        ecran.fill((0, 0, 0))  # Remplit l'écran en noir
        ecran.blit(menu_img, (0, 0))  # Affiche l'image du menu

        # Affiche le titre et les instructions
        titre = pygame.font.SysFont("Cascadia Code", 60).render("AMBULANCE EXPRESS", True, (255, 220, 50))
        meilleur_score_texte = police.render(f"Meilleur score : {meilleur_score}", True, BLANC)
        sous_titre1 = police.render("Bonne chance, sale noob !", True, BLANC)
        sous_titre2 = police.render("Appuie sur Entrée pour jouer", True, BLANC)

        # Positionne le texte à l'écran
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2 + 2, HAUTEUR // 3 + 2)))
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 3)))
        ecran.blit(meilleur_score_texte, meilleur_score_texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 3 - 100)))
        ecran.blit(sous_titre1, sous_titre1.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 120)))
        ecran.blit(sous_titre2, sous_titre2.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 140)))

        pygame.display.flip()  # Met à jour l'affichage

        # Gère les événements du menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Si Entrée est pressée
                en_menu = False  # Quitte le menu

# Fonction pour vérifier les collisions entre deux rectangles
def collision(rect1, rect2):
    return rect1.colliderect(rect2)  # Retourne True si les rectangles se touchent

# Fonction pour afficher le nombre de vies restantes
def afficher_vies(vies):
    for i in range(vies):
        x = 10 + i * 35  # Calcule la position x pour chaque vie
        y = 40
        ecran.blit(Vie_img, (x, y))  # Affiche l'image de vie

# Fonction principale du jeu
def lancer_jeu():
    joueur_x = LARGEUR // 2  # Position initiale du joueur
    joueur_y = HAUTEUR - 100
    v_joueur = 10  # Vitesse du joueur
    voitures = []  # Liste pour stocker les voitures
    bonus = []  # Liste pour stocker les bonus
    delai = 50  # Délai entre l'apparition des voitures
    timer = 0  # Compteur pour le délai
    score = 0  # Score du joueur
    vies = 3  # Nombre de vies
    en_jeu = True  # Variable pour contrôler l'état du jeu
    v_voiture = 4  # Vitesse des voitures
    niveau_difficulte = 1  # Niveau de difficulté
    invincible = False  # État d'invincibilité
    invincibility_timer = 0  # Timer pour l'invincibilité
    pieces_collectees = 0  # Compteur de pièces collectées

    # Voies où les voitures peuvent apparaître
    voie_voiture = [((LARGEUR - 300) // 2) + 10,
                   LARGEUR // 2 - 40,
                   ((LARGEUR - 300) // 2) + 210]

    while en_jeu:
        dessiner_fond()  # Dessine le fond de la route
        afficher_vies(vies)  # Affiche le nombre de vies

        # Gère les événements du jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()
                sys.exit()

        # Gère les touches du clavier
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:  # Si la touche gauche est pressée
            joueur_x -= v_joueur  # Déplace le joueur à gauche
        if touches[pygame.K_RIGHT]:  # Si la touche droite est pressée
            joueur_x += v_joueur  # Déplace le joueur à droite

        route_x = (LARGEUR - 300) // 2  # Calcule la position de la route
        joueur_x = max(route_x, min(joueur_x, route_x + 300 - 40))  # Empêche le joueur de sortir de la route

        timer += 1  # Incrémente le timer
        if timer >= delai:  # Si le délai est atteint
            voiture_x = random.choice(voie_voiture)  # Choisit une voie pour la voiture
            voitures.append([voiture_x, -90])  # Ajoute une nouvelle voiture

            bonus_voies_dispo = [x for x in voie_voiture if x != voiture_x]  # Voies disponibles pour les bonus

            # Empêche spawn bonus dans voie déjà occupée
            voies_occupees = [b[0] for b in bonus]  # Récupère les voies occupées par les bonus
            voies_libres = [v for v in bonus_voies_dispo if v not in voies_occupees]  # Filtre les voies libres

            # Taux de drop réduit pour les bonus
            if random.random() < 0.2 and voies_libres:  # 20% de chance d'apparition d'un bonus normal
                bonus_x = random.choice(voies_libres)  # Choisit une voie libre pour le bonus
                bonus.append([bonus_x, -30, "score"])  # Ajoute le bonus à la liste

            if random.random() < 0.05 and voies_libres:  # 5% de chance d'apparition d'un bonus d'invincibilité
                invincibility_x = random.choice(voies_libres)  # Choisit une voie libre pour le bonus d'invincibilité
                bonus.append([invincibility_x, -30, "invincible"])  # Ajoute le bonus d'invincibilité à la liste

            timer = 0  # Réinitialise le timer

        # Met à jour la position des voitures
        for v in voitures:
            v[1] += v_voiture  # Déplace la voiture vers le bas
        voitures = [v for v in voitures if v[1] < HAUTEUR]  # Garde seulement les voitures visibles

        # Met à jour la position des bonus
        for b in bonus:
            b[1] += v_voiture  # Déplace le bonus vers le bas
        bonus = [b for b in bonus if b[1] < HAUTEUR]  # Garde seulement les bonus visibles

        rect_joueur = pygame.Rect(joueur_x + 4, joueur_y + 4, 32, 42)  # Crée un rectangle pour le joueur

        # Vérifie les collisions entre le joueur et les voitures
        for v in voitures:
            rect_v = pygame.Rect(v[0] + 8, v[1] + 8, 64, 74)  # Crée un rectangle pour la voiture
            if collision(rect_joueur, rect_v):  # Si le joueur touche une voiture
                if not invincible:  # Si le joueur n'est pas invincible
                    vies -= 1  # Enlève une vie
                    voitures.remove(v)  # Enlève la voiture
                    collision_sound.play()  # Joue le son de collision
                    if vies <= 0:  # Si le joueur n'a plus de vies
                        en_jeu = False  # Met fin au jeu
                break  # Sort de la boucle

        # Vérifie les collisions entre le joueur et les bonus
        for b in bonus[:]:
            rect_b = pygame.Rect(b[0], b[1], 20, 20)  # Crée un rectangle pour le bonus
            if collision(rect_joueur, rect_b):  # Si le joueur touche un bonus
                if len(b) >= 3 and b[2] == "invincible":  # Si c'est un bonus d'invincibilité
                    invincible = True  # Active l'invincibilité
                    invincibility_timer = 300  # Définit le timer d'invincibilité
                    bonus.remove(b)  # Enlève le bonus
                elif len(b) >= 3 and b[2] == "score":  # Si c'est un bonus de score
                    score += 100  # Ajoute des points au score
                    pieces_collectees += 1  # Incrémente le compteur de pièces collectées
                    bonus.remove(b)  # Enlève le bonus
                    bonus_sound.play()  # Joue le son de collecte de bonus

                    if pieces_collectees >= 5:  # Si le joueur a collecté 5 pièces
                        vies += 1  # Ajoute une vie
                        pieces_collectees = 0  # Réinitialise le compteur de pièces

        # Gère l'état d'invincibilité
        if invincible:
            invincibility_timer -= 1  # Décrémente le timer
            if invincibility_timer <= 0:  # Si le timer est écoulé
                invincible = False  # Désactive l'invincibilité

        # Augmente la difficulté du jeu
        if score // 100 > niveau_difficulte:  # Si le score atteint un nouveau niveau
            niveau_difficulte += 1  # Augmente le niveau de difficulté
            v_voiture += 1  # Augmente la vitesse des voitures
            delai = max(20, delai - 5)  # Réduit le délai entre les apparitions de voitures

        # Affiche le joueur, les voitures et les bonus
        ecran.blit(ambulance_img, (joueur_x, joueur_y))  # Affiche l'ambulance
        for v in voitures:
            ecran.blit(voiture_img, (v[0], v[1]))  # Affiche chaque voiture
        for b in bonus:
            if len(b) >= 3 and b[2] == "invincible":  # Si c'est un bonus d'invincibilité
                ecran.blit(invincibility_img, (b[0], b[1]))  # Affiche le bonus d'invincibilité
            else:
                ecran.blit(bonus_img, (b[0], b[1]))  # Affiche le bonus normal

        score += 1  # Incrémente le score
        score_txt = police.render("Score : " + str(score), True, BLANC)  # Crée le texte du score
        ecran.blit(score_txt, (10, 10))  # Affiche le score

        # Affiche un message si le joueur est invincible
        if invincible:
            invincibility_txt = police.render("Invincibilité active!", True, (255, 255, 0))
            ecran.blit(invincibility_txt, (LARGEUR // 2 - 100, 10))

        pygame.display.flip()  # Met à jour l'affichage
        clock.tick(60)  # Limite le jeu à 60 images par seconde

    return score  # Retourne le score final

# Fonction pour afficher l'écran de fin de jeu
def ecran_fin(score):
    sauver_meilleur_score(score)  # Sauvegarde le score final
    meilleur_score = lire_meilleur_score()  # Lit le meilleur score

    continuer = True  # Variable pour contrôler l'affichage de l'écran de fin
    while continuer:
        ecran.blit(gameover_img, (0, 0))  # Affiche l'image de fin de jeu
        texte1 = police.render(f"T'a perdu sale noob XD - Score : {score}", True, BLANC)  # Affiche le score
        texte2 = police.render(f"Meilleur score : {meilleur_score}", True, BLANC)  # Affiche le meilleur score
        texte3 = police.render("Entrée pour rejouer | ESC pour quitter", True, BLANC)  # Instructions

        # Positionne le texte à l'écran
        ecran.blit(texte1, texte1.get_rect(center=(LARGEUR // 2, 180)))
        ecran.blit(texte2, texte2.get_rect(center=(LARGEUR // 2, 220)))
        ecran.blit(texte3, texte3.get_rect(center=(LARGEUR // 2, 260)))

        pygame.display.flip()  # Met à jour l'affichage

        # Gère les événements de l'écran de fin
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Si une touche est pressée
                if event.key == pygame.K_RETURN:  # Si Entrée est pressée
                    continuer = False  # Quitte l'écran de fin
                elif event.key == pygame.K_ESCAPE:  # Si Échap est pressé
                    pygame.quit()
                    sys.exit()

# Boucle principale du jeu
if __name__ == "__main__":
    while True:
        afficher_menu()  # Affiche le menu
        score_final = lancer_jeu()  # Lance le jeu et récupère le score final
        ecran_fin(score_final)  # Affiche l'écran de fin avec le score
