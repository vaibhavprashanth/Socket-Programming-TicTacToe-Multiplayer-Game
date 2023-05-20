import socket
import threading


HOST = 'localhost'
PORT = 8000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))


class TicTacToe:
    def __init__(self):
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.current_player = 'X'
    
    def play_move(self, x, y):
        if self.board[x][y] == ' ':
            self.board[x][y] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_board(self):
        return self.board
    
    def get_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None


game = TicTacToe()


clients = []


def handle_client(client_socket, client_address):
    
    clients.append(client_socket)
    
    
    client_socket.sendall(str(game.get_board()).encode('utf-8'))
    
    while True:
        
        data = client_socket.recv(1024)
        
        try:
            x, y = map(int, data.decode('utf-8').split(','))
            game.play_move(x, y)
        except:
            pass
            
        
        winner = game.get_winner()
        if winner:
            
            message = f'{winner} wins'
            for c in clients:
                c.sendall(message.encode('utf-8'))
            break
        
        
        for c in clients:
            c.sendall(str(game.get_board()).encode('utf-8'))
            
        
        if not data:
            clients.remove(client_socket)
            client_socket.close()
            break
'''
def handle_client(client_socket, client_address):
    
    clients.append(client_socket)
    
    
    client_socket.sendall(str(game.get_board()).encode('utf-8'))
    
    last_move = None
    
    while True:
        
        data = client_socket.recv(1024)
        
        try:
            x, y = map(int, data.decode('utf-8').split(','))
            game.play_move(x, y)
            last_move = (x, y)
        except:
            pass
            
        
        winner = game.get_winner()
        if winner:
            message = f'{winner} wins'
            if last_move is not None:
                message += f' with last move ({last_move[0]}, {last_move[1]})'
            for c in clients:
                c.sendall(message.encode('utf-8'))
            break
        
        
        for c in clients:
            c.sendall(str(game.get_board()).encode('utf-8'))
            
        
        if not data:
            clients.remove(client_socket)
            client_socket.close()
            break
'''

print(f'Tic Tac Toe server started on {HOST}:{PORT}')

while True:
    
    server_socket.listen()
    
    
    client_socket, client_address = server_socket.accept()
    
    
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
