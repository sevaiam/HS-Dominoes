# Write your code here
from random import choice
from random import randint
from random import shuffle


def full_domino_set():
    d_set = []
    for x in range(7):
        for y in range(x, 7):
            d_set.append([x, y])

    return d_set


def split_domino_set(i_set):
    set_1 = []
    set_2 = []
    s_snake = []
    s_status = -1
    for i in range(7):
        set_1.append(i_set.pop(randint(0, len(i_set) - 1)))
        set_2.append(i_set.pop(randint(0, len(i_set) - 1)))
    shuffle(i_set)
    for i in range(6, -1, -1):
        double = [i, i]
        if double in set_1:
            s_snake.append(set_1.pop(set_1.index(double)))
            s_status = 1
            break
        elif double in set_2:
            s_snake.append(set_2.pop(set_2.index(double)))
            s_status = 0
            break
        else:
            return False

    return [set_1, set_2, i_set, s_snake, s_status]


def print_field(i_set):
    print('=' * 70)
    print('Stock size: ', len(i_set[2]))
    print('Computer pieces: ', len(i_set[0]))
    print()

    if len(i_set[3]) <= 6:
        for i in i_set[3]:
            print(i, end='')
    else:
        for i in range(3):
            print(i_set[3][i], end='')
        print('...', end='')
        for i in range(-3, 0, 1):
            print(i_set[3][i], end='')

    print()
    print('Your pieces:')
    for n, p in enumerate(i_set[1]):
        print(f'{n+1}:{p}')
    print()
    if i_set[4] == 0:
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif i_set[4] == 1:
        print("Status: It's your turn to make a move. Enter your command.")


def check_game_over(i_set):
    if len(i_set[1]) == 0:
        print('Status: The game is over. You won!')
        return True
    elif len(i_set[0]) == 0:
        print('Status: The game is over. The computer won!')
        return True
    elif check_snake(i_set):
        print("Status: The game is over. It's a draw!")
        return True
    return False


def check_snake(i_set):
    snake = i_set[3]
    head = snake[-1][-1]
    snake_count = 0
    if snake[0][0] == head:
        for i in snake:
            if i[0] == head:
                snake_count += 1
            if i[1] == head:
                snake_count += 1
    return snake_count == 8


def play_domino(i_set, move, status):
    if move == 0 and len(i_set[2]) > 0:
        i_set[status].append(i_set[2].pop(randint(0, len(i_set[2]) - 1)))
    elif move == 0 and len(i_set[2]) == 0:
        pass
    elif move < 0:
        piece = i_set[status].pop(abs(move) - 1)
        if piece[1] != i_set[3][0][0]:
            piece.reverse()
        i_set[3].insert(0, piece)
    elif move > 0:
        piece = i_set[status].pop(abs(move) - 1)
        if piece[0] != i_set[3][-1][-1]:
            piece.reverse()
        i_set[3].append(piece)
    if status == 1:
        i_set[4] = 0
    elif status == 0:
        i_set[4] = 1
    return i_set


def check_input(i_set, move, status):
    try:
        move = int(move)
        if abs(move) <= len(i_set[status]):
            return check_move(i_set, move, status)
        else:
            print('Invalid input. Please try again.')
            return False
    except ValueError:
        print('Invalid input. Please try again.')
        return False
    return False


def check_move(i_set, move, status, print_error=True):
    head = i_set[3][-1][-1]
    tail = i_set[3][0][0]
    move = int(move)
    if move == 0:
        return True
    elif -move > 0:
        i_move = i_set[status][abs(move) - 1]
        if i_move[0] == tail or i_move[1] == tail:
            return True
        else:
            if print_error:
                print('Illegal move. Please try again. -1')
            return False
    elif move > 0:
        i_move = i_set[status][move - 1]
        if i_move[0] == head or i_move[1] == head:
            return True
        else:
            if print_error:
                print('Illegal move. Please try again. -2')
            return False

    return False


def domino_ai(i_set):
    i_comp = i_set[0]
    i_snake = i_set[3]
    head = i_snake[-1][-1]
    tail = i_snake[0][0]
    i_count = i_comp + i_snake
    i_dic = {}
    move_dic = {}
    for i in i_count:
        for x in i:
            i_dic.setdefault(x, 0)
            i_dic[x] += 1
    for i in range(len(i_comp)):
        rate = i_dic[i_comp[i][0]] + i_dic[i_comp[i][1]]
        move_dic.setdefault(i+1, rate)
    sorted_move_dic = {}
    for key in sorted(move_dic, key=move_dic.get, reverse=True):
        sorted_move_dic[key] = move_dic[key]
    for key in sorted_move_dic.keys():
        if check_move(i_set, key, 0, print_error=False):
            if i_comp[key - 1][0] == head or i_comp[key - 1][1] == head:
                return key
            elif i_comp[key - 1][0] == tail or i_comp[key - 1][1] == tail:
                return -key

    return 0




domino_game = split_domino_set(full_domino_set())
while not domino_game:
    domino_game = split_domino_set(full_domino_set())

# print('Stock pieces: ', d_stock)
# print('Computer pieces: ', d_computer)
# print('Player pieces: ', d_player)
# print('Domino snake: ', d_snake)
# print('Status: ', d_status)
print_field(domino_game)
while not check_game_over(domino_game):
    d_computer, d_player, d_stock, d_snake, d_status = domino_game

    if d_status == 1:
        player_move = input()
        while not check_input(domino_game, player_move, d_status):
            player_move = input()

        domino_game = play_domino(domino_game, int(player_move), d_status)
    elif d_status == 0:
        input()
        cpu_move = domino_ai(domino_game)
        while not (check_move(domino_game, cpu_move, d_status, print_error=False)):
            cpu_move = domino_ai(domino_game)
        # print('Cpu move: ', d_computer[abs(cpu_move) - 1])
        # print(cpu_move)
        domino_game = play_domino(domino_game, cpu_move, d_status)
    print_field(domino_game)

