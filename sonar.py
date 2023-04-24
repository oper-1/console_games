# Охотник за сокровищами

import random
import sys
import math


def getNewBoard():
    # Создает структуру данных нового игрового поля размером 60х15
    board = []
    for x in range(60):
        board.append([])
        for y in range(15):
            # Для создания океана используем разные символы, чтобы сделать
            # его реалистичнее
            if random.randint(0, 1) == 0:
                board[x].append('~')
            else:
                board[x].append('`')

    return board


def drawBoard(board):
    # Создаем строку нумерации столбцов
    columnsNum = '0 1 2 3 4 5 6 7 8 9 '

    # Отображает структуру данных игрового поля
    tensDigitsLine = ' ' * 4  # Создаем место для чисел вниз по левой строке
    for i in range(1, 6):
        tensDigitsLine += (' ' * (len(columnsNum) - 1)) + str(i)

    # Выводим числа в верхней части поля
    print(tensDigitsLine)
    print((' ' * 3) + (columnsNum * 6))
    # print()

    # Выводим 15 рядов поля
    for row in range(15):
        # К однозначным числам нужно добавить дополнительный пробел
        if row < 10:
            extraSpace = ' '
        else:
            extraSpace = ''

        # Создаем строку для этого ряда в игровом поле
        boardRow = ''
        for column in range(60):
            boardRow += board[column][row] + ' '

        print(f'{extraSpace}{row} {boardRow}{row}')

    # Выводим числа в нижней части поля
    # print()
    print((' ' * 3) + (columnsNum * 6))
    print(tensDigitsLine)


def getRandomChests(numChests):
    # Создает список структур данных сундука
    # (двухэлементные списки целочисленных x и y)
    chests = []
    while len(chests) < numChests:
        newChest = [random.randint(0, 59), random.randint(0, 14)]
        # Убедимся, что сундука здесь еще нет.
        if newChest not in chests:
            chests.append(newChest)

    return chests


def isOnBoard(x, y):
    # Возвращает True, если координаты есть на поле, в противном случае
    # возвращает False
    return x >= 0 and x <= 59 and y >= 0 and y <= 14


def makeMove(board, chests, x, y):
    # Изменяем структуру данных поля, используя символ гидролокатора. Удаляем
    # сундуки с сокровищами из списка с сундуками, как только их нашли.

    # Все сундуки будут расположены ближе, чем на расстоянии 100 единиц
    smallestDistance = 100
    for cx, cy in chests:
        distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))
        # Нам нужен ближайший сундук с сокровищами
        if distance < smallestDistance:
            smallestDistance = distance

        smallestDistance = round(smallestDistance)

    if smallestDistance == 0:
        # Координаты xy попали прямо в сундук с сокровищами!
        chests.remove([x, y])
        return 'Вы нашли сундук с сокровищами на затонувшем судне!'
    else:
        if smallestDistance < 10:
            board[x][y] = str(smallestDistance)
            return f'Сундук с сокровищами обнаружен на расстоянии {smallestDistance} от гидролокатора.'
        else:
            board[x][y] = 'X'
            return 'Гидролокатор ничего не обнаружил. Все сундуки с сокровищами вне пределов досягаемости'


def enterPlayerMove(previousMoves):
    # Позволяет игроку сделть ход. Проверяет допустимость хода. Вернуть двухэлементный список с целыми координатми x и y
    print('Где следует опустить гидролокатор? (координаты 0-59 0-14)')
    print('(или введите "вых" для выхода из игры)')

    while True:
        move = input()
        if move.lower() == 'вых':
            print('Спасибо за игру')
            sys.exit()

        move = move.split()
        if len(move) == 2 and move[0].isdigit() and move[
            1].isdigit() and isOnBoard(int(move[0]), int(move[1])):
            if [int(move[0]), int(move[1])] in previousMoves:
                print('Здесь вы уже опускали гидролокатор')
                continue
            # return [int(move[0]), int(move[1])]
            return int(move[0]), int(move[1])

        print(
            'Введите число от 0 до 59, потом пробел, а затем число от 0 до 14.')


def showInstructions():
    print('''Инструктаж:
Вы - капитан корабля, плывущего за сокровищами. Ваша задача - с помощью
гидролокаторов найти три сундука с сокровищами в затонувших судах на дне океана.
Но гидролокаторы очень просты и определяют только расстояние, но не направление.
Введите координаты, чтобы опустить гидролокатор в воду. На карте будет показано
число, обозначающее, на каком расстоянии находится ближайший сундук. Или будет
показана буква Х, обозначающая, что сундук в области действия гидролокатора не 
обнаружен. На карте ниже метки C - это сундуки.
Цифра 3 обозначает, что ближайший сундук находится на отдалении в 3 единицы.


\t\t              1         2         3
\t\t    012345678901234567890123456789012

\t\t  0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
\t\t  1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
\t\t  2 `~`C``3`~~~~`C`~~~~`````~~``~~~`` 2
\t\t  3 ````````~~~`````~~~`~`````~`~``~` 3
\t\t  4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4

\t\t    012345678901234567890123456789012
\t\t              1         2         3
(Во время игры сундуки на карте не обозначаются!)

Нажмите клавишу Enter, чтобы продолжить...''')
    input()

    print('''Если гидролокатор опущен прямо на сундук, вы сможете поднять
сундук. Другие гидролокаторы обновят данные о расположении ближайшего сундука.
Сундуки ниже находятся вне диапазона локатора, поэтому отображается буква X.

\t\t              1         2		  3
\t\t    012345678901234567890123456789012

\t\t  0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
\t\t  1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
\t\t  2 `~`X``7`~~~~`C`~~~~`````~~``~~~`` 2
\t\t  3 ````````~~~`````~~~`~`````~`~``~` 3
\t\t  4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4

\t\t    012345678901234567890123456789012
\t\t              1         2         3

Сундуки с сокровищами не перемещаются. Гидролокаторы определяют сундуки
на расстоянии до 9 единиц. Попробуйте поднять все 3 сундука до того, как все
гидролокаторы будут опущены на дно. Удачи!

Нажмите клавишу Enter, чтобы продолжить...''')

    input()


def chooseDif():
    difficulty = ''

    while difficulty not in 'Л С Т У'.split():
        print('Выберите уровень сложности: Л - Легкий, С - Средний, Т - Тяжелый')
        print('и Ультратяжлый - У (для самых хардовых игроков)')
        difficulty = input().upper()
        if difficulty == 'Л':
            return [25, 3]
        elif difficulty == 'С':
            return [20, 3]
        elif difficulty == 'Т':
            return [15, 3]
        elif difficulty == 'У':
            return [15, 5]


# Начало кода игры
print('Охотник за сокровищами')
print()
print('Показать инструктаж? (да/нет)')
if input().lower().startswith('д'):
    showInstructions()

while True:
    # Настройка игры
    sonarDevices, chestNum = chooseDif()
    theBoard = getNewBoard()
    theChests = getRandomChests(chestNum)
    drawBoard(theBoard)
    previousMoves = []

    while sonarDevices > 0:
        # Показываем гидролокаторые устройства и сундуки с сокровищами.
        print(
            'Осталось гидролокаторов: %s.Осталось сундуков с сокровищами: %s' % (
                sonarDevices, len(theChests)))

        x, y = enterPlayerMove(previousMoves)
        # Мы должны отслеживать все ходы, чтобы гидролокаторы могли обновляться
        previousMoves.append([x, y])

        moveResult = makeMove(theBoard, theChests, x, y)

        if moveResult == 'Вы нашли сундук с сокровищами на затонувшем судне!':
            # Обновить все гидролокаторные устройства, в настоящее время
            # находящихся на карте.
            for x, y in previousMoves:
                makeMove(theBoard, theChests, x, y)

        drawBoard(theBoard)
        print(moveResult)

        if len(theChests) == 0:
            print('Вы нашли все сундуки с сокровищами на затонувших судах! Поздравляем и спасибо за игру!')
            break

        sonarDevices -= 1

        if sonarDevices == 0:
            print(
                'Все гидролокаторы опущены на дно! Придется разворачивать корабль и')
            print('отправляться домой, в порт!')
            print('ИГРА ОКОНЧЕНА')
            print('Вы не нашли сундуки в следующих местах')
            for x, y in theChests:
                print(' %s, %s' % (x, y))

    print('Хотите сыграть еще раз? (да или нет)')
    if not input().lower().startswith('да'):
        sys.exit()
