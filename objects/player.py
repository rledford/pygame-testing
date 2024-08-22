from typing_extensions import Optional, NotRequired
import pygame
from core import utils
from core.entity import PhysicsEntity, PhysicsEntityProps
from core.events import (
    A_JUMP,
    A_LEFT,
    A_RIGHT,
    E_INPUT,
    GameActionEvent,
    GameEvent,
)
from core.game import Game


class PlayerProps(PhysicsEntityProps):
    speed: NotRequired[float]
    accel: NotRequired[float]
    decel: NotRequired[float]
    max_fall_speed: NotRequired[float]


class Player(PhysicsEntity):
    def __init__(self, game: Game, props: Optional[PlayerProps] = None):
        super().__init__()
        self.game = game
        self.direction: list[float] = [0, 0]
        self.speed = 30
        self.accel = 1800
        self.decel = 1800
        self.gravity = 10
        self.max_fall_speed = 50
        self.is_grounded = False

        self.game.router.on(E_INPUT, self.id, self.handle_event)
        self.game.add_entity(self)

        self.set_props(props)

    @property
    def dx(self):
        return self.direction[0] + self.direction[1]

    def update(self, dt: float):
        if self.dx != 0:
            new_vx = self.vx + (self.accel * self.dx * dt)
            self.vx = utils.clamp(new_vx, -self.speed, self.speed)
        elif self.dx == 0 and self.vx != 0:
            decel_dir = -utils.sign(self.vx)
            self.vx += self.decel * decel_dir * dt
            if utils.sign(self.vx) == decel_dir:
                self.vx = 0

        next_x = self.x + self.vx * dt
        # check horizonal collisions and set x accordingly
        next_collider = self.next_collider(next_x, self.y)
        other_collider: pygame.Rect
        for p in self.game.platforms:
            other_collider = p.collider
            if other_collider.colliderect(next_collider):
                self.vx = 0
                if self.x < other_collider.centerx:
                    next_collider.right = other_collider.left
                elif self.x > other_collider.centerx:
                    next_collider.left = other_collider.right
                next_x = next_collider.centerx
                break
        self.x = next_x

        self.apply_gravity(dt)
        next_y = self.y + self.vy * dt
        # check vertical collisions
        next_collider = self.next_collider(self.x, next_y)
        for p in self.game.platforms:
            other_collider = p.collider
            if other_collider.colliderect(next_collider):
                if self.y < other_collider.centery:
                    next_collider.bottom = other_collider.top
                    self.is_grounded = True
                    self.vy = 0
                elif self.y > other_collider.centery:
                    next_collider.top = other_collider.bottom
                    self.vy *= 0.25
                next_y = next_collider.centery
                break
        self.y = next_y

    def apply_gravity(self, dt: float):
        if self.is_grounded:
            return
        amt = self.gravity if self.vy <= 0 else self.gravity * 1.875
        self.vy += amt * dt

    def handle_action(self, event: GameActionEvent):
        if event.action == A_LEFT:
            self.direction[0] = -1 if event.pressed else 0
        elif event.action == A_RIGHT:
            self.direction[1] = 1 if event.pressed else 0
        elif event.action == A_JUMP and event.pressed:
            if self.is_grounded:
                self.vy -= 800
                self.is_grounded = False

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, 25)
        super().draw(surface)

    def handle_event(self, event: GameEvent):
        if isinstance(event, GameActionEvent):
            self.handle_action(event)
