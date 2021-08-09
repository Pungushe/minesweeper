import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    0: 'white',
    1: 'blue',
    2: 'green',
    3: '#ff0004',
    4: '#01ffff',
    5: '#6464c8',
    6: '#640aff',
    7: '#6495ff',
    8: '#970fff'
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number} {self.is_mine}'


class mineSweeper:
    window = tk.Tk()
    ROW = 7
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for item in range(mineSweeper.ROW + 2):
            temp = []
            for i in range(mineSweeper.COLUMNS + 2):
                btn = MyButton(mineSweeper.window, x=item, y=i)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):

        if mineSweeper.IS_GAME_OVER:
            return

        if mineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_cells()
            self.print_buttons()
            mineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            mineSweeper.IS_GAME_OVER = True
            showinfo('Game Over', ' Вы проиграли')
            for item in range(1, mineSweeper.ROW + 1):
                for i in range(1, mineSweeper.COLUMNS + 1):
                    btn = self.buttons[item][i]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]

        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= mineSweeper.ROW and \
                                1 <= next_btn.y <= mineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        mineSweeper.IS_FIRST_CLICK = True
        mineSweeper.IS_GAME_OVER = False

    def create_setting_win(self):
        win_setting = tk.Toplevel(self.window)
        win_setting.wm_title('Настройки')
        tk.Label(win_setting, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_setting)
        row_entry.insert(0, mineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_setting, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_setting)
        column_entry.insert(0, mineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_setting, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_setting)
        mines_entry.insert(0, mineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_setting, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', ' Вы ввели неправильный формат')
            return

        mineSweeper.ROW = int(row.get())
        mineSweeper.COLUMNS = int(column.get())
        mineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        setting_menu = tk.Menu(menubar, tearoff=0)
        setting_menu.add_command(label='Играть', command=self.reload)
        setting_menu.add_command(label='Настройки', command=self.create_setting_win)
        setting_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=setting_menu)

        count = 1
        for item in range(1, mineSweeper.ROW + 1):
            for i in range(1, mineSweeper.COLUMNS + 1):
                btn = self.buttons[item][i]
                btn.number = count
                btn.grid(row=item, column=i, stick='NWES')
                count += 1

        for item in range(1, mineSweeper.COLUMNS + 1):
            tk.Grid.rowconfigure(self.window, item, weight=1)

        for item in range(1, mineSweeper.ROW + 1):
            tk.Grid.columnconfigure(self.window, item, weight=1)

    def open_all_button(self):
        for item in range(mineSweeper.ROW + 2):
            for i in range(mineSweeper.COLUMNS + 2):
                btn = self.buttons[item][i]
                if btn.is_mine:
                    btn.config(text="*", background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        # self.open_all_button()
        mineSweeper.window.mainloop()

    def print_buttons(self):
        for item in range(1, mineSweeper.ROW + 1):
            for i in range(1, mineSweeper.COLUMNS + 1):
                btn = self.buttons[item][i]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for item in range(1, mineSweeper.ROW + 1):
            for i in range(1, mineSweeper.COLUMNS + 1):
                btn = self.buttons[item][i]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_cells(self):
        for item in range(1, mineSweeper.ROW + 1):
            for i in range(1, mineSweeper.COLUMNS + 1):
                btn = self.buttons[item][i]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbor = self.buttons[item + row_dx][i + col_dx]
                            if neighbor.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, mineSweeper.COLUMNS * mineSweeper.ROW + 1))
        print(f'Исключаем кноку номер {exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:mineSweeper.MINES]


game = mineSweeper()
game.start()
