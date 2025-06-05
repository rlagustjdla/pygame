# Example file showing a circle moving on screen
import pygame
import random

# import smbus
import time

pygame.init()

size = width, height = 640, 640
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

dt = 0
running = True
player_size = 50
player_speed = 200
arrow_size = 20
arrow_max_speed = 300
arrow_min_speed = 100
limited_arrows = 8 #화살 개수 제한
arrow_list = []




address = 0x48
A0 = 0x40
A1 = 0x41
# bus = smbus.SMBus(1)


# 중앙에서 시작하는 플레이어
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# 이미지 불러오기
arrow_image = pygame.image.load("assets/pearl.png").convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (arrow_size, arrow_size))

player_image = pygame.image.load("assets/dave_front.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# 폰트 설정하기
textFont = pygame.font.SysFont(None, 50)

# 게임 상태
game_state = 1

# 게임 점수
score = 0
# 시작 시간
start_ticks = 0
# 경과 시간
elapesed_time=0

while running:
    # 종료 조건
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 배경 색
    screen.fill("#ffe8f2")

    if game_state == 0:
        startText = textFont.render("PRESS K TO START", True, (255, 255, 255))
        text_rect = startText.get_rect(center=(width/2, height/2))
        screen.blit(startText, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_k]:
           game_state = 1
           start_ticks = pygame.time.get_ticks()

    elif game_state == 1:
        # 경과 시간 계산
        elapesed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        # 점수 계산
        score = int(elapesed_time)

        # ========
        # 화살 그리기
        arrow_list = [arrow for arrow in arrow_list if not (
                (arrow[2] == 0 and arrow[0].y > height) or
                (arrow[2] == 1 and arrow[0].x < 0) or
                (arrow[2] == 2 and arrow[0].y < 0) or
                (arrow[2] == 3 and arrow[0].x > width)
        )]

        # 10개 이하라면 또 추가
        while len(arrow_list) < limited_arrows:
            # 랜덤한 위치 속도, 시작 위치(북, 동, 남, 서)를 arrow 리스트에 넣는다.
            direction = random.randint(0, 3)
            # 북쪽에서 날아오는 화살
            if direction == 0:
                arrowX = random.randrange(0, width)
                speed = random.randrange(arrow_min_speed, arrow_max_speed)
                arrow_list.append([pygame.Vector2(arrowX, 0), speed, direction])
            # 동쪽에서 날아오는 화살
            elif direction == 1:
                arrowY = random.randrange(0, height)
                speed = random.randrange(arrow_min_speed, arrow_max_speed)
                arrow_list.append([pygame.Vector2(width, arrowY), speed, direction])
            # 남쪽에서 날아오는 화살
            elif direction == 2:
                arrowX = random.randrange(0, width)
                speed = random.randrange(arrow_min_speed, arrow_max_speed)
                arrow_list.append([pygame.Vector2(arrowX, height), speed, direction])
            # 서쪽에서 날아오는 화살
            else:
                arrowY = random.randrange(0, height)
                speed = random.randrange(arrow_min_speed, arrow_max_speed)
                arrow_list.append([pygame.Vector2(0, arrowY), speed, direction])

        # 화살 그리기 및 이동
        for arrow in arrow_list:
            screen.blit(arrow_image, arrow[0])
            if arrow[2] == 0:
                arrow[0].y += arrow[1] * dt
            elif arrow[2] == 1:
                arrow[0].x -= arrow[1] * dt
            elif arrow[2] == 2:
                arrow[0].y -= arrow[1] * dt
            else:
                arrow[0].x += arrow[1] * dt
        # ========

        # 플레이어 그리기
        # screen.blit(player_image, player_pos)

        # keyboard moving
        keys = pygame.key.get_pressed()
        # 중심 좌표와 반지름
        center = pygame.Vector2(width / 2, height / 2)
        radius = width / 2 - 20

        # 이동 처리
        move_delta = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move_delta.y -= 300 * dt
        if keys[pygame.K_s]:
            move_delta.y += 300 * dt
        if keys[pygame.K_a]:
            move_delta.x -= 300 * dt
        if keys[pygame.K_d]:
            move_delta.x += 300 * dt

        new_pos = player_pos + move_delta

        # 중심 기준 거리 체크
        if new_pos.distance_to(center) <= radius:
            player_pos = new_pos

        # 디버그 원
        pygame.draw.circle(screen, (200, 200, 200), (int(center.x), int(center.y)), int(radius), 2)

        # 화면에 플레이어 이미지 그릴 때 중심 기준으로 보정
        draw_pos = player_pos - pygame.Vector2(player_size / 2, player_size / 2)
        screen.blit(player_image, draw_pos)
        print(player_pos.distance_to(center))

        """
        # joystcik moving
        bus.write_byte(address, A0)
        time.sleep(0.01)
        value1 = bus.read_byte(address)

        bus.write_byte(address, A1)
        time.sleep(0.01)
        value2 = bus.read_byte(address)

        print(value1, value2)
        # down
        if value1 < 100 and player_pos.x > (0 - player_size / 2):
            print("left")
            player_pos.x -= player_speed * dt
        if value1 > 220 and player_pos.x < (width - player_size / 2):
            print("right")
            player_pos.x += player_speed * dt
        if value2 < 100 and player_pos.y > (0 - player_size / 2):
            print("up")
            player_pos.y -= player_speed * dt
        if value2 > 220 and player_pos.y < (height - player_size / 2):
            print("down")
            player_pos.y += player_speed * dt
    """


        # ========
        # 닿았는지 검사
        # 플레이어 콜라이더 값
        left_value = player_pos.x - player_size / 2
        right_value = player_pos.x + player_size / 2
        top_value = player_pos.y - player_size / 2
        bottom_value = player_pos.y + player_size / 2

        for arrow in arrow_list:
            # 화살의 좌표가 플레이어 콜라이더 안에 들어왔으면
            if left_value < arrow[0].x < right_value and top_value < arrow[0].y < bottom_value:
                print("닿음")
                #game_state = 2

        # ========
        scoreText = textFont.render(str(score), True, (255, 255, 255))
        text_rect = scoreText.get_rect(center=(width / 2, height / 2))
        screen.blit(scoreText, text_rect)

    elif game_state == 2:
        stopText = textFont.render(f"GAME OVER SCORE: {score} press K to restart", True, (255, 255, 255))
        text_rect = stopText.get_rect(center=(width / 2, height / 2))
        screen.blit(stopText, text_rect)
        keys = pygame.key.get_pressed()
    else:
        pass


    # 프레임 속도
    dt = clock.tick(60) / 1000
    # 다시 그리기
    pygame.display.flip()

pygame.quit()
