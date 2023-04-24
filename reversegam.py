# "Реверси: клон "Отелло"
import random
import sys

WIDTH = 8  # Ширина игрового поля
HEIGHT = 8  # Высота игрового поля


def draw_board(board):
    # Функция выводит игровое поле и ничего не возвращает
    print(' ' * 2 + '1 2 3 4 5 6 7 8')
    # print(' ' + ' - - - - - - - -')
    for y in range(HEIGHT):
        print(f'{y + 1}|', end='')
        for x in range(WIDTH):
            print(board[x][y], end='|')
        print(f'{y + 1}')


        '''# Рисуем горизонтальные разделители клеток
        print(' ', end='')
        for i in range(WIDTH):
            print('+-', end='')
        print('+')'''

    print(' ' * 2 + '1 2 3 4 5 6 7 8')
    '''Поработать над вариантами игрового поля'''


def get_new_board():
    # Функция создает новую структуру данных чистого игрового поля
    board = []
    for i in range(WIDTH):
        board.append([' '] * HEIGHT)
    return board


def is_valid_move(board, tile, x_start, y_start):
    # Возвращает False, если ход игрока в клетку xstart и ystart недопустим
    # Если ход допустим, то возвращает список клеток, которые бы игрок
    # забрал себе, сделав этот ход
    if board[x_start][y_start] != ' ' or is_not_on_board(x_start, y_start):
        return False

    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'

    tile_to_flip = []
    # Определяем направления поиска захваченных фишек (8 направлений)
    directions_list = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1],
                       [-1, 0], [-1, 1]]
    for x_direction, y_direction in directions_list:
        x, y = x_start, y_start
        # Делаем ход в выбранном направлении
        x += x_direction  # Первый шаг в направлении x
        y += y_direction  # Первый шаг в направлении y

        while is_on_board(x, y) and board[x][y] == other_tile:
            # Продолжаем двигаться в этом направлении x и y
            x += x_direction
            y += y_direction
            if is_on_board(x, y) and board[x][y] == tile:

                # Если есть фишки, которые можно перевернуть. Двигаемся в
                # обратном направлении до достижения исходной клетки,
                # отмечая все фишки на этом пути
                while True:
                    x -= x_direction
                    y -= y_direction
                    if x == x_start and y == y_start:
                        break
                    tile_to_flip.append([x, y])

    if len(tile_to_flip) == 0:
        # Если ни одна из фишек не перевернулась, то это недопустимый ход
        return False

    return tile_to_flip


def is_on_board(x, y):
    # Возвращает True, если координаты есть на игровом поле
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


def is_not_on_board(x, y):
    # Возвращает False, если координаты есть на игровом поле
    return not is_on_board(x, y)


def get_board_with_valid_moves(board, tile):
    # Возвращает новое поле с точками, обозначающими допустимые ходы,
    # которые может сделать игок
    board_copy = get_board_copy(board)

    for x, y in get_valid_moves(board_copy, tile):
        board_copy[x][y] = '.'
    return board_copy


def get_valid_moves(board, tile):
    # Возвращает список списков с координатами x и y допустимых ходов для
    # данного игрока на данном игровом поле
    valid_moves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if is_valid_move(board, tile, x, y):
                valid_moves.append([x, y])

    return valid_moves


def get_score_of_board(board):
    # Определяет очки игроков, подсчитав фишки. Возвращает словарь с
    # ключами 'O' и 'X'
    x_score = 0
    o_score = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                x_score += 1
            elif board[x][y] == 'O':
                o_score += 1

    return {'X': x_score, 'O': o_score}


def enter_player_tile():
    # Даем игроку выбрать тип игровой фишки
    # Возвращает список с фишкой игрока в качестве первого элемента
    # и фишкой компьютера в качестве второго
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        # print('Вы хотите играть за X или O?')
        tile = input('Вы хотите играть за X или O: ').upper()

    # Первый элемент в списке фишка игрока, второй фишка компьютера
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def who_goes_first():
    # Случайно выбирает, кто ходит первым
    turn = random.randint(0, 1)
    if turn == 0:
        return 'ИИ'
    else:
        return 'Человек'


def make_move(board, tile, xstart, ystart):
    # Помещает фишку на игровое поле в позицию xstart и ystart и
    # и переворачивает какую-либо фишку противника
    # Возвращает False, если ход недопустим. Или True, если допустим
    tile_to_flip = is_valid_move(board, tile, xstart, ystart)

    if not tile_to_flip:
        return False

    board[xstart][ystart] = tile

    for x, y in tile_to_flip:
        board[x][y] = tile

    return True


def get_board_copy(board):
    # Делает копию игрового поля
    board_copy = get_new_board()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            board_copy[x][y] = board[x][y]

    return board_copy


def is_in_corner(x, y):
    # Возвращает True, если указанная позиция находится в одном из
    # четырех углов
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)


def get_player_move(board, player_tile):
    # Позволяет игроку сделать ход
    # Возвращает ход в виде [x, y] (или вернуть строки 'подсказка' или 'выход')
    digits_1_to_8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Укажите ход, текст "выход" для завершения игры или "подсказка"',
              ' для вывода подсказки')
        move = input().lower()
        if move == 'выход' or move == 'подсказка':
            return move

        if len(move) == 2 and move[0] in digits_1_to_8 and move[1] in digits_1_to_8:
            # Игрок вводит сначала ряд, потом столбец, поэтому в x кладем второй
            # элемент списка, а в y первый
            x = int(move[1]) - 1
            y = int(move[0]) - 1

            if not is_valid_move(board, player_tile, x, y):
                print('Такой ход закрыт, введите другой.')
                continue
            else:
                break
        else:
            print('Это недопустимый ход. Введите номер ряда (1-8) '
                  'и номер столбца (1-8) без пробела.')
            print('Например 81')

    return [x, y]


def get_computer_move(board, computer_tile):
    # Учитывая данное игровое поле и данную фишку компьютера, определяет, куда
    # сделать ход, и возвращает этот ход в виде списка [x, y].
    possible_moves = get_valid_moves(board, computer_tile)
    random.shuffle(possible_moves) # Делаем случайный порядок ходов

    # Всегда делать ход в угол, если это возможно
    for x, y in possible_moves:
        if is_in_corner(x, y):
            return [x, y]

    # Найти ход с наибольшим возможным количеством очков.
    best_score = -1
    for x, y in possible_moves:
        board_copy = get_board_copy(board)
        make_move(board_copy, computer_tile, x, y)
        score = get_score_of_board(board_copy)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score

    return best_move


def print_score(board, playet_tile, computer_tile):
    scores = get_score_of_board(board)
    print(f'Ваш счет: {scores[playet_tile]}.'
          f' Счет компьютера: {scores[computer_tile]}')


def play_game(player_tile, computer_tile):
    show_hints = False
    turn = who_goes_first()
    print(f'{turn} ходит первым')

    # Очистить игровое поле и выставить стартовые фишки
    board = get_new_board()
    board[3][3] = 'X'
    board[4][4] = 'X'
    board[4][3] = 'O'
    board[3][4] = 'O'

    while True:
        player_valid_moves = get_valid_moves(board, player_tile)
        computer_valid_moves = get_valid_moves(board, computer_tile)

        if len(player_valid_moves) == 0 and len(computer_valid_moves) == 0:
            return board # Ходоов не у кого нет, заканчиваем игру

        elif turn == 'Человек':
            if len(player_valid_moves) != 0:
                if show_hints:
                    valid_moves_board = get_board_with_valid_moves(board, player_tile)
                    draw_board(valid_moves_board)
                else:
                    draw_board(board)
                print_score(board, player_tile, computer_tile)

                move = get_player_move(board, player_tile)
                if move == 'выход':
                    # Чтобы консоль сразу не закрылась используем input()
                    input('Красава, что сыграл')
                    sys.exit()
                elif move == 'подсказка':
                    show_hints = not show_hints
                    continue
                else:
                    make_move(board, player_tile, move[0], move[1])

            turn = 'ИИ'

        elif turn == 'ИИ':
            if len(computer_valid_moves) != 0:
                draw_board(board)
                print_score(board, player_tile, computer_tile)

                input('Нажмите Enter для просмотра хода компьютера...')
                move = get_computer_move(board, computer_tile)
                make_move(board, computer_tile, move[0], move[1])

            turn = 'Человек'


print('Здравия желаю,теперь ты в игре "Реверси"!')

player_tile, computer_tile = enter_player_tile()

while True:
    final_board = play_game(player_tile, computer_tile)

    # Отображаем итоговый счет
    draw_board(final_board)
    scores = get_score_of_board(final_board)
    print(f'X набрал {scores["X"]} очков. O набрал {scores["O"]} очков.')

    if scores[player_tile] > scores[computer_tile]:
        print(f'Вы победили ИИ, обогнав его на {scores[player_tile] - scores[computer_tile]} очков! Троекратное вам УРА')
    elif scores[player_tile] < scores[computer_tile]:
        print(f'Вы проиграли. Увы, ИИ обогнал вас на {scores[computer_tile] - scores[player_tile]}')
    else:
        print('Вот это да! У вас ничья.')

    print('Хотите сыграть ещ раз? (да или нет)')
    if not input().lower().startswith('д'):
        break
