import random

class BoardOutException(Exception):
    """Исключение, выбрасываемое при попытке обратиться к точке за пределами игрового поля.

    Используется для проверки корректности координат выстрела или размещения корабля.
    """
    pass

class BoardShotException(Exception):
    """Исключение, выбрасываемое при попытке выстрелить в уже использованную клетку.

    Гарантирует, что игрок не сможет повторить выстрел в ту же точку.
    """
    pass

class BoardShipPlacementException(Exception):
    """Исключение, выбрасываемое при невозможности разместить корабль на доске.

    Возникает, если корабль выходит за границы поля или пересекается с другими кораблями/их контурами.
    """
    pass


class Dot:
    """Представляет точку на игровом поле.

    Атрибуты:
        x (int): номер ряда (вертикаль).
        y (int): номер столбца (горизонталь).
        condition (str): состояние точки ('О' — пусто, '■' — корабль, 'X' — подбит, 'T' — промах, '.' — контур).
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.condition = 'О'
    
    def __eq__(self, other):
        """Проверяет равенство двух точек по координатам.

        Параметры:
            other (Dot): другая точка для сравнения.

        Возвращает:
            bool: True, если координаты совпадают, иначе False.
        """
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        """Возвращает строковое представление состояния точки.

        Возвращает:
            str: значение `condition`.
        """
        return self.condition
     

class Ship:
    """Представляет корабль на игровом поле.

    Атрибуты:
        length (int): длина корабля (количество клеток).
        bow_ship (Dot): точка, где размещён нос корабля.
        direction (int): направление корабля (0 — горизонтально, 1 — вертикально).
        lives (int): количество непораженных клеток корабля.
    """

    def __init__(self, length, bow_ship, direction):
        self.length = length
        self.bow_ship = bow_ship
        self.direction = direction
        self.lives = length
        
    @property
    def dots(self):
        """Возвращает список всех точек, занимаемых кораблём.
        Рассчитывает координаты всех клеток корабля на основе начальной точки и направления.

        Возвращает:
            list[Dot]: список объектов Dot, соответствующих клеткам корабля.
        """
        list_dots = []
        for i in range(self.length):
            x = self.bow_ship.x
            y = self.bow_ship.y
            if self.direction == 0:  # горизонтально
                x += i
            elif self.direction == 1:  # вертикально
                y += i
            list_dots.append(Dot(x, y))
        return list_dots

    def is_hit(self, dot):
        """Проверяет, попала ли точка выстрела в корабль.

        Параметры:
            dot (Dot): точка выстрела.

        Возвращает:
            bool: True, если точка принадлежит кораблю, иначе False.
        """
        return dot in self.dots


class Board:
    """Игровое поле (доска) для размещения кораблей и ведения боя.

    Атрибуты:
        board (list): двумерный список, представляющий игровое поле (7×7, включая заголовки).
        list_ships (list): список размещённых кораблей.
        hid (bool): флаг, скрывающий корабли на доске (для поля противника).
        count_live_ship (int): количество живых кораблей.
        used_dots (list): список использованных клеток (для контуров и выстрелов).
    """

    def __init__(self, hid=False):
        self.board = [[' ', 1, 2, 3, 4, 5, 6], 
                      [1, Dot(1,1), Dot(1,2), Dot(1,3), Dot(1,4), Dot(1,5), Dot(1,6)], 
                      [2, Dot(2,1), Dot(2,2), Dot(2,3), Dot(2,4), Dot(2,5), Dot(2,6)], 
                      [3, Dot(3,1), Dot(3,2), Dot(3,3), Dot(3,4), Dot(3,5), Dot(3,6)], 
                      [4, Dot(4,1), Dot(4,2), Dot(4,3), Dot(4,4), Dot(4,5), Dot(4,6)], 
                      [5, Dot(5,1), Dot(5,2), Dot(5,3), Dot(5,4), Dot(5,5), Dot(5,6)], 
                      [6, Dot(6,1), Dot(6,2), Dot(6,3), Dot(6,4), Dot(6,5), Dot(6,6)]]
        self.list_ships = []
        self.hid = hid
        self.count_live_ship = 7
        self.used_dots = []
        
    def add_ship(self, ship):
        """Размещает корабль на доске. Выбрасывает исключение при ошибке.
        Проверяет, что все точки корабля находятся в пределах поля и не пересекаются с другими объектами.

        Параметры:
            ship (Ship): корабль для размещения.

        Raises:
            BoardShipPlacementException: если корабль нельзя разместить.
        """
        for dot in ship.dots:
            if self.out(dot) or dot in self.used_dots:
                raise BoardShipPlacementException()
        for dot in ship.dots:
            self.board[dot.x][dot.y].condition = '■'
            self.used_dots.append(dot)
        self.list_ships.append(ship)
        self.contour(ship)
        
    def contour(self, ship, verb=False): 
        """Обводит корабль контуром, помечая соседние клетки как занятые.
        Если `verb=True`, визуально отображает контур на поле (для отладки).

        Параметры:
            ship (Ship): корабль, для которого создаётся контур.
            verb (bool): флаг отображения контура на поле.
        """
        contour_ship = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 0), (0, 1),
                        (1, -1), (1, 0), (1, 1)]
        for dot in ship.dots:
            for x, y in contour_ship:
                contour_dot = Dot(dot.x + x, dot.y + y)
                if not (self.out(contour_dot)) and contour_dot not in self.used_dots:
                    if verb:
                        self.board[contour_dot.x][contour_dot.y].condition = "."
                    self.used_dots.append(contour_dot) #extend
    
    def out(self, dot):
        """Проверяет, выходит ли точка за пределы игрового поля.

        Параметры:
            dot (Dot): проверяемая точка.

        Возвращает:
            bool: True, если точка вне поля, иначе False.
        """
        return not (0 < dot.x < 7 and 0 < dot.y < 7)

    def shot(self, dot):
        """Выполняет выстрел по указанной точке.
        Выбрасывает исключения при попытке выстрела за пределы поля или в использованную клетку.
        При попадании в корабль отмечает клетку как 'X', при промахе — как 'T'.
        Если корабль уничтожен, отмечает его контур.

        Параметры:
            dot (Dot): точка, в которую производится выстрел.

        Возвращает:
            bool: True, если нужен повторный ход (при попадании), иначе False.
        
        Raises:
            BoardOutException: если точка вне игрового поля.
            BoardShotException: если клетка уже была использована.
        """
        if self.out(dot):
            raise BoardOutException()
        if dot in self.used_dots:
            raise BoardShotException()                
        self.used_dots.append(dot)
        for ship in self.list_ships:
            if ship.is_hit(dot):
                ship.lives -= 1
                self.board[dot.x][dot.y].condition = "X"
                if ship.lives == 0:
                    self.contour(ship, verb=True)
                    self.count_live_ship -= 1
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль подбит!")
                    return True
        self.board[dot.x][dot.y].condition = "T"
        print("Промах!")
        return False
    
    def __str__(self):
        """Возвращает строковое представление игрового поля.
        Если self.hid == True, скрывает корабли (заменяет '■' на 'О').
        Иначе отображает все элементы поля.

        Возвращает:
            str: текстовое представление доски.
        """
        result = ""
        if self.hid:
            for row in self.board:
                result = result + ' '.join((elem.condition if elem.condition != '■' else 'О') if isinstance(elem, Dot) else str(elem) for elem in row) + '\n'
        else:
            for row in self.board:
                result = result + ' '.join(str(elem) for elem in row) + '\n'
        return result

    def clean_used_dots(self):
        """Очищает список использованных клеток перед началом игры.
        Удаляет все отметки о выстрелах и контурах, чтобы поле было готово к новому раунду.
        """
        self.used_dots = []


class Player:
    """Базовый класс игрока.

    Определяет общий интерфейс для игроков (человека и компьютера).
    Должен быть унаследован для реализации конкретных стратегий хода.
    """

    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board
    
    def ask(self):
        """Запрашивает у игрока координаты выстрела.
        Должен быть переопределён в наследниках (User, AI).

        Raises:
            NotImplementedError: если метод не переопределён.
        """
        raise NotImplementedError()
    
    def move(self):
        """Выполняет ход игрока.
        Повторяет запрос до успешного выстрела (без исключений).
        Возвращает True, если игрок должен сделать ещё один ход (при попадании).

        Возвращает:
            bool: True, если требуется повторный ход, иначе False.
        """
        while True:
            try:
                dot = self.ask()
                result = self.enemy_board.shot(dot)
                return result
            except BoardOutException:
                print('Вы вышли за пределы доски! Попробуйте ещё раз. Введите числа от 1 до 6')
            except BoardShotException:
                print('Эта клетка уже была использована. Попробуйте ещё раз')


class AI (Player):
    """Класс игрока-компьютера.
    Автоматически выбирает случайные координаты для выстрела.
    """

    def ask(self):
        """Генерирует случайные координаты выстрела.
        Выводит сообщение о ходе компьютера.

        Возвращает:
            Dot: случайная точка на поле.
        """
        x, y = random.randint(1, 6), random.randint(1, 6)
        print(f"Ход компьютера: {x} {y}")
        return Dot(x, y)

        
class User (Player):
    """Класс игрока-человека.
    Запрашивает координаты выстрела у пользователя через консоль.
    """

    def ask(self):
        """Спрашивает у пользователя координаты выстрела.
        Повторяет запрос до корректного ввода.

        Возвращает:
            Dot: точка с введёнными координатами.
        """
        while True:
            print('Введите через пробел координаты (ряд и столбец) свободной клетки, в которую хотите сделать выстрел, и нажмите Enter')
            try:
                x, y = [int(n) for n in input().split()]
                return Dot(x, y)
            except ValueError:
                print('Требуется ввести два целых числа')
 

class Game:
    """Основной класс игры «Морской бой».
    Управляет созданием досок, игроков, игровым циклом и выводом информации.
    """

    def __init__(self):
        board_user = self.random_board() # доска пользователя
        board_ai = self.random_board() # доска компьютера
        self.user = User(board_user, board_ai) # игрок-пользователь   
        self.ai = AI(board_ai, board_user) # игрок-компьютер
        self.user.enemy_board.hid = True
    
    def random_board(self):
        """Генерирует случайную расстановку кораблей на доске.
        Повторяет генерацию, если не удаётся разместить все корабли за 2000 попыток.

        Возвращает:
            Board: готовая доска с размещёнными кораблями.
        """
        board = Board()
        attempts = 0
        ships_to_place = [3, 2, 2, 1, 1, 1, 1]  # порядок: от больших к малым
        for length in ships_to_place:
            while True: 
                attempts += 1
                if attempts > 2000:  # слишком много попыток — начинаем заново
                    return self.random_board()
                ship = Ship(length, Dot(random.randint(1, 6), random.randint(1, 6)), random.randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipPlacementException:
                    continue
        board.clean_used_dots()
        return board

    def greet(self):
        """Выводит приветственное сообщение и правила игры."""
        print("Добро пожаловать в Морской бой!")
        print()
        print("Правила:")
        print("* Поле 6×6 клеток.")
        print("* У каждого игрока: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на 1 клетку.")
        print("* Корабли не могут соприкасаться (даже углами).")
        print("* Ваш ход — введите координаты выстрела в формате «x y» (ряд и столбец).")
        print("* «■» — ваш корабль.")
        print("* «X» — подбитый корабль.")
        print("* «T» — промах.")
        print("* Побеждает тот, кто первым уничтожит все корабли противника.")
        print()

    def loop(self):
        """Основной игровой цикл.
        Чередует ходы игрока и компьютера до победы одной из сторон.
        """
        while True:
            print("Ваше поле:")
            print(self.user.board)
            print("Поле противника:")
            print(self.ai.board)

            user_turn = True
            while user_turn:
                user_turn = self.user.move()
                if user_turn:
                    print("Поле противника:")
                    print(self.ai.board)
                if end := (self.ai.board.count_live_ship == 0):
                    print("Вы победили! Все корабли противника уничтожены!")
                    break
            if end:
                break
            
            ai_turn = True
            while ai_turn:
                ai_turn = self.ai.move()
                if end := (self.user.board.count_live_ship == 0):
                    print("Компьютер победил! Ваши корабли уничтожены!")
                    break
            if end:
                break

            print()

    def start(self):
        """Запускает игру, выводя приветственное сообщение и запуская игровой цикл."""
        self.greet()
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()
