SYSTEM_SENDER = 9999

E_RENDER = 1000
E_INPUT = 1001

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


class GameEvent:
    def __init__(self, code: int, sender: int):
        self.code = code
        self.sender = sender


class GameActionEvent(GameEvent):
    def __init__(self, action: int, pressed: bool, sender: int = SYSTEM_SENDER):
        GameEvent.__init__(self, code=E_INPUT, sender=sender)
        self.action = action
        self.pressed = pressed
