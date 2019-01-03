import json
import os

from InputData import InputData


def read_data(q):
    result = []
    direct = './data/' + str(q)
    files = os.listdir(direct)

    # res_file = open(direct + "/res2", 'w')
    count = len(files)
    i = 1

    for file in files:
        if i < 4000:
            try:
                if i % 100 == 0:
                    print(str(i) + "/" + str(count))
                f = open(direct + "/" + file, "r")
                s = ""
                for line in f:
                    s += line

                obj = json.loads(s)
                dataElem = InputData()
                dataElem.setNum(i)
                text = (str(obj['text']).replace('\n', ''))
                text = text.replace('  ', ' ')
                text = text.lower()

                # оставляем в предложении только русские буквы (таким образом
                # удалим и ссылки, и имена пользователей, и пунктуацию и т.д.)
                alph = 'qwertyuiopasdfghjklzxcvbnm'

                cleaned_text = ''
                for char in text:
                    if (char.isalpha() and char[0] in alph) or (char == ' '):
                        cleaned_text += char
                dataElem.setText(cleaned_text)
                dataElem.setMark(int(q - 1))
                result.append(dataElem)

                i += 1
            except Exception:
                print("shit happens")
    return result

# file1 = open("./data/res1", 'r')
# file2 = open("./data/res2", 'r')
#
# file = open("./data/res", 'w')
# i = 1
# for line in file1:
#     if i % 100 == 0:
#         print(str(i) + "/22000")
#     file.writelines(line)
#     s = file2.readline()
#     file.writelines(s)
#     s = file2.readline()
#     file.writelines(s)
#     i += 1
# file.close()
