import requests
import json
import pytest

link = 'https://regions-test.2gis.com/1.0/regions'
link_page = 'https://regions-test.2gis.com/1.0/regions?page=1'

@pytest.fixture # объявляем фикстуру
def start_request(): # пишем функцию, на действия которые будут повторяться в каждом тесте, чтобы не дублировать код, и будем
    # передавать эту функцию в качестве аргумента в те тесты, в которых будет нужен ответ сервера в формате json
    print('start request...') # принт, который говорит о том, что тест стартовал
    doc = requests.get(link).text# при помощи библиотеки requests отправляем запрос на url который храниться в переменной link
    # далее в этой же строчке применяем .text - это переведет результат ответа сервера в тип данных str и и положим весь
    # обработанный ответ в переменную doc
    doc = json.loads(doc)# теперь, при помощи библиотеки json и метода loads(), приведем doc к типу dict, для того, чтобы было
    # удобнее перебирать и доставать нужные ключи и значения из ответа сервера
    return doc # возвращаем нашей функцией готовый к работе doc типа данных dict

@pytest.fixture # объявляем фикстуру
def list_items():# функция которая будет проходить по всем значениям параметра "page" до тех пор пока в ответе значение ключа
# "items" не будет пустым
# и собирать в список значения "country":{"code:__}
    res = []# результирующий список, куда будут вносится все country_code
    count = 1 # счетчик для перебора параметра "page" по требованиям минимальное значение = 1
    req = requests.get('https://regions-test.2gis.com/1.0/regions?page={}'.format(count)).text #заполняем переменную "req" первым запросом
    #чтобы она не была пустой и выполнились условия цикла 27 строчки
    req = json.loads(req)# приводим req к типу данных dict
    while len(req['items'])!=0:# запускаем цикл который будет итерироваться до тех пор пока в ключе 'items' нашего запроса не придет пустой
        # список
        req = requests.get('https://regions-test.2gis.com/1.0/regions?page={}'.format(count)).text# подставляем в url переменную count
        req = json.loads(req)# приводим "req" к типу dict
        for i in range(len(req['items'])):# перебираем все элементы списка "req[items]"
            res.append(req["items"][i]['name'] + "|" + req['items'][i]['country']['code'])# и складываем их в результирующий список res
        count+=1# инкреминтируем счетчик
    return res # возвращаем результирующий список