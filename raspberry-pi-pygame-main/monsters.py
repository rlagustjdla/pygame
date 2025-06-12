import pygame
import random
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MONSTER_MIN_SPEED, MONSTER_MAX_SPEED, LIMITED_MONSTERS, CENTER, RADIUS, MONSTER_SIZE

class MonsterManger:
    def __init__(self):
        self.monsters = []
        self.size = MONSTER_SIZE

        self.images = []
        # 프레임 나누기
        for i in range(1, 4):
            sheet = pygame.image.load(f"assets/monster{i}.png").convert_alpha()
            sheet_width = sheet.get_width()
            frame_width = sheet_width // 6
            height = sheet.get_height()
            frames = []
            for i in range(6):
                frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, height))
                frame = pygame.transform.scale(frame, (self.size, self.size))
                frames.append(frame)
            self.images.append(frames)

        self.respawn_delay = 0
        self.freeze_timer = 0
        self.slow_timer = 0
        self.frame_delay = 0.5

    def update(self, dt):
        if self.respawn_delay > 0:
            self.respawn_delay -= dt
            return

        is_frozen = self.freeze_timer > 0
        is_slown = self.slow_timer > 0
        if is_frozen:
            self.freeze_timer -= dt
        if is_slown:
            self.slow_timer -=dt

        self.monsters = [monster for monster in self.monsters if not self._is_out(monster)]

        while len(self.monsters) < LIMITED_MONSTERS:
            angle = random.uniform(0, 2 * math.pi)
            x = CENTER[0] + RADIUS * math.cos(angle)
            y = CENTER[1] + RADIUS * math.sin(angle)
            pos = pygame.Vector2(x, y)

            direction = (pygame.Vector2(CENTER) - pos).normalize()
            speed = random.randint(MONSTER_MIN_SPEED, MONSTER_MAX_SPEED)

            monsters = {
                "pos": pos,
                "dir": direction,
                "speed": speed,
                "frames": random.choice(self.images),
                "frame_index": 0,
                "frame_timer": 0
            }

            self.monsters.append(monsters)

        if not is_frozen:
            for monsters in self.monsters:
                if is_slown:
                    speed_value = 0.3
                    monsters["pos"] += monsters["dir"] * monsters["speed"] * dt * speed_value
                else:
                    speed_value = 1.0
                    monsters["pos"] += monsters["dir"] * monsters["speed"] * dt * speed_value


    def draw(self, screen):
        for monster in self.monsters:
            monster["frame_timer"] += 1
            if monster["frame_timer"] >= self.frame_delay * 60:
                monster["frame_timer"] = 0
                monster["frame_index"] = (monster["frame_index"] + 1) % len(monster["frames"])

            image = monster["frames"][monster["frame_index"]]

            if monster["dir"].x < 0:
                image = pygame.transform.flip(image, True, False)

            screen.blit(image, image.get_rect(center=monster["pos"]))

    def check_collision(self, collider, shield_active=False):
        if shield_active:
            return False
        left, right, top, bottom = collider
        for monster in self.monsters:
            if left < monster["pos"].x < right and top < monster["pos"].y < bottom:
                return True
        return False

    def _is_out(self, monster):
        return monster["pos"].distance_to(CENTER) > RADIUS

    def clear_all(self):
        self.monsters = []
        self.respawn_delay = 1.0

    def freeze(self, seconds):
        self.freeze_timer = seconds
    def slow_down(self, seconds):
        self.slow_timer = seconds