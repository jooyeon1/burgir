import random
from tkinter import *
from PIL import ImageTk, Image


class Burger:
    BUN_MAP = {
        'Standart bun': 'standart',
        'Sesame bun': 'sesame',
        'English muffin': 'english'
    }

    FILL_MAP = {
        'Lettuce': 'lettuce',
        'Tomato': 'tomato',
        'Bacon': 'bacon',
        'Chicken patty': 'chicken',
        'Beef - Rare': 'beefr',
        'Beef - Medium': 'beefm',
        'Beef - Well Done': 'beefw'
    }

    buns = [bun for bun in BUN_MAP]

    def __init__(self):
        self.window = None
        self.frame = None
        self.bun = random.choice(self.buns)
        self.menu = 'bun'

        self.toppings = ['Lettuce', 'Tomato', 'Lettuce']
        self.create_window()
        self.show(self.bun, self.toppings)

    def create_window(self):
        self.window = Tk()
        self.window.minsize(500, 200)

        self.frame = Frame(self.window)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def reset_window(self):
        self.clear_window()
        self.show(self.bun, self.toppings)

    def show(self, bun, fillings):
        self.create_menu()

        top = bun_pos(self.BUN_MAP[bun], 't')
        top_img = create_image(image(top))
        create_img_label(top_img, self.window)

        i = 0
        fill_imgs = []
        for filling in fillings:
            fill_imgs.append(create_image(image(self.FILL_MAP[filling])))
            create_img_label(fill_imgs[i], self.window)
            i += 1

        bot = bun_pos(self.BUN_MAP[bun], 'b')
        bot_img = create_image(image(bot))
        create_img_label(bot_img, self.window)

        self.window.mainloop()

    def bun_menu(self):
        selected_bun = StringVar(self.window)
        selected_bun.set(self.bun)

        bun_menu = OptionMenu(self.window, selected_bun, *self.buns, command=self.change_bun)
        bun_menu.pack()

    def create_menu(self):
        if self.menu == 'bun':
            self.bun_menu()
            return

        if self.menu == 'topping':
            pass

    def change_bun(self, bun):
        self.bun = bun
        self.reset_window()


def option_change(val):
    root.destroy()
    show_burger(['Lettuce', 'Tomato', 'Lettuce'], fill_map, val, bun_map, root)


def image(name):
    return 'imgs/' + name + ('.png' if not name.endswith('.png') else '')


def create_image(path):
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)

    return img


def create_img_label(img, tkwindow):
    label = Label(tkwindow, image=img)
    label.pack()


def bun_pos(select_bun, top):
    return select_bun + '_' + ('top' if top == 't' else 'bottom') + '.png'


def show_burger(fillings, possible_fillings: dict, bun, possible_buns: dict, tkwindow):
    top = bun_pos(possible_buns[bun], 't')
    top_img = create_image(image(top))
    create_img_label(top_img, tkwindow)

    i = 0
    fill_imgs = []
    for filling in fillings:
        fill_imgs.append(create_image(image(possible_fillings[filling])))
        create_img_label(fill_imgs[i], tkwindow)
        i += 1

    bot = bun_pos(possible_buns[bun], 'b')
    bot_img = create_image(image(bot))
    create_img_label(bot_img, tkwindow)

    tkwindow.mainloop()


# root = Tk()
# root.minsize(500, 200)
#
# buns = ['Standart bun', 'Sesame bun', 'English muffin']
# selected_bun = StringVar(root)
# selected_bun.set('Standard bun')
#
# bun_menu = OptionMenu(root, selected_bun, *buns, command=option_change)
# bun_menu.pack()
#
# show_burger(['Lettuce', 'Tomato', 'Lettuce'], fill_map, 'Standart bun', bun_map, root)
#
# root.mainloop()
burger = Burger()
