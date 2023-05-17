import arcade


class Rectangle:
    def __init__(self, center_x, center_y, width, height, color=arcade.color.RED):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.width = width
        self.height = height

    def draw(self):
        arcade.draw_lrtb_rectangle_outline(self.center_x - self.width / 2, self.center_x + self.width / 2,
                                           self.center_y + self.height / 2, self.center_y - self.height / 2,
                                           self.color)
