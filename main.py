from _signal import pause
from time import sleep

from keras import Sequential
from keras.preprocessing.text import Tokenizer, text_to_word_sequence

import dataConverter
from InputData import InputData
from PlotDrawer import draw
from data_cleaner import text_cleaner

from neural_nets.convNN import func1
from neural_nets.nn import func

word_not_in_texts = list()
word_not_in_texts.append("кукусики")

file = open('./data/Trump_240_2.txt', 'r')
file.readline()
data = list()
texts = list()
dataElem = InputData()
X_train = list()
y_train = list()

X_test = list()
y_test = list()

i = 1

# data1 = dataConverter.read_data(1)
# data2 = dataConverter.read_data(2)
#
# for i in range(3000):
#     X_train.append(data1[i].text)
#     X_train.append(data2[i].text)
#     y_train.append(data1[i].mark)
#     y_train.append(data2[i].mark)
#
# for j in range(900):
#     i = 3001 + j
#     X_test.append(data1[i].text)
#     X_test.append(data2[i].text)
#     y_test.append(data1[i].mark)
#     y_test.append(data2[i].mark)

for line in file:
    if i < 200:
        elems = line.split("\t")
        dataElem.setNum(int(elems[0].replace(" ", "")))
        dataElem.setText(text_cleaner(elems[1]))
        dataElem.setMark(int(elems[2]))
        if dataElem.mark != 3:
            X_train.append(dataElem.text)
            y_train.append(dataElem.mark)
        data.append(dataElem)
        # выводим элемент входных данных
        print(dataElem)
        dataElem = InputData()
    else:
        elems = line.split("\t")
        dataElem.setNum(int(elems[0].replace(" ", "")))
        dataElem.setText(text_cleaner(elems[1]))
        dataElem.setMark(int(elems[2]))
        if dataElem.mark != 3:
            X_test.append(dataElem.text)
            y_test.append(dataElem.mark)
        data.append(dataElem)
        # выводим элемент входных данных
        print(dataElem)
        dataElem = InputData()
    i = i + 1
total_texts = list.copy(X_train)
total_texts.extend(X_test)
total_texts.extend(word_not_in_texts)

fileRaw = open('./data/Trump_texts.txt', 'r')
raw_strings = list()
for line in fileRaw:
    raw_strings.append(text_cleaner(line))

tokenizer = Tokenizer()
tokenizer.fit_on_texts(total_texts)

word2id = tokenizer.word_index
id2word = {v: k for k, v in word2id.items()}

xtr = list()
for q in X_train:
    xtr.append(list(word2id[w] for w in text_to_word_sequence(q)))

xts = list()
for q in X_test:
    xts.append(list(word2id[w] for w in text_to_word_sequence(q)))

predict = list()
# for q in raw_strings:
#     l = list()
#     for w in text_to_word_sequence(q):
#         if w in word2id.keys():
#             l.append(word2id[w])
#         else:
#             l.append(word2id[word_not_in_texts[0]])
#     predict.append(l)
predict = list.copy(xtr)
predict.extend(xts)

right_answers = list.copy(y_train)
right_answers.extend(y_test)

x = []
y1 = []
y2 = []
for ep in [1, 2, 3, 4, 5, 8, 10, 12, 15, 20, 25]:
    answ1 = func1(xtr, y_train, xts, y_test, predict, ep)
    answ = func(xtr, y_train, xts, y_test, predict, ep)

    common = 0
    diff = 0

    r1 = 0
    w1 = 0

    r2 = 0
    w2 = 0

    for i in range(len(answ)):
        a = answ[i]
        b = answ1[i]
        r = right_answers[i]
        if a == b:
            common += 1
        else:
            diff += 1

        if a == r:
            r1 += 1
        else:
            w1 += 1

        if b == r:
            r2 += 1
        else:
            w2 += 1
    x.append(ep)
    y1.append(r1 * 100 / (r1 + w1))
    y2.append(r2 * 100 / (r2 + w2))
    print("Количество эпох: " + str(ep) + "\n")
    print("Число одинаковых ответов, полученных двумя сетями: " + str(common))
    print("Число разных ответов, полученных двумя сетями:" + str(diff))

    print("Число правильных ответов в сверточной сети: " + str(r1))
    print("Число неправильных ответов в сверточной сети: " + str(w1))

    print("Число правильных ответов в рекурентной сети: " + str(r2))
    print("Число неправильных ответов в рекурентной сети: " + str(w2))
    print("-----------------------------------------------------------------")

draw(x, y1, y2)

