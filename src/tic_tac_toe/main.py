field = [[' ', 1, 2, 3], [1, '-', '-', '-'], [2, '-', '-', '-'], [3, '-', '-', '-']]
players = {1: 'x', 2: 'o'}

def print_field():
    '''
    Выводит игровое поле в консоль
    '''
    for row in field:
        print(*row)

def game_move(symbol):
    '''
    Принимает значение символа текущего игрока.
    Запрашивает у пользователя координаты свободной клетки поля,
    проверяет их корректность и отсутствие символа в выбранной клетке,
    после чего размещает символ игрока в выбранной клетке.
    При ошибках ввода или неверных координатах
    повторно запрашивает ввод
    
    Параметры: symbol: Символ игрока, который будет размещен в выбранной клетке поля
    '''
    print('Введите через пробел координаты (ряд и столбец) свободной клетки и нажмите Enter')
    try:
        row, column = [int(n) for n in input().split()]
        if 1 <= row <= 3 and 1 <= column <= 3:
            if field[row][column] == '-':
                field[row][column] = symbol
                print_field()
            else:
                print('Эта клетка уже занята')
                game_move(symbol)
        else:
            print('Введите числа от 1 до 3')
            game_move(symbol)
    except:
        print('Требуется ввести два целых числа')
        game_move(symbol)

def check():
    '''
    Проверяет, есть ли в текущем состоянии игрового поля выигрышная комбинация
    
    Возвращает:
    True - если найдена выиграшная комбинация
    False - если выиграшной комбинации нет
    '''
    for row in range(1, 4):
        if field[row][1] == field[row][2] == field[row][3] != '-':
            return True
    for column in range(1, 4):
        if field[1][column] == field[2][column] == field[3][column] != '-':
            return True
    if field[1][1] == field[2][2] == field[3][3] != '-':
        return True
    if field[3][1] == field[2][2] == field[1][3] != '-':
        return True

print_field()
for i in range(1, 10):
    player = 1 if i % 2 else 2
    game_move(players[player])
    
    if i > 4 and check():
        print(f'Выиграл игрок {player}')
        break
    elif i == 9 and not check():
        print('Ничья')
    
