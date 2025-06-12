import socket
import threading

updown_value = 0
LR_value = 0

def handle_client(conn):
    global updown_value, LR_value
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                # 데이터는 "value1,value2" 형식으로 온다고 가정
                decoded = data.decode().strip()
                value1_str, value2_str = decoded.split(',')
                updown_value = int(value1_str)
                LR_value = int(value2_str)
                print("Received:", updown_value, LR_value)
            except Exception as e:
                print("Error:", e)
                break

def run_server():
    host = '0.0.0.0'
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Socket server running on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

# 서버 스레드 시작
threading.Thread(target=run_server, daemon=True).start()
