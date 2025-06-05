import pygame
# import smbus
from settings import PLAYER_SIZE, PLAYER_SPEED, CENTER, RADIUS

class Player:
    # 이니셜라이즈
    def __init__(self, image_path):
        self.pos = pygame.Vector2(CENTER[0], CENTER[1])
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.shield_timer = 0
        self.shield_radius = self.size * 1.2  # 시각적 쉴드 반지름
        self.address = 0x48
        self.A0 = 0x40
        self.A1 = 0x41
        # self.bus = smbus.SMBus(1)

    # 움직임 메서드
    def move(self, keys, dt):
        if self.shield_timer > 0:
            self.shield_timer -= dt
        delta = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: delta.y -= self.speed * dt
        if keys[pygame.K_s]: delta.y += self.speed * dt
        if keys[pygame.K_a]: delta.x -= self.speed * dt
        if keys[pygame.K_d]: delta.x += self.speed * dt

        new_pos = self.pos + delta
        if new_pos.distance_to(CENTER) <= RADIUS:
            self.pos = new_pos
        """
        bus.write_byte(address, A0)
        time.sleep(0.01)
        value1 = bus.read_byte(address)

        bus.write_byte(address, A1)
        time.sleep(0.01)
        value2 = bus.read_byte(address)
        
        delta = pygame.Vector2(0, 0)

        if value1 < 100 and player_pos.x > (0 - player_size / 2):
            print("left")
            delta.x -= self.speed * dt
        if value1 > 220 and player_pos.x < (width - player_size / 2):
            print("right")
            delta.x += self.speed * dt
        if value2 < 100 and player_pos.y > (0 - player_size / 2):
            print("up")
            delta.y -= self.speed * dt
        if value2 > 220 and player_pos.y < (height - player_size / 2):
            print("down")
            delta.y += self.speed * dt
        
        new_pos = self.pos + delta
        if new_pos.distance_to(CENTER) <= RADIUS:
            self.pos = new_pos
        """

    # 화면에 그리기
    def draw(self, screen):
        draw_pos = self.pos - pygame.Vector2(self.size / 2, self.size / 2)

        pygame.draw.circle(screen, (127, 127, 127), draw_pos, self.size / 2)

        if self.shield_timer > 0:
            draw_pos = self.pos - pygame.Vector2(self.size / 2, self.size / 2)
            pygame.draw.circle(screen, (127, 127, 255), draw_pos, self.shield_radius, 3)
        # screen.blit(self.image, draw_pos)

    # 콜라이더 각 좌표 반환 (네모 상자)
    def get_collider(self):
        return (
            self.pos.x - self.size / 2, self.pos.x + self.size / 2,
            self.pos.y - self.size / 2, self.pos.y + self.size / 2
        )

    def activate_shield(self, duration):
        self.shield_timer = duration  # 예: 2.0초