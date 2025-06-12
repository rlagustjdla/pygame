import pygame
from settings import * 

class Player:
    def __init__(self):
        self.pos = pygame.Vector2(CENTER[0], CENTER[1])
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.shield_timer = 0
        self.shield_radius = self.size * 1.2

    def move(self, dt, keys=None, joystick_updown=None, joystick_leftright=None):
        if self.shield_timer > 0:
            self.shield_timer -= dt
        delta = pygame.Vector2(0, 0)

        if keys:
            if keys[pygame.K_w]: delta.y -= self.speed * dt
            if keys[pygame.K_s]: delta.y += self.speed * dt
            if keys[pygame.K_a]: delta.x -= self.speed * dt
            if keys[pygame.K_d]: delta.x += self.speed * dt

        # 조이스틱 값으로 움직임 처리
        if joystick_updown is not None:
            if 0 < joystick_updown < 100 and self.pos.x > (0 - self.size / 2):
                delta.x -= self.speed * dt
            if joystick_updown > 220 and self.pos.x < (SCREEN_WIDTH - self.size / 2):
                delta.x += self.speed * dt

        if joystick_leftright is not None:
            if 0 < joystick_leftright < 100 and self.pos.y > (0 - self.size / 2):
                delta.y -= self.speed * dt
            if joystick_leftright > 220 and self.pos.y < (SCREEN_HEIGHT - self.size / 2):
                delta.y += self.speed * dt

        new_pos = self.pos + delta
        if new_pos.distance_to(CENTER) <= RADIUS:
            self.pos = new_pos

    def draw(self, screen):
        draw_pos = self.pos - pygame.Vector2(self.size / 2, self.size / 2)
        pygame.draw.circle(screen, (127, 127, 127), draw_pos, self.size / 2)

        if self.shield_timer > 0:
            pygame.draw.circle(screen, (127, 127, 255), draw_pos, self.shield_radius, 3)

    def get_collider(self):
        return (
            self.pos.x - self.size / 2, self.pos.x + self.size / 2,
            self.pos.y - self.size / 2, self.pos.y + self.size / 2
        )

    def activate_shield(self, duration):
        self.shield_timer = duration
