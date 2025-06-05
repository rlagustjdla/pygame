import pygame
import random
import math
from settings import *

class ItemManager:
    def __init__(self, arrows, player):
        self.items = []
        self.collected_items = []
        self.size = ARROW_SIZE
        self.arrows = arrows  # ArrowManager 객체
        self.player = player  # Player 객체

    def update(self, dt):
        # 원 안에 있는 화살만 다시 만든다.
        self.items = [a for a in self.items if not self._is_out(a) and not a[4]]

        while len(self.items) < LIMITED_ITEMS:
            # RADIUS를 반지름으로 갖는 원 테투리 위의 랜덤한 좌표 생성
            angle = random.uniform(0, 2 * math.pi)
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            pos = pygame.Vector2(x, y)

            # 센터를 중심으로 벡터 구한다.
            direction = (pygame.Vector2(CENTER) - pos).normalize()      # 방향만 기억하면 되므로 normalize한다.

            speed = random.randint(ARROW_MIN_SPEED, ARROW_MAX_SPEED)

            index = random.choice([1, 2, 3])  # 3종류로 제한

            self.items.append([pos, direction, speed, index, False])

        # 상하좌우가 아닌 생성된 방향으로 이동한다.
        for item in self.items:
            item[0] += item[1] * item[2] * dt  # pos += direction * speed * dt

    def draw(self, screen):
        for item in self.items:
            # 색상 설정 (각각 3가지 아이템 색상)
            if item[3] == 1:
                pygame.draw.circle(screen, (255, 127, 127), item[0], self.size / 2)
            elif item[3] == 2:
                pygame.draw.circle(screen, (255, 185, 127), item[0], self.size / 2)
            elif item[3] == 3:
                pygame.draw.circle(screen, (255, 255, 127), item[0], self.size / 2)

    def check_collision(self, collider):
        left, right, top, bottom = collider
        for item in self.items:
            if left < item[0].x < right and top < item[0].y < bottom and len(self.collected_items) < 3:
                item[4] = True
                self.collected_items.append(item)
                print("아이템 먹음", len(self.collected_items))
                return True
        return False

    def _is_out(self, item):
        # 중심으로부터 거리가 반지름 이상인지
        return item[0].distance_to(CENTER) > RADIUS

    def use_item(self, item_num):
        # 아이템 사용 효과
        if item_num == 1:
            self.freeze_obstacles()
        elif item_num == 2:
            self.clear_all_obstacles()
        elif item_num == 3:
            self.activate_shield()

    def freeze_obstacles(self):
        print("아이템 1 발동: 장애물 정지")
        self.arrows.freeze(2)  # 2초 동안 장애물 정지

    def clear_all_obstacles(self):
        print("아이템 2 발동: 모든 장애물 제거")
        self.arrows.clear_all()  # 모든 장애물 제거

    def activate_shield(self):
        print("아이템 3 발동: 쉴드 활성화")
        self.player.activate_shield(2.0)  # 2초 동안 쉴드 활성화

    def draw_collection(self, screen):
        x = 20
        y = SCREEN_HEIGHT - 20
        gap = self.size + 10  # 아이템 간 간격

        for i, item in enumerate(self.collected_items):
            pos = pygame.Vector2(x + i * gap, y)
            color = (255, 255, 255)
            if item[3] == 1:
                color = (255, 127, 127)
            elif item[3] == 2:
                color = (255, 185, 127)
            elif item[3] == 3:
                color = (255, 255, 127)

            pygame.draw.circle(screen, color, pos, self.size / 2)
