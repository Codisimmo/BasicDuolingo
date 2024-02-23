import tkinter as tk
import random

Slovicka = {
    "Počasí": ["počasí", "déšť", "vítr", "slunce", "mráz", "mlha", "bouřka", "chumelenice", "kroupy", "svítání", "západ", "teplota", "vlhkost", "sníh", "led", "teplo"],
    "Zvířata": ["pes", "kočka", "kůň", "králík", "medvěd", "liška", "slon", "myš", "klokan", "panda", "žirafa", "opice", "tygr", "lev", "jelen", "pták"],
    "Tělo": ["oko", "nos", "ústa", "ucho", "brada", "čelo", "ruka", "noha", "srdce", "ledviny", "játra", "plicy", "žaludek", "koleno", "paže", "prst"],
    "Barvy": ["červená", "modrá", "zelená", "žlutá", "bílá", "černá", "fialová", "oranžová", "růžová", "šedá", "tyrkysová", "zlatá", "stříbrná", "bronzová", "purpurová"],
    "Slovesa": ["běhat", "skákat", "plavat", "létat", "číst", "psát", "hrát", "jíst", "pít", "vidět", "slyšet", "cítit", "milovat", "nenávidět", "myslet"]
}
Slovicka_uk = {
    "Počasí": ["погода", "дощ", "вітер", "сонце", "мороз", "туман", "гроза", "заметіль", "град", "світанок", "захід сонця", "температура", "вологість", "сніг", "льод", "тепло"],
    "Zvířata": ["собака", "кішка", "кінь", "кролик", "ведмідь", "лисиця", "слон", "миша", "кенгуру", "панда", "жирафа", "мавпа", "тигр", "лев", "олень", "птах"],
    "Tělo": ["око", "ніс", "рот", "вухо", "підборіддя", "лоб", "рука", "нога", "серце", "нирки", "печінка", "легені", "живіт", "коліно", "плече", "палець"],
    "Barvy": ["червоний", "синій", "зелений", "жовтий", "білий", "чорний", "фіолетовий", "оранжевий", "рожевий", "сірий", "бірюзовий", "золотий", "срібний", "бронзовий", "пурпурний"],
    "Slovesa": ["бігати", "стрибати", "плавати", "літати", "читати", "писати", "грати", "їсти", "пити", "бачити", "чути", "відчувати", "кохати", "ненавидіти", "думати"]
}

# Inicializace hlavního okna
root = tk.Tk()
root.title("Seřaď tlačítka")
root.geometry("600x360")

# Globální proměnné
kategorie = None
cesky = None
ukrajinsky = None
pismena = None
ukr_label = None
hlaseni = None

# Skóre
score = 0

# Inicializace hry
buttons = []
slots = []
sorted_buttons = []
current_word = []
button_dict = {}


category_var = tk.StringVar(root)
category_var.set("Počasí")


def reset_game():
    global current_word, cesky, ukrajinsky, pismena, ukr_label, slots
    print("Hra byla resetována.")
    cesky = random.choice(Slovicka[kategorie])
    ukrajinsky = Slovicka_uk[kategorie][Slovicka[kategorie].index(cesky)]
    pismena = list(cesky)
    random.shuffle(pismena)
    ukr_label.config(text=ukrajinsky.upper())
    print(f"Náhodné české slovo: {cesky}, Ukrajinský překlad: {ukrajinsky.upper()}")
    print(f"Zamíchaná písmena: {''.join(pismena).upper()}")
    current_word = [''] * len(cesky)
    # smazat existující písmena a sloty
    for frame, label in slots:
        label.destroy()
        frame.destroy()
    slots.clear()
    for button in buttons:
        button.destroy()
    buttons.clear()

    # Vytvoření nových tlačítek s písmeny a jejich umístění vedle sebe v řádku
    button_x = 50
    button_y = 50
    button_width = 50
    button_spacing = 5
    # Vytvoření slotů
    for index in range(len(pismena)):
        frame = tk.Frame(root, height=40, width=40, borderwidth=1, relief="sunken")
        frame.place(x=button_x + index * (button_width + button_spacing), y=button_y + 100)
        frame.pack_propagate(False)
        label = tk.Label(frame, text="", bg="white",fg="white", width=40, height=40)
        label.pack(expand=True, fill="both")
        slots.append((frame, label))
    # Vytvoření tlačítek
    for index, letter in enumerate(pismena):
        button = tk.Button(root, text=letter.upper(), command=lambda idx=index: select_letter(idx))
        frame = tk.Frame(root, width=40, height=40)
        button.place(x=button_x + index * (button_width + button_spacing), y=button_y)
        frame.pack_propagate(False)
        button.bind('<Button-1>', start_drag)
        button.bind('<B1-Motion>', stop_drag)
        buttons.append(button)


def start_drag(event):
    widget = event.widget
    widget._drag_start_x = widget.winfo_x()
    widget._drag_start_y = widget.winfo_y()
    widget._drag_start_x_offset = event.x
    widget._drag_start_y_offset = event.y

def stop_drag(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x_offset + event.x
    y = widget.winfo_y() - widget._drag_start_y_offset + event.y
    widget.place(x=x, y=y)

    # zkontrolovat, jestli je tlačítko uvnitř nějakého slotu
    for index, (frame, label) in enumerate(slots):
        if (x >= frame.winfo_x() and x < frame.winfo_x() + frame.winfo_width() and
            y >= frame.winfo_y() and y < frame.winfo_y() + frame.winfo_height()):
            # pokud ano, aktualizovat current_word a label slotu
            label.config(text=widget.cget("text"))
            current_word[index] = widget.cget("text").lower()
            break

def check_word():
    global score, hlaseni
    guessed_word = ''.join(current_word)
    if guessed_word == cesky:
        score += 1
        score_label.config(text=f"Skóre: {score}")
        hlaseni = "Správně! Skóre bylo zvýšeno."
        show_message(hlaseni)
    else:
        hlaseni = "Špatně. Zkus to znovu."
        show_message(hlaseni)


# Funkce pro aktualizaci hry při zvolení kategorie
def update_category(*args):
    global kategorie
    kategorie = category_var.get()
    print(f"Aktuální kategorie: {kategorie}")
    reset_game()

category_var.trace("w", update_category)

# GUI
# Horní rám pro umístění widgetů
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x")
# Určení nejdelší položky pro nastavení šířky rozbalovacího menu
max_length = max(len(word) for category in Slovicka.values() for word in category)
# Vytvoření rozbalovacího okna s kategoriemi a nastavení stálé šířky
button_width = max_length
category_menu = tk.OptionMenu(top_frame, category_var, *Slovicka.keys())
category_menu.config(width=button_width)
category_menu.pack(side="left", padx=10)
# Label pro zobrazení skóre, umístění do středu horního rámu
score_label = tk.Label(top_frame, text=f"Skóre: {score}")
score_label.pack(side="left", expand=True)
# Tlačítko pro reset hry
reset_button = tk.Button(top_frame, text="Nová hra", command=reset_game, width=button_width)
reset_button.pack(side="left", padx=10)
 # Label s ukrajinským překladem
ukr_label = tk.Label(root, text=f"{ukrajinsky}".upper(), font=("calibri", 14))
ukr_label.pack(side="bottom", pady=10)
# Vytvoření tlačítka pro kontrolu slova
check_button = tk.Button(top_frame, text="Kontrola slova", command=check_word, width=button_width)
check_button.pack(side="left", padx=10)
# hlášení
def show_message(hlaseni):
    ukr_label = tk.Label(root, text=f"{hlaseni}", font=("calibri", 12))
    ukr_label.pack(side="bottom", pady=40)
    def remove_label():
        ukr_label.destroy()
    root.after(2000, remove_label)


root.mainloop()