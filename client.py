import pygame
import socket
import threading

HOST = 'localhost'
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

pygame.init()

# set up the display window
WINDOW_SIZE = (300, 300)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic Tac Toe")

# set up the fonts
FONT_SIZE = 50
font = pygame.font.Font(None, FONT_SIZE)
t=0
# set up the board
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

# define the function to draw the board
'''
def draw_board():
    # Clear the screen
    screen.fill((255, 255, 255))
    
    # Draw the horizontal lines
    pygame.draw.line(screen, (0, 0, 0), (0, 100), (300, 100), 2)
    pygame.draw.line(screen, (0, 0, 0), (0, 200), (300, 200), 2)
    
    # Draw the vertical lines
    pygame.draw.line(screen, (0, 0, 0), (100, 0), (100, 300), 2)
    pygame.draw.line(screen, (0, 0, 0), (200, 0), (200, 300), 2)
    
    # Draw the X's and O's
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(j*100, i*100, 100, 100)
            text_surface = font.render(board[i][j], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
    
    # Update the display
    pygame.display.flip()
# draw the initial board
'''
def draw_board(last_move=None):
    # Clear the screen
    screen.fill((255, 255, 255))
    
    # Draw the horizontal lines
    pygame.draw.line(screen, (0, 0, 0), (0, 100), (300, 100), 2)
    pygame.draw.line(screen, (0, 0, 0), (0, 200), (300, 200), 2)
    
    # Draw the vertical lines
    pygame.draw.line(screen, (0, 0, 0), (100, 0), (100, 300), 2)
    pygame.draw.line(screen, (0, 0, 0), (200, 0), (200, 300), 2)
    
    # Draw the X's and O's
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(j*100, i*100, 100, 100)
            if (i, j) == last_move:
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)
            text_surface = font.render(board[i][j], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
    
    # Update the display
    pygame.display.flip()

draw_board()

# define the function to handle a move
'''
def make_move(x, y):
    client_socket.sendall(f'{x},{y}'.encode('utf-8'))
'''
def make_move(x, y):
    global board
    global t
    if t==0:
        board[x][y] = 'X'
    else:
        board[x][y] = 'O'
    t=(t+1)%2
    client_socket.sendall(f'{x},{y}'.encode('utf-8'))



def receive_data():
    global board
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        if 'draw' in message: 
            print(message)
        if 'wins' in message:
            
            draw_board()
            print(message)
            draw_board()
            pygame.quit()
            break
        else:
            board = eval(message)
            draw_board()

# start the thread for receiving data
threading.Thread(target=receive_data).start()

# run the game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            client_socket.close()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x = pos[1] // 100
            y = pos[0] // 100
            if board[x][y] == ' ':
                make_move(x, y)

    pygame.display.update()
"""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    data = client_socket.recv(1024)
    message = data.decode('utf-8')
    if 'wins' in message:
        print(message)
        running = False
    else:
        board = eval(message)
        draw_board()

    if not running:
        client_socket.close()
        pygame.quit()
"""