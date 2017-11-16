import socket
import threading
import random
import struct
import sys
import time

INT = 4
INF = 2 ** 30
random.seed()
referee_number = random.randint(0,1001)

lock = threading.Lock()
winner_player = None
timeout = threading.Event()
timeout.clear()
winner_elected = threading.Event()
winner_elected.clear()
players = []
player_count = 0
min_difference = INF

def set_timeout():
	global timeout
	timeout.set()

timer = threading.Timer(5, set_timeout)

def player_behaviour(player_socket):
	global lock, player_count, winner_player, timeout, min_difference, winner_elected

	myself = player_count
	print('Player #{} from {}'.format(myself, player_socket.getpeername()))

	greeting = 'Player #{}\n'.format(myself)
	player_socket.sendall(bytes(greeting))

	player_number = player_socket.recv(INT)
	player_number = struct.unpack('!I', player_number)[0]

	timeout.wait()
	lock.acquire()
	if (abs(player_number - referee_number) < min_difference):
		min_difference = abs(player_number - referee_number)
		winner_player = myself

	player_count-=1
	if (player_count == 0):
		winner_elected.set()
	lock.release()

	winner_elected.wait()

	if (myself == winner_player):
		print('Winner player: #{}\n'.format(winner_player))
		player_socket.sendall(bytes('You won! with a diff of: {}\n'.format(min_difference)))
	else:
		player_socket.sendall(bytes('You lost. with a diff of: {}\n'.format(abs(player_number - referee_number))))

	player_socket.close

def reset_game():
	global lock, players, winner_player, player_count, referee_number, timeout, min_difference, winner_elected
	while True:
		print('-' * 40)
		timeout.wait()
		for player in players:
			player.join()

		timeout.clear()
		lock.acquire()

		players = []
		player_count = 0

		winner_elected.clear()
		winner_player = None

		referee_number = random.randint(0,1001)
		min_difference = INF
		print('They have to guess this: ', referee_number)
		lock.release()


if __name__=='__main__':
	try:
		rs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rs.bind( ('0.0.0.0',8090) )
		rs.listen(5)
	except socket.error as msg:
		print(msg.strerror)
		exit(-1)

	print(socket.gethostname())
	print('They have to guess this: ' + str(referee_number))

	referee = threading.Thread(target=reset_game)
	referee.start()

	while True:
		player_socket, addrc = rs.accept()
		player = threading.Thread(target=player_behaviour, args=(player_socket,) )
		players.append(player)
		player_count+=1
		player.start()
		timer.cancel()
		timer = threading.Timer(5, set_timeout)
		timer.start()
