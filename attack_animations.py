from enum import Enum
from arcade import Sprite


class AttackType(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class Animation(Sprite):
    def __init__(self, interval, frames, *args, **kwargs):
        """
        Une classe qui permet de gerer automatiquement des animations.
        :param interval: le temps entre chaque frame
        :param frames: une liste de sprites
        """
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.frames = frames
        self.current_frame = 0
        self.texture = self.frames[self.current_frame]
        self.time_since_last_frame = 0

    def update(self, delta_time):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_since_last_frame = 0
            self.texture = self.frames[self.current_frame]
