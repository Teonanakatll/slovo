from tkinter import *
from tkinter import messagebox
from random import randint

g = 0
if (g > 5):
    wordLabel["text"] = wordComp
# ========================= МЕТОДЫ И ФУНКЦИИ ===================================

# Метод при нажатии на клавишу
def pressKey(event):
    if (event.keycode == 16):
        wordLabel["text"] = wordComp
    ch = event.char.upper()
    if (len(ch) == 0):
        return 0

    codeBtn = ord(ch) - st

    pressLetter(codeBtn)
    
    print()
    
# Начало нового раунда
def startNewRound():
    global wordStar, wordComp, dictonary, userTry

    for i in range(32):
        btn[i]["text"] = chr(st + i)
        btn[i]["state"] = "normal"

    userTry = 10

    # Загадываем слово
    wordComp = dictonary[randint(0, len(dictonary) - 1)]
    dictonary.pop(dictonary.index(wordComp))
    print(dictonary)

    # Формируем строку из "*"
    wordStar = "*" * len(wordComp)

    # Устанавливаем текст в метку
    wordLabel["text"] = wordStar

    # Устанавливаем метку по центру окна
    wordLabel.place(x=WIDTH // 2 - wordLabel.winfo_reqwidth() // 2, y=50)

    updateInfo()


# Возвращаем слово с открытыми символами
def getWordStar(ch):
    # Переменная для результата
    ret = ""
    for i in range(len(wordComp)):
        # Сравниваем символы
        if (wordComp[i] == ch):
            ret += ch
        else:
            ret += wordStar[i]
    return ret
        
    

# При нажатии мышкой на кнопку
def pressLetter(n):
    global wordStar, score, userTry
    btn[n]["text"] = "."
    btn[n]["state"] = "disabled"

    # Временная переменная
    oldWordStar = wordStar

    # Получаем строку с открытыми симвалами
    wordStar = getWordStar(chr(st + n))
    wordLabel["text"] = wordStar

    # Находим различие между старой и новой строкой
    count = compareWord(wordStar, oldWordStar)

    if (count > 0):
        score += count * 5
    else:
        score -= 10

        if (score < 0):
            score = 0
            
    userTry -= 1

    if (wordStar == wordComp):
        score += score // 2
        
        updateInfo()
        
        if (score > topScore):
            messagebox.showinfo("Поздравляю!" f" Вы топчик! Угадано слово: {wordComp}! Нажмите ОК для продолжения игры.")       
            saveTopScore()
        else:
            messagebox.showinfo(f"Отлично! Слово угадано: {wordComp}. Продолжаем играть!")
        startNewRound()
    elif (userTry <= 0):
        messagebox.showinfo("Бу! Попытки кончились! Возвращайся...")
        quit(0)

    

    updateInfo()

def compareWord(s1, s2):
    res = 0
    for i in range(len(s1)):
        if (s1[i] != s2[i]):
            res += 1
    return res
            


# Загружает слова в список
def getWordsFromFile():
    ret = []

    # Ставим блок проверки ошибок
    try:
        # Получаем дескриптор.
        f = open("words.dat", "r", encoding="utf-8")
        # Читаем построчно
        for l in f.readlines():
            # Обязательно убираем последний символ
            # переноса строки (типа нажатый Enter)
            l = l.replace("\n", "")

            # Добавляем слово в список
            ret.append(l)
        # Незабываем закрыть файл!
        f.close()
    except:
        # Что произойдет в случае ошибки?
        # Например если файл недоступен?
        print("Проблема с файлом. Программа прекращает работу.")
        quit(0)

    return ret


# Обновляем информацию об очках и т.д.
def updateInfo():
    scoreLabel["text"] = f"Ваши очки: {score}"
    topScoreLabel["text"] = f"Лучший результат: {topScore}"
    userTryLabel["text"] = f"Осталось попыток: {userTry}"
    
# Сохраняет в файл очки пользователя
def saveTopScore():
    global topScore
    topScore = score
    try:
        f = open("topchik.dat", "w", encoding="utf-8")
        f.write(str(topScore))
        f.close()
    except:
        messagebox.showinfo("Ошибка!", "Возникла проблема с файлом при сохранении.")

# Возвращает максимальное значение очков из файла
def getTopScore():
    try:
        f = open("topchik.dat", "r", encoding="utf-8")
        m = int(f.readline())
        f.close
    except:
        m = 0
    return m
    
# ============================= ПЕРЕМЕННЫЕ =====================================

# Переменные для хранения значений
score = 0                     # Текущие очки
topScore = getTopScore ()       # Рекорд игры, будем загружать из файла
userTry = 10                  # Количество попыток, каждая попытка -1 балл


# Определяем глобально: "загаданное слово"
wordComp = ""
# Определяем глобально: "слово со звездочками"
wordStar = ""


# ============================= ЭЛЕМЕНТЫ ОКНА ==================================
# Создание окна
root = Tk()                      # В переменной root хранится ссылка на окно в памяти
root.bind("<Key>", pressKey)
root.resizable(False, False)     # Запрещаем изменение размеров
root.title("Угадай слово by ВГ") # Устанавливаем заголовок

# Настройки геометрии окна
WIDTH = 810     # Ширина
HEIGHT = 320    # Высота

# Получим средствами языка ширину и высоту экрана в пикселях
SCR_WIDTH = root.winfo_screenwidth()
SCR_HEIGHT = root.winfo_screenheight()

# И вычислим точку, в которой расположим окно на экране 
POS_X = SCR_WIDTH // 2 - WIDTH // 2
POS_Y = SCR_HEIGHT // 2 - HEIGHT // 2

# Устанавливаем параметры окна
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

# Метка для вывода слова, которое человек угадывает в текущем раунде
wordLabel = Label(font="consolas 35")

# Метки для отображения текущих очков и рекорда
scoreLabel = Label(font=", 12")
topScoreLabel = Label(font=", 12")

# Метка оставшихся попыток
userTryLabel = Label(font=", 12")

# Устанавливаем метки в окне
scoreLabel.place(x=10, y=165)
topScoreLabel.place(x=10, y=190)
userTryLabel.place(x=10, y=215)

# =============================== КНОПКИ =======================================

st = ord("А")   # Для определения символа на кнопке по коду
btn = []        # Список кнопок    

for i in range(32):
    btn.append(Button(text=chr(st + i), width=2, font="consolas 15")) # Создаём и добавляем в список
    btn[i].place(x=215 + (i % 11) * 35, y=150 + i // 11 * 50)         # Расчитываем координаты
    btn[i]["command"] = lambda x=i: pressLetter(x)                    # Определяем переход на метод
                                                                      # с передачей аргументом номера кнопки

dictonary = getWordsFromFile()

startNewRound()

root.mainloop()
