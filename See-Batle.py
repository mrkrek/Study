from random import randint


class Dot:  # Точка
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "(" + str(self.x) + " , " + str(self.y) + ")"


class Ship:  # Кораблик
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
                ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."

                    self.busy.append(cur)

    def prinfield(self, other):
        res = "-------------------------------------------------------------- \n"
        res += "          Поле Игрока                 Поле Компуктера)))    \n"
        res += "-------------------------------------------------------------- \n"
        res += "  || 1 | 2 | 3 | 4 | 5 | 6 ||   || 1 | 2 | 3 | 4 | 5 | 6 || "
        for i in range(6):
            res += "\n" + str(i + 1) + " ||"

            for j in range(6):
                line = str()
                line += " " + self.field[i][j] + " |"

                if self.hid:
                    line = line.replace("■", "O")
                res += line

            res += "|   ||"

            for j in range(6):
                line = str()
                line += " " + other.field[i][j] + " |"

                if other.hid:
                    line = line.replace("■", "O")

                res += line

            res += "| " + str(i + 1)

        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"

                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True

                else:
                    print("Корабль подбит!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Промах!")
        return False

    def begin(self):
        self.busy = []


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Player:  # клас игрок
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat

            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        global d
        step = 1
        for i in range(6):
            for j in range(6):
                if self.enemy.field[i][j] == "X":
                    if i == 0:
                        if self.enemy.field[i + 1][j] == "■":
                            if step:
                                d = Dot(i + 1, j)
                                step = 0
                                break

                    if i == 5:
                        if self.enemy.field[i - 1][j] == "■":
                            if step:
                                d = Dot(i - 1, j)
                                step = 0
                                break

                    if 5 > i > 0:
                        if self.enemy.field[i - 1][j] != "■" and self.enemy.field[i + 1][j] == "■":
                            if step:
                                d = Dot(i + 1, j)
                                step = 0
                                break

                        if self.enemy.field[i - 1][j] == "■" and self.enemy.field[i + 1][j] != "■":
                            if step:
                                d = Dot(i - 1, j)
                                step = 0
                                break

                    if j == 0:
                        if self.enemy.field[i][j + 1] == "■":
                            if step:
                                d = Dot(i, j + 1)
                                step = 0
                                break

                    if j == 5:
                        if self.enemy.field[i][j - 1] == "■":
                            if step:
                                d = Dot(i, j - 1)
                                step = 0
                                break

                    if 5 > j > 0:
                        if self.enemy.field[i][j - 1] != "■" and self.enemy.field[i][j + 1] == "■":
                            if step:
                                d = Dot(i, j + 1)
                                step = 0
                                break

                        if self.enemy.field[i][j - 1] == "■" and self.enemy.field[i][j + 1] != "■":
                            if step:
                                d = Dot(i, j - 1)
                                step = 0
                                break

        if step:
            while True:
                d = Dot(randint(0, 5), randint(0, 5))
                if d not in self.enemy.busy:
                    break

        print("Ход компьютера: " + str(d.x + 1) + " " + str(d.y + 1))
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


def greet():
    print("------------------------------")
    print("         МОРСКОЙ БОЙ          ")
    print("------------------------------")
    print("       формат ввода: x y      ")
    print("       x - номер строки       ")
    print("       y - номер столбца      ")
    print("------------------------------")


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1

                if attempts > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break

                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def loop(self):
        num = 0
        while True:
            print(self.us.board.prinfield(self.ai.board))

            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()

            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print(self.us.board.prinfield(self.ai.board))
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print(self.us.board.prinfield(self.ai.board))
                print("-" * 20)
                print("Компьютер выиграл!")
                break

            num += 1

    def start(self):
        greet()
        self.loop()


game = Game()
game.start()
