import random
from tkinter import *
from PIL import ImageTk, Image


class Burger:
    BUN_MAP = {
        'Standart bun': 'standart',
        'Sesame bun': 'sesame',
        'English muffin': 'english'
    }

    SAUCE_MAP = {
        'Ketchup': 'ketchup',
        'Mustard': 'mustard',
        'Mayonaisse': 'mayo',
        'BBQ': 'bbq'
    }

    TOPPING_MAP = {
        'Lettuce': 'lettuce',
        'Tomato': 'tomato',
        'Bacon': 'bacon',
        'Cheese': 'cheese',
        'Onion': 'onion',
        'Pickle': 'pickle'
    }

    MEAT_MAP = {
        'Chicken': 'chicken',
        'Beef': 'beef'
    }

    DONENESS_MAP = {
        'Rare': 'r',
        'Medium': 'm',
        'Well Done': 'w'
    }

    buns = [bun for bun in BUN_MAP]
    sauces = [sauce for sauce in SAUCE_MAP]
    meats = [meat for meat in MEAT_MAP]
    doneness = [done for done in DONENESS_MAP]

    def __init__(self):
        self.window = None
        self.topping_frame = None
        self.meat_frame = None

        self.bun = random.choice(self.buns)
        self.sauce = random.choice(self.sauces)
        self.meat = self.MEAT_MAP[random.choice(self.meats)]
        self.done = random.choice(self.doneness)
        self.meat += self.DONENESS_MAP[self.done] if self.meat == 'beef' else ''

        self.toppings = {topping: bool(random.getrandbits(1)) for topping in self.TOPPING_MAP}
        self.create_window()
        self.show()

    def hr(self):
        label = Label(self.window, text='---------------------')
        label.pack()

    def add_label(self, text):
        label = Label(self.window, text=text)
        label.pack()

    def create_window(self):
        self.window = Tk()
        self.window.minsize(500, 200)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def reset_window(self):
        self.clear_window()
        self.show()

    def show(self):
        self.bun_menu()
        self.sauce_menu()
        self.meat_menu()
        self.doneness_menu()
        self.topping_menu()

        top = bun_pos(self.BUN_MAP[self.bun], 't')
        top_img = create_image(image(top))
        create_img_label(top_img, self.window)

        i = 0
        top_imgs = []
        for topping in self.toppings:
            if not self.toppings[topping]:
                continue
            top_imgs.append(create_image(image(self.TOPPING_MAP[topping])))
            create_img_label(top_imgs[i], self.window)
            i += 1

        meat = create_image(image(self.meat))
        create_img_label(meat, self.window)

        sauce = create_image(image(self.SAUCE_MAP[self.sauce]))
        create_img_label(sauce, self.window)

        bot = bun_pos(self.BUN_MAP[self.bun], 'b')
        bot_img = create_image(image(bot))
        create_img_label(bot_img, self.window)

        self.window.mainloop()

    def bun_menu(self):
        self.add_label('Select bun:')

        selected_bun = StringVar(self.window)
        selected_bun.set(self.bun)

        bun_menu = OptionMenu(self.window, selected_bun, *self.buns, command=self.change_bun)
        bun_menu.pack()

    def change_bun(self, bun):
        self.bun = bun
        self.reset_window()

    def sauce_menu(self):
        self.hr()
        self.add_label('Select sauce:')

        choice = StringVar()
        choice.set(self.sauce)

        menu = OptionMenu(self.window, choice, *self.sauces, command=self.change_sauce)
        menu.pack()

    def change_sauce(self, sauce):
        self.sauce = sauce
        self.reset_window()

    def meat_menu(self):
        self.hr()
        self.add_label('Select patty:')

        self.meat_frame = Frame(self.window)

        choice = StringVar()
        choice.set(random.choice(self.meats))

        for meat in self.meats:
            button = Radiobutton(
                self.meat_frame, text=meat, value=self.MEAT_MAP[meat], variable=choice,
                command=lambda: self.change_meat(choice.get(), self.DONENESS_MAP[self.done])
            )
            button.pack(side='left')

        self.meat_frame.pack()

    def change_meat(self, meat, doneness):
        self.meat = meat + doneness \
            if meat == 'beef' \
            else meat

        self.reset_window()

    def doneness_menu(self):
        if not self.meat.startswith('beef'):
            return

        self.hr()
        self.add_label('Select doneness:')

        choice = StringVar()
        choice.set(self.done)

        menu = OptionMenu(self.window, choice, *self.doneness, command=self.change_doneness)
        menu.pack()

    def change_doneness(self, doneness):
        self.done = doneness
        self.change_meat(self.meat[:-1], self.DONENESS_MAP[doneness])

    def topping_menu(self):
        self.topping_frame = Frame(self.window)

        self.hr()
        self.add_label('Select toppings:')

        buttons = []

        for topping in self.toppings:
            var = BooleanVar()
            var.set(self.toppings[topping])
            buttons.append(var)
            checkbox = Checkbutton(
                self.topping_frame, text=topping, variable=var
            )
            checkbox.pack(side='left')

        def change_topping():
            self.toppings = {selected: value.get() for selected, value in zip(self.toppings, buttons)}
            self.reset_window()

        submit = Button(self.topping_frame, text='Submit toppings', command=change_topping)
        submit.pack()

        self.topping_frame.pack()


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


burger = Burger()
