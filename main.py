from tkinter import *
from PIL import ImageTk, Image


def option_change(val):
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


bun_map = {
    'Standart bun': 'standart',
    'Sesame bun': 'sesame',
    'English muffin': 'english'
}

fill_map = {
    'Lettuce': 'lettuce',
    'Tomato': 'tomato',
    'Bacon': 'bacon',
    'Chicken patty': 'chicken',
    'Beef - Rare': 'beefr',
    'Beef - Medium': 'beefm',
    'Beef - Well Done': 'beefw'
}

root = Tk()
root.minsize(500, 200)

buns = ['Standart bun', 'Sesame bun', 'English muffin']
selected_bun = StringVar(root)
selected_bun.set('Standard bun')

bun_menu = OptionMenu(root, selected_bun, *buns, command=option_change)
bun_menu.pack()

show_burger(['Lettuce', 'Tomato', 'Lettuce'], fill_map, 'Standart bun', bun_map, root)

# root.mainloop()
