from enum import Enum
from arcade import Sprite


class Animation(Sprite):
    def __init__(self, interval, frames, *args, **kwargs):
        """
        Une classe qui permet de gerer automatiquement des animations.
        interval: le temps entre chaque frame
        frames: une liste de sprites
        """
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.frames = frames
        self.current_frame = 0
        #la texture actuelle
        self.texture = self.frames[self.current_frame]
        self.time_since_last_frame = 0

    def update(self, delta_time):
        self.time_since_last_frame += delta_time
        #il faut passer au prochain frame
        if self.time_since_last_frame > self.interval:
            #le modulo fait en sort que les frames se répétent en boucle
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_since_last_frame = 0
            self.texture = self.frames[self.current_frame]
