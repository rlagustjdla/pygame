import pygame
import random
import math
from settings import *

class ItemManager:
    def __init__(self):
        self.items = []
        self.collected_items = []
        self.size = ITEM_SIZE

        self.item_types = ["button", "sound", "shock", "light"]
        self.images = {}
        for name in self.item_types:
            image = pygame.image.load(f"assets/{name}.PNG").convert_alpha()
            image = pygame.transform.scale(image, (self.size, self.size))
            self.images[name] = image

    def update(self, dt):
        self.items = [item for item in self.items if not self._is_out(item) and not item["collected"]]

        while len(self.items) < LIMITED_ITEMS:
            angle = random.uniform(0, 2 * math.pi)
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            pos = pygame.Vector2(x, y)

            direction = (pygame.Vector2(CENTER) - pos).normalize()
            speed = random.randint(MONSTER_MIN_SPEED, MONSTER_MAX_SPEED)
            item_type = random.choice(self.item_types)

            item = {
                "pos": pos,
                "dir": direction,
                "speed": speed,
                "type": item_type,
                "collected": False
            }

            self.items.append(item)

        for item in self.items:
            item["pos"] += item["dir"] * item["speed"] * dt

    def draw(self, screen):
        for item in self.items:
            screen.blit(self.images[item["type"]], item["pos"])

    def check_collision(self, collider):
        left, right, top, bottom = collider
        for item in self.items:
            if left < item["pos"].x < right and top < item["pos"].y < bottom and len(self.collected_items) < 3:
                item["collected"] = True
                self.collected_items.append(item)
                print("아이템 먹음", len(self.collected_items))
                return True
        return False

    def _is_out(self, item):
        return item["pos"].distance_to(CENTER) > RADIUS

    def use_item(self, message):
        # 가지고 있는 아이템 중에
        for item in self.collected_items:
            # "message" 아이템이 있으면
            if item["type"] == message:
                # 그 아이템을 사용한다.
                print(f"아이템 {message} 사용")
                # 가진 아이템 중에서 뺀다.
                self.collected_items.remove(item)
                # 사용할 아이템 반환
                return message


    def draw_collection(self, screen):
        x = 20
        y = SCREEN_HEIGHT - 20
        gap = self.size + 10

        for i, item in enumerate(self.collected_items):
            pos = pygame.Vector2(x + i * gap, y)
            screen.blit(self.images[item["type"]], pos)