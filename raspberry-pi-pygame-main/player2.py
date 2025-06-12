import pygame
from settings import *

class Player:
    def __init__(self, sprite_path1, sprite_path2): # 이미지 경로를 받아오도록 __init__ 수정
        self.pos = pygame.Vector2(CENTER[0], CENTER[1])
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.shield_timer = 0
        self.shield_radius = self.size * 1.2
        
        # 플레이어 이미지 로드 및 크기 조정
        self.image1 = pygame.image.load(sprite_path1).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (self.size, self.size))
        self.image2 = pygame.image.load(sprite_path2).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (self.size, self.size))
        self.current_image = self.image1 # 현재 사용할 이미지
        
        self.animation_timer = 0
        self.animation_speed = 0.2 # 이미지 전환 속도 (초)

    def move(self, dt, keys=None, joystick_updown=None, joystick_leftright=None):
        if self.shield_timer > 0:
            self.shield_timer -= dt
            
        # 플레이어 애니메이션 업데이트
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.current_image == self.image1:
                self.current_image = self.image2
            else:
                self.current_image = self.image1

        delta = pygame.Vector2(0, 0)
        
        # 키보드 입력 처리 (기존 로직 유지)
        if keys:
            if keys[pygame.K_w]: delta.y -= self.speed * dt
            if keys[pygame.K_s]: delta.y += self.speed * dt
            if keys[pygame.K_a]: delta.x -= self.speed * dt
            if keys[pygame.K_d]: delta.x += self.speed * dt

        # 조이스틱 상하 (joystick_updown) -> 플레이어 Y축 (상하) 움직임
        if joystick_updown is not None:
            normalized_y_input = (joystick_updown - 127) / 127.0 # 대략 -1.0 ~ 1.0 범위
            delta.y += normalized_y_input * self.speed * dt

        # 조이스틱 좌우 (joystick_leftright) -> 플레이어 X축 (좌우) 움직임
        if joystick_leftright is not None:
            normalized_x_input = (joystick_leftright - 127) / 127.0 # 대략 -1.0 ~ 1.0 범위
            delta.x += normalized_x_input * self.speed * dt

        new_pos = self.pos + delta

        if new_pos.distance_to(CENTER) <= RADIUS:
            self.pos = new_pos
        else:
            direction = new_pos - CENTER
            if direction.length() > 0: # 0으로 나누는 오류 방지
                self.pos = CENTER + direction.normalize() * RADIUS
            else: # 플레이어가 정확히 CENTER에 있을 때 (움직이지 않는 경우)
                self.pos = CENTER

    def draw(self, screen):
        player_rect = self.current_image.get_rect(center=self.pos)
        screen.blit(self.current_image, player_rect)

        if self.shield_timer > 0:
            pygame.draw.circle(screen, (127, 127, 255), self.pos, self.shield_radius, 3)

    def get_collider(self):
        return pygame.Rect(self.pos.x - self.size / 2, self.pos.y - self.size / 2, self.size, self.size)

    def activate_shield(self, duration):
        self.shield_timer = duration