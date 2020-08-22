
SOURIS_COLORIER = ("XXX             ",
                   "X..XX           ",
                   "X....XX         ",
                   " X.....XX       ",
                   " X.......XX     ",
                   "  X........XX   ",
                   "  X..........XX ",
                   "   X...........X",
                   "   X...........X",
                   "    X....XXXXXX ",
                   "    X....X      ",
                   "     X...X      ",
                   "     X...X      ",
                   "      X..X      ",
                   "      X..X      ",
                   "       XX       ")


for ligne in SOURIS_COLORIER:
    texte = ''
    for lettre in ligne:
        if lettre == 'X':
            texte += 'o'
        elif lettre == '.':
            texte += 'o'
        else:
            texte += ' '
    print(f'    "{texte}",')
