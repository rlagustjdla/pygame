import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ARROW_MIN_SPEED, ARROW_MAX_SPEED, LIMITED_ARROWS, CENTER, RADIUS, ARROW_SIZE

class ArrowManager:
    # 이니셜라이즈
    def __init__(self, image_path):
        self.arrows = []
        self.size = ARROW_SIZE
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.respawn_delay = 0  # 화살 재생성까지 남은 시간(초)
        self.freeze_timer = 0  # 멈춘 시간 (초)

    def update(self, dt):
        # 딜레이 중이면 딜레이만 감소시키고 return
        if self.respawn_delay > 0:
            self.respawn_delay -= dt
            return

        # 멈춤 중이면 이동 생략 (위치는 그대로, 삭제 & 생성은 계속)
        is_frozen = self.freeze_timer > 0
        if is_frozen:
            self.freeze_timer -= dt

        # 원 안에 있는 화살만 다시 만든다.
        self.arrows = [a for a in self.arrows if not self._is_out(a)]

        while len(self.arrows) < LIMITED_ARROWS:
            # RADIUS를 반지름으로 갖는 원 테투리 위의 랜덤한 좌표 생성

            # 랜덤한 각도 생성
            angle = random.uniform(0, 2 * math.pi)
            # 그 각도에서의 x, y 좌표 구하기
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            pos = pygame.Vector2(x, y)

            # 센터를 중심으로 벡터 구한다.
            direction = (pygame.Vector2(CENTER) - pos).normalize()      # 방향만 기억하면 되므로 normalize한다.

            # 최대 속도와 최저 속도 내에서 랜덤한 속도
            speed = random.randint(ARROW_MIN_SPEED, ARROW_MAX_SPEED)

            self.arrows.append([pos, direction, speed])


        # 상하좌우가 아닌 생성된 방향으로 이동한다.
        if not is_frozen:
            for arrow in self.arrows:
                arrow[0] += arrow[1] * arrow[2] * dt

    # 화면에 그리는 메서드
    def draw(self, screen):
        for arrow in self.arrows:
            # screen.blit(self.image, arrow[0])
            pygame.draw.circle(screen, (127, 127, 255), arrow[0], self.size / 2)

    # 부딪혔는지 확인하는 메서드
    def check_collision(self, collider, shield_active=False):
        if shield_active:
            return False  # 쉴드 중이면 충돌 무시
        left, right, top, bottom = collider
        for arrow in self.arrows:
            if left < arrow[0].x < right and top < arrow[0].y < bottom:
                return True
        return False

    # 화면 밖으로 나갔는지 확인하는 메서드
    def _is_out(self, arrow):
        # 중심으로부터 거리가 반지름 이상인지
        return arrow[0].distance_to(CENTER) > RADIUS

    def clear_all(self):
        self.arrows = []
        self.respawn_delay = 1.0  # 1초 동안 새로 생성하지 않음

    def freeze(self, seconds):
        self.freeze_timer = seconds