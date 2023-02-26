from django import template


register = template.Library()


forbidden_words = ["ишак",
                   "Ишак",
                   "лошадь",
                   "Лошадь",
                   "Осел",
                   "осел",
                   "Осёл",
                   "осёл",
                   "Козел",
                   "козел",
                   "Козёл",
                   "козёл",
]                                # Список. Искомые слова. Дополняемый новыми словами


@register.filter                                # Примечание. Данный фильтр не работает,
def hide_forbidden(value):                      # если к слову "примыкает" знак препинания! (т.е. запятая или точка)
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)


# Код ниже делал в рамках работы по созданию собственного фильтра в одном из прошлых модулей

# dict1 = {                                 # Словарь Цензор. Искомые слова и их длина. Дополняемый новыми словами
#     "ишак": 4,
#     "Ишак": 4,
#     "лошадь": 6,
#     "Лошадь": 6
# }


# @register.filter()
# def censor(text, dict_censor=None):
#     if dict_censor is None:
#         dict_censor = dict1
#     if type(text) != str:               # Проверка строкового типа. Вызов исключения при попытке применения не к строке
#         raise ValueError
#     length = len(text)
#     for word in dict_censor:              # Цикл, для перебора слов (ключей) из словаря Цензор
#         index = 0
#         while index < length:             # Цикл для поиска вхождения текущего слова в строку и определение его индекса
#             i = text.find(word, index)
#             if i == -1:
#                 break
#             else:
#                 print(i)
#                 for j in range(i+1, i + dict_censor[word]):
#                     text = text[:j] + "*" + text[j + 1:]
#             index = i + 1
#     return text
