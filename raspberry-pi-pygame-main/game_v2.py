import pygame
import socket
import threading

from settings import *
from player import Player
from monsters import MonsterManger
from items import ItemManager

SERVER_IP = '10.125.126.208'
PORT = 9000
JOYSTICK_PORT = 5000
# 기존 게임용 소켓
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)
print(f"Server listening on {SERVER_IP}:{PORT}")
# 조이스틱 소켓
joystick_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
joystick_socket.bind((SERVER_IP, JOYSTICK_PORT))
joystick_socket.listen(1)
print(f"Joystick server listening on {SERVER_IP}:{JOYSTICK_PORT}")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
textFont = pygame.font.SysFont(None, 50)

player = Player("assets/Swim.png", "assets/Swim2.png")
monsters = MonsterManger()
items = ItemManager()
bg_image = pygame.image.load("assets/background.png")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

running = True
game_state = 1
score = 0
start_time = pygame.time.get_ticks()

# 조이스틱 값 저장용 전역 변수
joystick_updown = None
joystick_leftright = None

# 센서 메시지 클라이언트 연결 수락
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")
# 조이스틱 클라이언트 연결 수락
joystick_client_socket, joystick_client_address = joystick_socket.accept()
print(f"Joystick connected from {joystick_client_address}")

"""client_socket = None
joystick_client_socket = None
client_connected = threading.Event() # 이벤트 클라이언트 연결을 확인하기 위한 플래그
joystick_connected = threading.Event() # 조이스틱 클라이언트 연결을 확인하기 위한 플래그

def accept_event_client():
    global client_socket
    conn, addr = server_socket.accept()
    client_socket = conn
    print(f"Connected to event client: {addr}")
    client_connected.set() # 연결되었음을 알림
    handle_client_message() # 연결되면 메시지 처리 시작

def accept_joystick_client():
    global joystick_client_socket
    conn, addr = joystick_socket.accept()
    joystick_client_socket = conn
    print(f"Connected to joystick client: {addr}")
    joystick_connected.set() # 연결되었음을 알림
    handle_joystick_message() # 연결되면 메시지 처리 시작

# 클라이언트 연결 수락 스레드 시작
threading.Thread(target=accept_event_client, daemon=True).start()
threading.Thread(target=accept_joystick_client, daemon=True).start()

# 모든 클라이언트가 연결될 때까지 기다립니다.
print("Waiting for all clients to connect...")
client_connected.wait()
joystick_connected.wait()
print("All clients connected. Starting game loop.")"""


def handle_client_message():
    global running
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
    global game_state, items, player
    used_item = items.use_item(message)

    if used_item == "button":
        print("press_detected: Freeze obstacle")
        monsters.freeze(2)
    elif used_item == "sound":
        monsters.slow_down(2.0)
    elif used_item == "light":
        print("dark_detected: Shield")
        player.activate_shield(3.0)
    elif used_item == "shock":
        print("shock_detected: Destroy obstacle (Clear All)")
        monsters.clear_all()

def handle_joystick_message():
    global running, joystick_updown, joystick_leftright
    while running:
        try:
            message = joystick_client_socket.recv(1024).decode('utf-8')
            if message:
                value1_str, value2_str = message.strip().split(',')
                joystick_updown = int(value1_str)
                joystick_leftright = int(value2_str)
                # print(f"Joystick data received: {joystick_updown}, {joystick_leftright}")
        except Exception as e:
            print(f"Error receiving joystick data: {e}")
            break

# 메시지 수신을 위한 스레드 실행
threading.Thread(target=handle_client_message, daemon=True).start()
threading.Thread(target=handle_joystick_message, daemon=True).start()

while running:
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            used_item = items.use_item(event.key)
            if used_item == "button":
                monsters.freeze(2)
            elif used_item == "sound":
                monsters.slow_down(2.0)
            elif used_item == "light":
                player.activate_shield(3.0)
            elif used_item == "shock" :
                monsters.clear_all()


    keys = pygame.key.get_pressed()

    if game_state == 0:
        startText = textFont.render("PRESS K TO START", True, (255, 255, 255))
        text_rect = startText.get_rect(center=(CENTER[0],CENTER[1]))
        screen.blit(startText, text_rect)

        if keys[pygame.K_k]:
            game_state = 1
            start_ticks = pygame.time.get_ticks()

    elif game_state == 1:
        score = int((pygame.time.get_ticks() - start_time) / 1000)

        # 화살 그리기
        monsters.update(clock.get_time() / 1000)
        monsters.draw(screen)

        # 아이템 그리기
        items.update(clock.get_time() / 1000)
        items.draw(screen)

        # 가지고 있는 아이템 그리기
        items.draw_collection(screen)

        # 수정: 조이스틱 값 같이 넘김
        player.move(clock.get_time() / 1000, keys=keys, joystick_updown=joystick_updown, joystick_leftright=joystick_leftright)
        player.draw(screen)

        # 맵 그리기
        pygame.draw.circle(screen, (0, 0, 0), (int(CENTER[0]), int(CENTER[1])), int(RADIUS), 2)

        # 충돌 검사 시 쉴드 반영
        if monsters.check_collision(player.get_collider(), shield_active=(player.shield_timer > 0)):
            print("닿음")
            # game_state = 2
        if items.check_collision(player.get_collider()):
            print("아이템 먹음")

        # 점수 그리기
        startText = textFont.render(str(score), True, (0, 0, 0))
        text_rect = startText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(startText, text_rect)

    elif game_state == 2:
        endText = textFont.render(f"GAME OVER SCORE: {score} press K to restart", True, (255, 255, 255))
        text_rect = endText.get_rect(center=(CENTER[0], CENTER[1]))
        screen.blit(endText, text_rect)

    else:
        pass

    # 다시 그리기
    pygame.display.flip()
    clock.tick(60)

# 소켓 연결 종료
client_socket.close()
server_socket.close()
joystick_client_socket.close()
joystick_socket.close()
pygame.quit()