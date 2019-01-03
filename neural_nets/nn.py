# Just disables the warning, doesn't enable AVX/FMA
import os

import keras
import numpy as np
from keras.utils import to_categorical

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.layers import Dense, Embedding, Dropout
from keras.layers import LSTM, SpatialDropout1D
from keras.models import Sequential
from keras.preprocessing import sequence

# Устанавливаем seed для повторяемости результатов
np.random.seed(42)
# Максимальное количество слов (по частоте использования)
max_features = 500000
# Максимальная длина статьи в словах
maxlen = 500


def func(x1, y1, x2, y2, predict, ep=25):
    # Загружаем данные
    (X_train, y_train), (X_test, y_test) = (x1, y1), (x2, y2)

    # Заполняем или обрезаем рецензии
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
    predict = sequence.pad_sequences(predict, maxlen=maxlen)

    # Создаем сеть
    model = Sequential()
    # Слой для векторного представления слов
    model.add(Embedding(max_features, 32))
    model.add(SpatialDropout1D(0.25))
    # Слой долго-краткосрочной памяти
    model.add(LSTM(128, dropout=0.25, recurrent_dropout=0.25))
    # Полносвязный слой
    model.add(Dense(3, activation="softmax"))
    # Копмилируем модель
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Обучаем модель
    model.fit(X_train, to_categorical(y_train, num_classes=3), batch_size=8, epochs=ep,
              validation_data=(X_test, to_categorical(y_test, 3)), verbose=1)

    # Проверяем качество обучения на тестовых данных
    scores = model.evaluate(X_test, to_categorical(y_test, num_classes=3),
                            batch_size=8)
    print("Точность на тестовых данных: %.2f%%" % (scores[1] * 100))

    res = model.predict(predict, batch_size=1)
    answ = []
    i = 1
    for el in res:
        maxelem = max(el)
        print(str(i) + " = " + str(el) + ", mark " + str(list(el).index(maxelem)))
        answ.append(list(el).index(maxelem))
        i += 1

    return answ
