"""
Modèle de départ pour la programmation Arcade.
Il suffit de modifier les méthodes nécessaires à votre jeu.
"""

import random
from arcade import Sprite
import arcade
from rectangle import Rectangle
from attack_animations import AttackType, Animation
from game_state import GameState
from PIL.Image import open as open_image

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.

PLAYER_IMAGE_X = SCREEN_WIDTH * 0.25
PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2
COMPUTER_IMAGE_X = SCREEN_WIDTH * 0.75
COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2
ATTACK_ROW = SCREEN_HEIGHT * 0.25
ATTACK_FRAME_WIDTH = 154 / 2
ATTACK_FRAME_HEIGHT = 154 / 2
ANIMATION_INTERVAL = 0.1

class MyGame(arcade.Window):
    """
   La classe principale de l'application

   NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
   Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
   """


    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        # creation des textures
        self.rock_texture = arcade.load_texture("assets/srock.png")
        self.paper_texture = arcade.load_texture("assets/spaper.png")
        self.scissors_texture = arcade.load_texture("assets/scissors.png")
        self.rock_attack = arcade.load_texture("assets/srock-attack.png")
        self.spaper_attack = arcade.load_texture("assets/spaper-attack.png")
        self.scissors_attack = arcade.load_texture("assets/scissors-attack.png")

        self.player_rock = Animation(ANIMATION_INTERVAL, [self.rock_texture, self.rock_attack],
                                     center_x=PLAYER_IMAGE_X - ATTACK_FRAME_WIDTH * 2, center_y=ATTACK_ROW, image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.player_rock_rectangle = Rectangle(PLAYER_IMAGE_X - ATTACK_FRAME_WIDTH * 2, ATTACK_ROW, ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        self.player_paper = Animation(ANIMATION_INTERVAL, [self.paper_texture, self.spaper_attack],
                                      center_x=PLAYER_IMAGE_X, center_y=ATTACK_ROW, image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.player_paper_rectangle = Rectangle(PLAYER_IMAGE_X, ATTACK_ROW, ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        self.player_scissors = Animation(ANIMATION_INTERVAL, [self.scissors_texture, self.scissors_attack],
                                         center_x=PLAYER_IMAGE_X + ATTACK_FRAME_WIDTH * 2, center_y=ATTACK_ROW, image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)

        self.player_scissors_rectangle = Rectangle(PLAYER_IMAGE_X + ATTACK_FRAME_WIDTH * 2, ATTACK_ROW,
                                                   ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        self.player_sprite = Sprite("assets/faceBeard.png", center_x=PLAYER_IMAGE_X, center_y=PLAYER_IMAGE_Y, scale=0.4)
        self.computer_sprite = Sprite("assets/compy.png", center_x=COMPUTER_IMAGE_X, center_y=COMPUTER_IMAGE_Y)
        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = None
        self.computer_attack_type = None
        self.player_won_round = None
        self.draw_round = None
        self.game_state = None

    def setup(self):
        """
       Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
       fois si vous recommencer une nouvelle partie.
       """
        # C'est ici que vous allez créer vos listes de sprites et vos sprites.
        # Prenez note que vous devriez attribuer une valeur à tous les attributs créés dans __init__


    def validate_victory(self):
        """
       Utilisé pour déterminer qui obtient la victoire (ou s'il y a égalité)
       Rappel: après avoir validé la victoire, il faut changer l'état de jeu
       """

    def draw_possible_attack(self):
        """
       Méthode utilisée pour dessiner toutes les possibilités d'attaque du joueur
       (si aucune attaque n'a été sélectionnée, il faut dessiner les trois possibilités)
       (si une attaque a été sélectionnée, il faut dessiner cette attaque)
       """
        self.player_rock.draw()
        self.player_rock_rectangle.draw()
        self.player_paper.draw()
        self.player_paper_rectangle.draw()
        self.player_scissors.draw()
        self.player_scissors_rectangle.draw()

    def draw_players(self):
        """
       Méthode utilisée pour dessiner les joueurs
       """
        self.player_sprite.draw()
        self.computer_sprite.draw()

    def draw_computer_attack(self):
        """
       Méthode utilisée pour dessiner les possibilités d'attaque de l'ordinateur
       """
        pass

    def draw_scores(self):
        """
       Montrer les scores du joueur et de l'ordinateur
       """
        pass

    def draw_instructions(self):
        """
       Dépendemment de l'état de jeu, afficher les instructions d'utilisation au joueur (appuyer sur espace, ou sur une image)
       """
        pass

    def on_draw(self):
        """
       C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
       de votre jeu à l'écran.
       """

        # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
        # plan selon la couleur spécifié avec la méthode "set_background_color".
        arcade.start_render()

        # Display title
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")

        self.draw_instructions()
        self.draw_players()
        self.draw_possible_attack()
        self.draw_scores()

        # afficher l'attaque de l'ordinateur selon l'état de jeu
        # afficher le résultat de la partie si l'ordinateur a joué (ROUND_DONE)
        pass

    def on_update(self, delta_time):
        """
       Toute la logique pour déplacer les objets de votre jeu et de
       simuler sa logique vont ici. Normalement, c'est ici que
       vous allez invoquer la méthode "update()" sur vos listes de sprites.
       Paramètre:
           - delta_time : le nombre de milliseconde depuis le dernier update.
       """
        # vérifier si le jeu est actif (ROUND_ACTIVE) et continuer l'animation des attaques
        # si le joueur a choisi une attaque, générer une attaque de l'ordinateur et valider la victoire
        # changer l'état de jeu si nécessaire (GAME_OVER)
        #faire les animations
        self.player_rock.update(delta_time)
        self.player_paper.update(delta_time)
        self.player_scissors.update(delta_time)

    def on_key_press(self, key, key_modifiers):
        """
       Cette méthode est invoquée à chaque fois que l'usager tape une touche
       sur le clavier.
       Paramètres:
           - key: la touche enfoncée
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

       Pour connaître la liste des touches possibles:
       http://arcade.academy/arcade.key.html
       """
        pass

    def reset_round(self):
        """
       Réinitialiser les variables qui ont été modifiées
       """
        # self.computer_attack_type = -1
        # self.player_attack_chosen = False
        # self.player_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}
        # self.player_won_round = False
        # self.draw_round = False

        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
       Méthode invoquée lorsque l'usager clique un bouton de la souris.
       Paramètres:
           - x, y: coordonnées où le bouton a été cliqué
           - button: le bouton de la souris appuyé
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
       """

        # Test de collision pour le type d'attaque (self.player_attack_type).
        # Rappel que si le joueur choisi une attaque, self.player_attack_chosen = True
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
