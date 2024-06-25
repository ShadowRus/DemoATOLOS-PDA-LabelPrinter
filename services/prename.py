import re
from collections import Counter


def clean_name(name):
    # Очистить название от спецсимволов и привести к нижнему регистру
    return re.sub(r'[^A-Za-zА-Яа-я0-9\s]', '', name).strip().lower()


def get_most_common_words(names):
    # Получаем все слова по всем именам и находим самые частые слова (предположительно ключевые)
    words = []
    for name in names:
        cleaned_name = clean_name(name)
        words.extend(cleaned_name.split())

    word_counts = Counter(words)
    most_common_words = [word for word, count in word_counts.most_common(5)]  # 5 самых частых слов

    return most_common_words


def is_valid_name(name, common_words):
    cleaned_name = clean_name(name)

    # Проверяем если в названии хотя бы половина из самых частых слов
    count_matches = sum(1 for word in common_words if word in cleaned_name.split())

    return count_matches >= len(common_words) // 2 + 1


def select_valid_name(names):
    common_words = get_most_common_words(names)

    valid_names = [name for name in names if is_valid_name(name, common_words)]

    if not valid_names:
        return None

    # Выбираем название с минимальной длиной после очистки
    best_names = min(valid_names, key=lambda x: len(clean_name(x)))

    return best_names
