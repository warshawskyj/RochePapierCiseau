"""
Modèle de départ pour la programmation Arcade.
Il suffit de modifier les méthodes nécessaires à votre jeu.
"""

import random
from arcade import Sprite
import arcade
from rectangle import Rectangle
from attack_animations import AttackType, Animation
from game_state import GameState, GameOutcome
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
ANIMATION_INTERVAL = 0.2


class MyGame(arcade.Window):
    """
   La classe principale de l'application

   NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
   Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
   """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        # création des textures pour les diverses attaques
        self.rock_texture = arcade.load_texture("assets/srock.png")
        self.paper_texture = arcade.load_texture("assets/spaper.png")
        self.scissors_texture = arcade.load_texture("assets/scissors.png")
        self.rock_attack = arcade.load_texture("assets/srock-attack.png")
        self.spaper_attack = arcade.load_texture("assets/spaper-attack.png")
        self.scissors_attack = arcade.load_texture("assets/scissors-attack.png")
        
        #création des sprites qui vont alterner entre les deux images chaque ANIMATION_INTERVAL pour le joueur
        #ainsi que les rectangles qui encadrent les attaques
        self.player_rock = Animation(ANIMATION_INTERVAL, [self.rock_texture, self.rock_attack],
                                     center_x=PLAYER_IMAGE_X - ATTACK_FRAME_WIDTH * 2, center_y=ATTACK_ROW,
                                     image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.player_rock_rectangle = Rectangle(PLAYER_IMAGE_X - ATTACK_FRAME_WIDTH * 2, ATTACK_ROW, ATTACK_FRAME_WIDTH,
                                               ATTACK_FRAME_HEIGHT)
        self.player_paper = Animation(ANIMATION_INTERVAL, [self.paper_texture, self.spaper_attack],
                                      center_x=PLAYER_IMAGE_X, center_y=ATTACK_ROW, image_width=ATTACK_FRAME_WIDTH,
                                      image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.player_paper_rectangle = Rectangle(PLAYER_IMAGE_X, ATTACK_ROW, ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        self.player_scissors = Animation(ANIMATION_INTERVAL, [self.scissors_texture, self.scissors_attack],
                                         center_x=PLAYER_IMAGE_X + ATTACK_FRAME_WIDTH * 2, center_y=ATTACK_ROW,
                                         image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.player_scissors_rectangle = Rectangle(PLAYER_IMAGE_X + ATTACK_FRAME_WIDTH * 2, ATTACK_ROW,
                                                   ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        #même chose mais pour l'ordi
        #tous les sprites sont au même endroit, car qu'une seule attaque de l'ordi sera affiché à la fois
        self.comp_rock = Animation(ANIMATION_INTERVAL, [self.rock_texture, self.rock_attack],
                                     center_x=COMPUTER_IMAGE_X, center_y=ATTACK_ROW,
                                     image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.comp_rock_rectangle = Rectangle(COMPUTER_IMAGE_X, ATTACK_ROW, ATTACK_FRAME_WIDTH,
                                               ATTACK_FRAME_HEIGHT)
        self.comp_paper = Animation(ANIMATION_INTERVAL, [self.paper_texture, self.spaper_attack],
                                      center_x=COMPUTER_IMAGE_X, center_y=ATTACK_ROW, image_width=ATTACK_FRAME_WIDTH,
                                      image_height=ATTACK_FRAME_HEIGHT, scale=0.5)
        self.comp_paper_rectangle = Rectangle(COMPUTER_IMAGE_X, ATTACK_ROW, ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        self.comp_scissors = Animation(ANIMATION_INTERVAL, [self.scissors_texture, self.scissors_attack],
                                         center_x=COMPUTER_IMAGE_X, center_y=ATTACK_ROW,
                                         image_width=ATTACK_FRAME_WIDTH, image_height=ATTACK_FRAME_HEIGHT, scale=0.5)

        self.comp_scissors_rectangle = Rectangle(COMPUTER_IMAGE_X, ATTACK_ROW,
                                                   ATTACK_FRAME_WIDTH, ATTACK_FRAME_HEIGHT)
        self.player_attacks = [self.player_rock, self.player_paper, self.player_scissors]
        self.player_rectangles = [self.player_rock_rectangle, self.player_paper_rectangle, self.player_scissors_rectangle]
        #les sprites du joueur et de l'ordi
        self.player_sprite = Sprite("assets/faceBeard.png", center_x=PLAYER_IMAGE_X, center_y=PLAYER_IMAGE_Y, scale=0.4)
        self.computer_sprite = Sprite("assets/compy.png", center_x=COMPUTER_IMAGE_X, center_y=COMPUTER_IMAGE_Y, scale=2)

        # textes pour montrer les scores, les instructions ainsi que le résultat du jeu
        self.player_score_text = arcade.Text("", PLAYER_IMAGE_X - ATTACK_FRAME_WIDTH * 1.5, ATTACK_ROW - 75, arcade.color.WHITE, 20)
        self.computer_score_text = arcade.Text("", COMPUTER_IMAGE_X - ATTACK_FRAME_WIDTH * 1.5, ATTACK_ROW - 75, arcade.color.WHITE, 20)
        self.instruction_text = arcade.Text("", SCREEN_WIDTH / 4, SCREEN_HEIGHT * 0.75, arcade.color.WHITE, 20)
        self.outcome_text = arcade.Text("", SCREEN_WIDTH * 0.4, SCREEN_HEIGHT / 2, arcade.color.WHITE, 20)
        #variables représentant l'état du jeu
        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = None
        self.computer_attack_type = None
        self.game_state = GameState.NOT_STARTED
        self.outcome = None
        
    def draw_possible_attack(self):
        """
       Méthode utilisée pour dessiner toutes les possibilités d'attaque du joueur
       (si aucune attaque n'a été sélectionnée, il faut dessiner les trois possibilités)
       (si une attaque a été sélectionnée, il faut dessiner cette attaque)
       """
        #pour chaque attaque, si aucune attaque n'a encore été choisie
        #ou cette attaque a été choisie, on l'affiche
        if self.player_attack_type is None or self.player_attack_type == 0:
            self.player_rock.draw()
            self.player_rock_rectangle.draw()
        if self.player_attack_type is None or self.player_attack_type == 1:
            self.player_paper.draw()
            self.player_paper_rectangle.draw()
        if self.player_attack_type is None or self.player_attack_type == 2:
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
        if self.game_state == GameState.ROUND_DONE: #afficher l'attaque de l'ordi seulement après que le joueur a choisi son attaque
            if self.computer_attack_type == 0:
                self.comp_rock.draw()
                self.comp_rock_rectangle.draw()
            elif self.computer_attack_type == 1:
                self.comp_paper.draw()
                self.comp_paper_rectangle.draw()
            elif self.computer_attack_type == 2:
                self.comp_scissors.draw()
                self.comp_scissors_rectangle.draw()

    def draw_scores(self):
        """
       Montrer les scores du joueur et de l'ordinateur
       """
        self.player_score_text.text = "Vous avez " + str(self.player_score) + " points"
        self.computer_score_text.text = "L'ordinateur a " + str(self.computer_score) + " points"
        self.player_score_text.draw()
        self.computer_score_text.draw()

    def draw_instructions(self):
        """
       Dépendemment de l'état de jeu, afficher les instructions d'utilisation au joueur (appuyer sur espace, ou sur une image)
       """
        if self.game_state == GameState.NOT_STARTED:
            self.instruction_text.text = 'Appuyez sur espace pour commencer la partie'
        elif self.game_state == GameState.ROUND_ACTIVE:
            self.instruction_text.text = 'Appuyez sur une image pour faire une attaque'
        elif self.game_state == GameState.ROUND_DONE:
            self.instruction_text.text = 'Appuyez sur espace pour commencer une nouvelle ronde'
        elif self.game_state == GameState.GAME_OVER:
            self.instruction_text.text = 'Appuyez sur espace pour commencer une nouvelle partie'
        self.instruction_text.draw()

    def draw_result(self):
        """
        changer le texte pour que ce dernier affiche le gagant de la partie précédente
        """
        if self.game_state == GameState.ROUND_DONE:
            if self.outcome == GameOutcome.PLAYER_WON:
                self.outcome_text.text = "Vous avez gagné!"
            elif self.outcome == GameOutcome.COMPUTER_WON:
                self.outcome_text.text = "L'ordinateur a gagné!"
            elif self.outcome == GameOutcome.DRAW:
                self.outcome_text.text = "Égalité!"
        else:
            self.outcome_text.text = ""
        self.outcome_text.draw()
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
        #afficher tous les composants du jeu
        self.draw_instructions()
        self.draw_players()
        self.draw_possible_attack()
        self.draw_scores()
        self.draw_result()
        self.draw_computer_attack()

    def on_update(self, delta_time):
        """
       Toute la logique pour déplacer les objets de votre jeu et de
       simuler sa logique vont ici. Normalement, c'est ici que
       vous allez invoquer la méthode "update()" sur vos listes de sprites.
       Paramètre:
           - delta_time : le nombre de milliseconde depuis le dernier update.
       """
        # faire les animations
        self.player_rock.update(delta_time)
        self.player_paper.update(delta_time)
        self.player_scissors.update(delta_time)
        self.comp_rock.update(delta_time)
        self.comp_paper.update(delta_time)
        self.comp_scissors.update(delta_time)
        #determiner si un joueur a gagné
        if self.player_score == 3 or self.computer_score == 3:
            self.game_state = GameState.GAME_OVER



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
        #avancer le gamestate quand espace est appuyée
        if key == arcade.key.SPACE and self.game_state == GameState.NOT_STARTED:
            self.game_state = GameState.ROUND_ACTIVE
        elif key == arcade.key.SPACE and self.game_state == GameState.ROUND_DONE:
            self.game_state = GameState.ROUND_ACTIVE
            self.player_attack_type = None
        elif key == arcade.key.SPACE and self.game_state == GameState.GAME_OVER:
            self.reset_round()


    def reset_round(self):
        """
       Réinitialiser les variables qui ont été modifiées pour pouvoir commence une nouvelle partie
       """
        self.game_state = GameState.NOT_STARTED
        self.player_attack_type = None
        self.computer_attack_type = None
        self.outcome = None
        self.player_score = 0
        self.computer_score = 0

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
       Méthode invoquée lorsque l'usager clique un bouton de la souris.
       Paramètres:
           - x, y: coordonnées où le bouton a été cliqué
           - button: le bouton de la souris appuyé
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
       """
        #le joueur peut seulement choisir une attaque si cela n'a pas déjà été faite
        if self.game_state == GameState.ROUND_ACTIVE:
             # Test de collision entre la souris et les rectangles des attaques différentes
            for i in range(len(self.player_rectangles)):
                rect = self.player_rectangles[i]
                if rect.center_x - rect.width / 2 < x < rect.center_x + rect.width / 2 and rect.center_y - rect.height / 2 < y < rect.center_y + rect.height / 2:
                    self.player_attack_type = i
                    #choisir l'attaque de l'ordi
                    self.computer_attack_type = random.randint(0, 2)
                    #déterminer le gagnant et changer le score
                    if self.player_attack_type == self.computer_attack_type:
                        self.outcome = GameOutcome.DRAW
                    elif self.player_attack_type == (self.computer_attack_type + 1) % 3:
                        self.outcome = GameOutcome.PLAYER_WON
                        self.player_score += 1
                    else:
                        self.outcome = GameOutcome.COMPUTER_WON
                        self.computer_score += 1
                    self.game_state = GameState.ROUND_DONE



def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
