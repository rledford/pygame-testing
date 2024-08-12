# Events
import pygame

SYSTEM_SENDER = 9999

E_RERESH = 1000
E_ACTION = 1001

# Actions
A_NONE = 0
A_LEFT = 1
A_RIGHT = 2
A_UP = 3
A_DOWN = 4
A_CONFIRM = 5
A_CANCEL = 6

A_JUMP = 100
A_SHOOT = 101
A_DASH = 102
A_ACTIVATE = 103

PYGAME_KEY_ACTION_MAP = {
    # left
    pygame.K_a: A_LEFT,
    pygame.K_LEFT: A_LEFT,
    # right
    pygame.K_d: A_RIGHT,
    pygame.K_RIGHT: A_RIGHT,
    # up
    pygame.K_w: A_UP,
    pygame.K_UP: A_UP,
    # down
    pygame.K_s: A_DOWN,
    pygame.K_DOWN: A_DOWN,
    # jump
    pygame.K_SPACE: A_JUMP,
    # activate
    pygame.K_e: A_ACTIVATE
}


class GameEvent:
    def __init__(self, code: int, sender: int):
        self.code = code
        self.sender = sender

class GameActionEvent(GameEvent):
    def __init__(self, action: int, pressed: bool, sender: int = SYSTEM_SENDER):
        GameEvent.__init__(self, code=E_ACTION, sender=sender)
        self.action = action
        self.pressed = pressed

    @classmethod
    def from_pygame_key_event(cls, key: int, pressed: bool = False):
        action = PYGAME_KEY_ACTION_MAP.get(key, A_NONE)
        return GameActionEvent(action=action, pressed=pressed)

