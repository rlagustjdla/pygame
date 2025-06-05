import socket
import pygame
import threading
from settings import *
from player import Player
from arrows import ArrowManager
from items import ItemManager

SERVER_IP = '10.125.126.208'
PORT = 9000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_IP}:{PORT}")

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
textFont = pygame.font.SysFont(None, 50)

player = Player(r"C:\Users\user\Desktop\raspberry-pi-pygame-main\raspberry-pi-pygame-main\assets\dave_front.png")
arrows = ArrowManager(r"C:\Users\user\Desktop\raspberry-pi-pygame-main\raspberry-pi-pygame-main\assets\pearl.png")
items = ItemManager(arrows, player)

running = True
game_state = 1
score = 0
start_time = pygame.time.get_ticks()

# 서버 연결 수락
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

# 클라이언트로부터 메시지를 받는 함수
def handle_client_message():
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                handle_message(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def handle_message(message):
    global game_state, items, arrows, player
    if message == "shock_detected":
        print("Item 2 activated: Destroy obstacle (Clear All)")
        # 아이템 2 효과: 장애물 파괴
        items.use_item(2)  # 메시지를 받으면 아이템 2 사용
    elif message == "press_detected":
        print("Item 1 activated: Freeze obstacle")
        # 아이템 1 효과: 장애물 정지
        items.use_item(1)  # 메시지를 받으면 아이템 1 사용
    elif message == "dark_detected":
        print("Item 3 activated: Shield")
        # 아이템 3 효과: 플레이어에게 쉴드 부여
        items.use_item(3)  # 메시지를 받으면 아이템 3 사용

# 메시지 수신을 위한 스레드 실행
threading.Thread(target=handle_client_message, daemon=True).start()

# 게임 루프
while running:
    screen.fill("#ffffff")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == 0:
        startText = textFont.render("PRESS K TO START", True, (255, 255, 255))
        text_rect = startText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(startText, text_rect)

        if keys[pygame.K_k]:
            game_state = 1
            start_ticks = pygame.time.get_ticks()

    elif game_state == 1:
        score = int((pygame.time.get_ticks() - start_time) / 1000)

        # 화살 그리기
        arrows.update(clock.get_time() / 1000)
        arrows.draw(screen)

        # 아이템 그리기
        items.update(clock.get_time() / 1000)
        items.draw(screen)

        # 가지고 있는 아이템 그리기
        items.draw_collection(screen)

        # 플레이어 그리기
        player.move(keys, clock.get_time() / 1000)
        player.draw(screen)

        # 맵 그리기
        pygame.draw.circle(screen, (0, 0, 0), (int(CENTER[0]), int(CENTER[1])), int(RADIUS), 2)

        # 충돌 검사 시 쉴드 반영
        if arrows.check_collision(player.get_collider(), shield_active=(player.shield_timer > 0)):
            print("Collision detected")

        if items.check_collision(player.get_collider()):
            print("Item collected")

        # 점수 그리기
        startText = textFont.render(str(score), True, (0, 0, 0))
        text_rect = startText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(startText, text_rect)

    elif game_state == 2:
        endText = textFont.render(f"GAME OVER SCORE: {score} press K to restart", True, (255, 255, 255))
        text_rect = endText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(endText, text_rect)

    pygame.display.flip()
    clock.tick(60)

# 소켓 연결 종료
client_socket.close()
server_socket.close()
pygame.quit()
