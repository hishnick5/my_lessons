"""Игра угадай число
Компьютер сам загадывает и сам угадывает число
"""

import numpy as np

def random_predict(number: int = 1) -> int:
    """Рандомно угадываем число

    Args:
        number (int, optional): Загаданное число. Поумолчанию равно 1.

    Returns:
        int: Возвращаем число попыток
    """
    count = 0 # Подсчёт колличества попыток

    while True:
        count += 1
        predict_number = np.random.randint(1, 101)  # Задываем рандомное число
        if number == predict_number: # Проверяем если угадали число
            break  # Выход из цикла если угадали
    return count # Возвращаем колличество попыток

def score_game(random_predict) -> int:
    """За какое количество попыток в среднем за 1000 подходов угадывает наш алгоритм

    Args:
        random_predict ([type]): функция угадывания

    Returns:
        int: среднее количество попыток
    """
    count_ls = [] #Готовим список для предугаданных попыток
    
    np.random.seed(1)  # фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=(1000))  # загадали массив рандомных чисел

    for number in random_array: # Циклом пройдемся по каждому числу из массива
        count_ls.append(random_predict(number)) # И добавим в список число попыток угаданного числа

    score = int(np.mean(count_ls)) # Получаем результат среднего значения 
    print(f"Ваш алгоритм угадывает число в среднем за:{score} попыток")
    return score # Возвращаем результат


if __name__ == "__main__": # Прописываем условие для возможности импорта
    # RUN
    score_game(random_predict)
