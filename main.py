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
        self.scroll = None

        self.bun = random.choice(self.buns)
        self.sauce = random.choice(self.sauces)
        self.meat = self.MEAT_MAP[random.choice(self.meats)]
        self.done = random.choice(self.doneness)
        self.meat += self.DONENESS_MAP[self.done] if self.meat == 'beef' else ''

        self.toppings = {topping: bool(random.getrandbits(1)) for topping in self.TOPPING_MAP}
        self.create_window()
        self.show()

    def hr(self, length: int = 15):
        """
        Creates a horizontal ruler.
        """
        label = Label(self.window, text=length*'-')
        label.pack()

    def add_label(self, **kwargs):
        """
        Creates a label with specified options.
        :param kwargs: Label options
        """
        kw = {key: value for key, value in kwargs.items()}
        label = Label(self.window, text=kw.get('text'), image=kw.get('image'))
        label.pack()

    def create_window(self):
        self.window = Tk()
        self.window.minsize(500, 200)

    def clear_window(self):
        """
        Deletes all widgets from the window.
        """
        for widget in self.window.winfo_children():
            widget.destroy()

    def reset_window(self):
        self.clear_window()
        self.show()

    def show(self):
        """
        Adds all the needed widgets to the window and shows it.
        """
        # Create all menus
        self.bun_menu()
        self.sauce_menu()
        self.meat_menu()
        self.doneness_menu()
        self.topping_menu()

        # Add all images
        top = self.bun_pos(self.BUN_MAP[self.bun], 't')
        top_img = self.create_image(self.image(top))
        self.add_label(image=top_img)

        i = 0
        top_imgs = []
        for topping in self.toppings:
            if not self.toppings[topping]:
                continue
            top_imgs.append(self.create_image(self.image(self.TOPPING_MAP[topping])))
            self.add_label(image=top_imgs[i])
            i += 1

        meat = self.create_image(self.image(self.meat))
        self.add_label(image=meat)

        sauce = self.create_image(self.image(self.SAUCE_MAP[self.sauce]))
        self.add_label(image=sauce)

        bot = self.bun_pos(self.BUN_MAP[self.bun], 'b')
        bot_img = self.create_image(self.image(bot))
        self.add_label(image=bot_img)

        self.window.mainloop()

    def bun_menu(self):
        self.add_label(text='Select bun:')

        selected_bun = StringVar(self.window)
        selected_bun.set(self.bun)

        bun_menu = OptionMenu(self.window, selected_bun, *self.buns, command=self.change_bun)
        bun_menu.pack()

    def change_bun(self, bun):
        self.bun = bun
        self.reset_window()

    def sauce_menu(self):
        self.hr()
        self.add_label(text='Select sauce:')

        choice = StringVar()
        choice.set(self.sauce)

        menu = OptionMenu(self.window, choice, *self.sauces, command=self.change_sauce)
        menu.pack()

    def change_sauce(self, sauce):
        self.sauce = sauce
        self.reset_window()

    def meat_menu(self):
        self.hr()
        self.add_label(text='Select patty:')

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
        self.add_label(text='Select doneness:')

        choice = StringVar()
        choice.set(self.done)

        menu = OptionMenu(self.window, choice, *self.doneness, command=self.change_doneness)
        menu.pack()

    def change_doneness(self, doneness):
        self.done = doneness
        self.change_meat(self.meat[:-1], self.DONENESS_MAP[doneness])

    def topping_menu(self):
        def change_topping():
            self.toppings = {selected: value.get() for selected, value in zip(self.toppings, buttons)}
            self.reset_window()

        self.topping_frame = Frame(self.window)

        self.hr()
        self.add_label(text='Select toppings:')

        buttons = []

        for topping in self.toppings:
            var = BooleanVar()
            var.set(self.toppings[topping])
            buttons.append(var)
            checkbox = Checkbutton(
                self.topping_frame, text=topping, variable=var,
                command=change_topping
            )
            checkbox.pack(side='left')

        self.topping_frame.pack()

    @staticmethod
    def image(name):
        """
        :param name: Name of the image
        :return: Path to the image
        """
        return 'imgs/' + name + ('.png' if not name.endswith('.png') else '')

    @staticmethod
    def create_image(path):
        """
        :param path: Path to the wanted image
        :return: Object of the image to pass to tkinter
        """
        img = Image.open(path)
        img = ImageTk.PhotoImage(img)

        return img

    @staticmethod
    def bun_pos(select_bun, position):
        """
        Adds a suffix to image name based on if it's the top or bottom bun.
        :param select_bun: Selected bun name
        :param position: Position of the bun
        :return: Path to the wanted image
        """
        return select_bun + '_' + ('top' if position == 't' else 'bottom') + '.png'


burger = Burger()
