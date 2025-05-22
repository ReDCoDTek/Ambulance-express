import pygame
import random
import sys

pygame.init()

# Fenetre
LARGEUR = 600
HAUTEUR = 800
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Ambulance Express")
clock = pygame.time.Clock()

# Couleurs
VERT = (16, 0, 0)
GRIS = (50, 50, 50)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Images
ambulance_img = pygame.transform.scale(pygame.image.load("Ambulance.png"), (40, 50))
voiture_img = pygame.transform.scale(pygame.image.load("Audi.png"), (80, 90))
bonus_img = pygame.transform.scale(pygame.image.load("Bonus.png"), (20, 20))
invincibility_img = pygame.transform.scale(pygame.image.load("Invincibility.png"), (20, 20))  # Image pour le bonus d'invincibilité
Vie_img = pygame.transform.scale(pygame.image.load("Vie.png"), (20, 20))
gameover_img = pygame.transform.scale(pygame.image.load("gameover.png"), (600, 1000))
menu_img = pygame.transform.scale(pygame.image.load("menu.png"), (900, 812))
# Police
police = pygame.font.SysFont("Comic Sans MS", 22)

# Sons
pygame.mixer.init()
pygame.mixer.music.load("ambulance.mp3")  # Charge la musique de fond
pygame.mixer.music.play(-1)  # Joue en boucle le son 
collision_sound = pygame.mixer.Sound("crash.wav")  # Charge le son de collision
bonus_sound = pygame.mixer.Sound("bonus.mp3")  # Charge le son de bonus

# Fonctions
def dessiner_fond():
    ecran.fill(VERT)
    route_x = (LARGEUR - 300) // 2
    pygame.draw.rect(ecran, GRIS, (route_x, 0, 300, HAUTEUR))
    for y in range(0, HAUTEUR, 60):
        pygame.draw.rect(ecran, BLANC, (LARGEUR//2 - 5, y, 10, 30))
    pygame.draw.rect(ecran, BLANC, (route_x, 0, 5, HAUTEUR))
    pygame.draw.rect(ecran, BLANC, (route_x + 295, 0, 5, HAUTEUR))

def afficher_menu():
    en_menu = True
    while en_menu:
        ecran.fill((0, 0, 0))  # Fond noir
        ecran.blit(menu_img, (0, 0))  # Utilise la variable menu_img

        # Titre avec une police stylisée
        titre = pygame.font.SysFont("Cascadia Code", 60).render("AMBULANCE EXPRESS", True, (255, 220, 50))
        sous_titre1 = police.render("Bonne chance, sale noob !", True, (255, 255, 255))
        sous_titre2 = police.render("Appuie sur Entrée pour jouer", True, (255, 255, 255))

        # Ajout d'ombres pour le titre
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2 + 2, HAUTEUR // 3 + 2)))  # Ombre
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 3)))  # Titre principal

        # Positionnement des sous titres
        ecran.blit(sous_titre1, sous_titre1.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
        ecran.blit(sous_titre2, sous_titre2.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 40)))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                en_menu = False


def collision(rect1, rect2):
    return rect1.colliderect(rect2)

def afficher_vies(vies):
    for i in range(vies):
        x = 10 + i * 35
        y = 40
        ecran.blit(Vie_img, (x, y))

def lancer_jeu():
    joueur_x = LARGEUR // 2
    joueur_y = HAUTEUR - 100
    v_joueur = 10
    voitures = []
    bonus = []
    delai = 50
    timer = 0
    score = 0
    vies = 3  # Nombre de vies
    en_jeu = True
    v_voiture = 4
    niveau_difficulte = 1  # Niveau de difficulté
    invincible = False  # État d'invincibilité
    invincibility_timer = 0  # Timer pour l'invincibilité
    pieces_collectees = 0  # Compteur de pièces collectées

    voie_voiture = [((LARGEUR - 300) // 2) + 10, LARGEUR // 2 - 40, ((LARGEUR - 300) // 2) + 210]

    while en_jeu:
        dessiner_fond()
        afficher_vies(vies)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            joueur_x -= v_joueur
        if touches[pygame.K_RIGHT]:
            joueur_x += v_joueur

        route_x = (LARGEUR - 300) // 2
        joueur_x = max(route_x, min(joueur_x, route_x + 300 - 40))

        timer += 1
        if timer >= delai:
            voiture_x = random.choice(voie_voiture)
            voitures.append([voiture_x, -90])

            # Bonus aléatoires 
            bonus_voies_dispo = [x for x in voie_voiture if x != voiture_x]
            if random.random() < 0.4 and bonus_voies_dispo:
                bonus_x = random.choice(bonus_voies_dispo)
                bonus.append([bonus_x, -30])

            # Bonus d'invincibilité très rare
            if random.random() < 0.15 and bonus_voies_dispo:  # 15% de chance d'apparition
                invincibility_x = random.choice(bonus_voies_dispo)
                bonus.append([invincibility_x, -30])

            timer = 0

        for v in voitures:
            v[1] += v_voiture
        voitures = [v for v in voitures if v[1] < HAUTEUR]

        for b in bonus:
            b[1] += v_voiture
        bonus = [b for b in bonus if b[1] < HAUTEUR]

        rect_joueur = pygame.Rect(joueur_x + 4, joueur_y + 4, 32, 42)

        # Collision voitures
        for v in voitures:
            rect_v = pygame.Rect(v[0] + 8, v[1] + 8, 64, 74)
            if collision(rect_joueur, rect_v):
                if not invincible:  # Si le joueur n'est pas invincible
                    vies -= 1
                    voitures.remove(v)
                    collision_sound.play()  # Joue le son de collision
                    if vies <= 0:
                        en_jeu = False
                break  # Évite de perdre plusieurs vies d’un coup

        # Collecte bonus 
        for b in bonus[:]:
            rect_b = pygame.Rect(b[0], b[1], 20, 20)
            if collision(rect_joueur, rect_b):
                if b[1] == -30:  # Bonus d'invincibilité
                    invincible = True
                    invincibility_timer = 300  # 5 secondes à 60 FPS
                    bonus.remove(b)
                else:
                    score += 100
                    pieces_collectees += 1  # Incrémente le compteur de pièces collectées
                    bonus.remove(b)
                    bonus_sound.play()  # Joue le son de bonus

                    # Vérifie si le joueur a collecté 5 pièces
                    if pieces_collectees >= 5:
                        vies += 1  # Ajoute une vie
                        pieces_collectees = 0  # Réinitialise le compteur de pièces collectées

        # Gérer l'invincibilité
        if invincible:
            invincibility_timer -= 1
            if invincibility_timer <= 0:
                invincible = False  # Fin de l'invincibilité

        # Augmenter la difficulté
        if score // 100 > niveau_difficulte:  # Chaque 100 points
            niveau_difficulte += 1
            v_voiture += 1  # Augmente la vitesse des voitures
            delai = max(20, delai - 5)  # Diminue le délai d'apparition des voitures

        ecran.blit(ambulance_img, (joueur_x, joueur_y))
        for v in voitures:
            ecran.blit(voiture_img, (v[0], v[1]))
        for b in bonus:
            if b[1] == -30:  # Bonus d'invincibilité
                ecran.blit(invincibility_img, (b[0], b[1]))  # Affiche le bonus d'invincibilité
            else:
                ecran.blit(bonus_img, (b[0], b[1]))

        score += 1  # Score continue à augmenter
        score_txt = police.render("Score : " + str(score), True, BLANC)
        ecran.blit(score_txt, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    return score

def ecran_fin(score):
    continuer = True
    while continuer:
        ecran.blit(gameover_img, (0, 0))  # Utilise la variable gameover_img
        texte1 = police.render(f"T'a perdu sale noob XD - Score : {score}", True, (255, 255, 255))
        texte2 = police.render("Entrée pour rejouer | Échap pour quitter", True, (255, 255, 255))
        
        ecran.blit(texte1, texte1.get_rect(center=(LARGEUR // 2, 180)))
        ecran.blit(texte2, texte2.get_rect(center=(LARGEUR // 2, 220)))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    continuer = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
# Boucle principale
while True:
    afficher_menu()
    score_final = lancer_jeu()
    ecran_fin(score_final)
