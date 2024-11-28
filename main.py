import socket
import threading
import pygame as pg
import json

APP_PORT = 8080
VERYFICATION_HEADER = b"CCLOCALMULTIPLAYER"

controls = {}

players = {}

def start_control_listener():
    def get_controls():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind(("", APP_PORT))  # Listening on all interfaces

            data, address = server_socket.recvfrom(1024)
            print(f"Received message from {address}: {data}")
            if data.startswith(VERYFICATION_HEADER):  # Verify that message is sent by this application
                global controls
                controls[address[0]] = json.loads(data[len(VERYFICATION_HEADER):].decode('utf-8'))

    global running
    while running:
        get_controls()

if __name__ == '__main__':

    own_ip = socket.gethostbyname(socket.gethostname())

    # pygame setup
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    running = True

    control_listener = threading.Thread(target=start_control_listener)
    control_listener.start()

    message = {
        'position': [0, 0],
        'w': False,
        'a': False,
        's': False,
        'd': False,
        'esc': False,
    }

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                message['esc'] = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    message['w'] = True
                elif event.key == pg.K_a:
                    message['a'] = True
                elif event.key == pg.K_s:
                    message['s'] = True
                elif event.key == pg.K_d:
                    message['d'] = True
                elif event.key == pg.K_ESCAPE:
                    message['esc'] = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    message['w'] = False
                elif event.key == pg.K_a:
                    message['a'] = False
                elif event.key == pg.K_s:
                    message['s'] = False
                elif event.key == pg.K_d:
                    message['d'] = False
                elif event.key == pg.K_ESCAPE:
                    message['esc'] = False

        message['position'] = players[own_ip] if own_ip in players else [0, 0]
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(VERYFICATION_HEADER + json.dumps(message).encode('utf-8'), ("255.255.255.255", APP_PORT))  # Broadcast message on APP_PORT

        print(controls, players)

        to_delete = []
        if controls:
            for ip in controls:
                if ip not in players:
                    players[ip] = controls[ip]['position']
                    print(f"New player: {ip}")
                else:
                    control = controls[ip]
                    if control['esc']:
                        if ip == own_ip:
                            running = False
                        else:
                            to_delete.append(ip)
                    if control['w']:
                        players[ip][1] -= 1
                    if control['a']:
                        players[ip][0] -= 1
                    if control['s']:
                        players[ip][1] += 1
                    if control['d']:
                        players[ip][0] += 1
        
        for ip in to_delete:
            players.pop(ip)
        
        controls.clear()

        screen.fill((0, 0, 0))

        for player in players:
            pg.draw.circle(screen, (255, 255, 255), (players[player][0] + screen.get_width() // 2, players[player][1] + screen.get_height() // 2), 10)
        
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60

    pg.quit()