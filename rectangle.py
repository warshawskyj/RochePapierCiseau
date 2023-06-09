import arcade


class Rectangle:
    """
    une classe possédant les caractèristiques nécessaires pour afficher un rectangle dans arcade
    """
    def __init__(self, center_x, center_y, width, height, color=arcade.color.RED):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.width = width
        self.height = height

    def draw(self):
        #il faut soustraire la moitié des dimensions du point central pour trouver les extrémités
        arcade.draw_lrtb_rectangle_outline(self.center_x - self.width / 2, self.center_x + self.width / 2,
                                           self.center_y + self.height / 2, self.center_y - self.height / 2,
                                           self.color)
