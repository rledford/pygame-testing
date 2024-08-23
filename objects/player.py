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
    jump_velocity: NotRequired[float]
    max_fall_speed: NotRequired[float]


class Player(PhysicsEntity):
    def __init__(self, game: Game, props: Optional[PlayerProps] = None):
        super().__init__()
        self.game: Game = game
        self.direction: list[float] = [0, 0]
        self.speed: float = 30
        self.accel: float = 1800
        self.decel: float = 1800
        self.gravity: float = 10
        self.jump_velocity = 10
        self.max_fall_speed: float = 50
        self.is_grounded: bool = False
        self.trail: list[list[float]] = []

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

        self.apply_gravity(dt)
        self.check_ground()

        self.move_x(self.vx * dt)
        self.move_y(self.vy * dt)

        self.trail.append([self.x, self.y])
        if len(self.trail) > 500:
            self.trail.pop(0)

    def move_x(self, amt: float):
        if amt == 0:
            return

        next_x = self.x + amt
        collider = self.get_collider(next_x, self.y)
        other_collider: pygame.Rect
        for p in self.game.platforms:
            other_collider = p.get_collider()
            if other_collider.colliderect(collider):
                self.vx = 0
                if next_x < other_collider.centerx:
                    collider.right = other_collider.left
                elif next_x > other_collider.centerx:
                    collider.left = other_collider.right
                next_x = collider.centerx
                break
        self.x = next_x

    def move_y(self, amt: float):
        if amt == 0:
            return

        next_y = self.y + amt
        collider = self.get_collider(self.x, next_y)
        for p in self.game.platforms:
            other_collider = p.get_collider()
            if other_collider.colliderect(collider):
                if self.y < other_collider.centery:
                    collider.bottom = other_collider.top
                    self.is_grounded = True
                    self.vy = 0
                elif self.y > other_collider.centery:
                    collider.top = other_collider.bottom
                    self.vy *= 0.25
                next_y = collider.centery
                break
        self.y = next_y

    def apply_gravity(self, dt: float):
        if self.is_grounded:
            return
        amt = self.gravity if self.vy <= 0 else self.gravity * 1.5
        self.vy += amt * dt

    def check_ground(self):
        collider = self.get_collider(self.x, self.y + 1)
        other_collider: pygame.Rect
        is_grounded = False
        for p in self.game.platforms:
            other_collider = p.get_collider()
            if collider.colliderect(other_collider):
                is_grounded = True
                break

        self.is_grounded = is_grounded

    def handle_action(self, event: GameActionEvent):
        if event.action == A_LEFT:
            self.direction[0] = -1 if event.pressed else 0
        elif event.action == A_RIGHT:
            self.direction[1] = 1 if event.pressed else 0
        elif event.action == A_JUMP and event.pressed:
            if self.is_grounded:
                self.vy -= self.jump_velocity

    def draw(self, surface):
        for point in self.trail:
            pygame.draw.circle(surface, (255, 0, 0), point, 3)
        super().draw(surface)

    def handle_event(self, event: GameEvent):
        if isinstance(event, GameActionEvent):
            self.handle_action(event)
