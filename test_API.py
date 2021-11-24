import requests
import json
import pytest

link = 'https://regions-test.2gis.com/1.0/regions'
link_page = 'https://regions-test.2gis.com/1.0/regions?page=1'

def list_only_items():# функция , которая собирает список всех городов, который дает API
    res = []# пустой список в который будут записываться регионы
    i = 1 # переменная для значения query параметра в запросе, которую будем инкрементировать
    while True: # цикл в котором проходим по всем данным с номерами page, пока список в ответе не придет пустым
        resp = requests.get('https://regions-test.2gis.com/1.0/regions?page={}'.format(i)).text
        resp = json.loads(resp)
        if len(resp['items'])==0:
            break
        for j in range(len(resp['items'])):
            res.append(resp['items'][j]['name'])
        i+=1
    return res

class Test_get_regions_default():# объявляем тестовый класс в котором будем проверять данные в ответе сервера с параметрами "по умолчанию"

    def test_quantity_total_regions(self, start_request):

        assert start_request['total'] == 22

    #===ТЕСТ-КЕЙС 1.0 https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit?usp=sharing===
    def test_quantity_page_size_default(self, start_request):# тест с проверкой количества элементов с параметром "page_size" по умолчанию
        # в качестве аргумента передаем в тестовый метод фикстуру "start_request" которая возвращает ответ сервера в формате dict
        length_items = start_request['items'] # в переменную "length_items" передаем значение ключа "items" из нашего запроса
        # внимание!!! значение ключа "items" имеет тип данных list
        assert len(length_items) == 15, 'количество регионов не соответствует требованию по умолчанию = {}'.format(len(length_items))
        # в строке 31 делаем проверку которая сравнивает количество элементов в "length_items" и количество элементов, которое должно быть
        # с параметрами запроса "по умолчанию"



    #===ТЕСТ-КЕЙС 1.1 https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit?usp=sharing===
    def test_page_number_default(self, start_request):#тест который проверяет соответствие элементов в ответе с параметрами "по умолчанию"
        # и с параметром "page=1" так как в требованиях с параметрами запроса "по умолчанию" должен отобразиться ответ соответствующий
        # ответу с параметром "page" ==1
        page_1 = requests.get(link_page).text# получаем ответ на запрос с параметром "page" = 1
        page_1 = json.loads(page_1) # приводим этот ответ к типу dict
        assert page_1 == start_request, 'значения "items" с параметром "page=1", не соответствует "items" по умолчанию...'
        #  строке 40 сравниваем результат ответа с парамеиром "page" = 1  и ответ с параметрами "по умолчанию"



    #===ТЕСТ-КЕЙС 1.2 https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit?usp=sharing===
    def test_show_default_country_code(self, list_items): # тест который проверяет, что при отправке запроса  с параметрами"по умолчанию"
        # отображаются 'country_code' разных стран
        # list_items - полный список регионов с параметрами country_code по умолчанию
        res = False# переменная, которая хранит результат для assert, если проверка будет удачной изменится на True
        for i in range(len(list_items)):# цикл который берет первый элемент из списка и поочередно сравнивает его со всеми остальными
            if list_items[0] == list_items[i]:# если первый элемент списка равен i-тому элементу этого же списка, то
                # уходим на следующую итерацию
                continue
            else:# если же первый элемент списка  list_items отличается от остальных этого же списка, то
                res = True# результат для assert принимает значение True
                break# выходим из цикла и выводим результат проверки
        assert res, 'ОШИБКА!!! при запросе с параметрами "по умолчанию" в значениях ключа "items", одинаковые "country_code" {}'.format(list_items)



    #===ТЕСТ-КЕЙС 3.1 https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit?usp=sharing===
    def test_unique_items_default(self, list_items):# тест проверяет общий список регионов в ответе сервера на уникальность
        res = {} # dict для хранения количества повторений регионов
        err = [] # список регионов которые не уникальны(повторяются 2 и более раза)

        while len(list_items) > 0: # цикл который проходит по списку list_items
            if list_items[0] in res.keys():# если ключ list_items[0] есть в списке, то
                res[list_items[0]] += 1# инкрементируем количество регионов в словаре "res"
            else:# если же такого ключа нет в словаре, то
                res[list_items[0]] = 1 # добавляем этот ключ в словарь res со значением 1
            if res[list_items[0]] > 1: # если по ключу list_items[0] более 1 региона, то
                err.append(list_items[0]) # вносим этот ключ в список "err"
            list_items.remove(list_items[0]) # удаляем текущий list_items[0]
        assert len(err) == 0, 'регионы {} не уникальны в общем списке регионов'.format(err) # если список с ошибками пуст - тест пройден
        # если в списке "err" есть элементы, то тест провален и выводится список регионов, которые не уникальны



    #===ТЕСТ-КЕЙС 2.0 https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit?usp=sharing===
    @pytest.mark.parametrize('page_size', [5, 10, 15])
    def test_page_size(self, page_size):# Проверка количества возвращаемых в ответе регионов с параметрами page_size:5,10,15
        i = 1 # переменная для хранения значений query параметра "page"
        final = True # результирующая переменная для assert

        while True:# в цикле перебираем ответы изменяя параметры, пока не придет ответ с пустым списком
            link = 'https://regions-test.2gis.com/1.0/regions?page={}&page_size={}'.format(i, page_size)#формируем динамические параметры
            # в url
            resp = requests.get(link).text# получаем ответ
            resp = json.loads(resp)# приводим его к типу dict
            if len(resp['items']) == page_size:# если в ответе длина списка равна page_size из параметров url то
                final = True # результирующая переменная True - все идет по плану:))
                i+=1# инкрементируем счетчик параметра page
            elif len(resp['items']) > page_size:# но если длина списка больше чем указано в параметре переменной page_size то
                break# покидаем цикл, НЕ ИНКРЕМЕНТИРУЯ счетчик параметра i
            else:# если же длинна списка в ответе меньше чем параметр page_size
                i+=1 # инкрементируем счетчик страниц, для того чтобы удостовериться, что следующая страница пустая,
                break# покидаем цикл
        link = 'https://regions-test.2gis.com/1.0/regions?page={}&page_size={}'.format(i, page_size)# формируем url для финальной проверки
        resp = requests.get(link).text
        resp = json.loads(resp)
        if len(resp['items'])==0:# если с текущим парметром page приходит ответ с пустым списком то
            final = True# все отлично идем на assert
        else:# если же в списке есть регионы
            final = False# ломаем assert
            i -= 1 # и декрементируем переменную на ту страницу, где найдена ошибка
        assert final == True, 'в ответе к запросу с параметром {}, не верное количество регионов на странице номер {} '.format(page_size, i)


    # =====Тест-кейс 5.0=====https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit#gid=2009304920
    f_l_i = list_only_items()# скрипт для получения полного списка регионов
    @pytest.mark.parametrize('full_list_items', f_l_i)# в параметризации указываем переменную со списком регионов, которые мы будем
    # подставлять по одному в качестве query параметра в url
    def test_q_search_with_valid_data(self, full_list_items):# тест, который проверяет как работает нечеткий поиск по полному имени региона
        link = 'https://regions-test.2gis.com/1.0/regions?q={}'.format(full_list_items)# в переменную передаем url с query параметром
        # в качестве подстроки url используем полное имя региона
        resp = requests.get(link).text # отправляем запрос и в переменную resp помещаем ответ типа str
        resp = json.loads(resp)# приводим resp к dict
        result = True# результирующая переменная для assert
        try:# обрабатываем исключения в случае отсутствия региона в списке после фильтрации по ПОЛНОМУ ИМЕНИ
            if resp['items']==[]:# если запрос с query параметром из действующего списка не вернул нам искомый регион, то
                result = False # то проверка провалена - и результирующая переменная стала False
            elif full_list_items in resp['items'][0]['name']:# если все в порядке и поиск отработал корректно
                result = True# результирующая переменная True
        except Exception:# в случае пустого списка items в ответе
            result=False# результирующую переменную делаем False
        assert result==True, 'Ошибка, региона-{}, нет в отфильтрованном списке регионов'.format(full_list_items)# если тест упал, то в сообщении будет
        # напечатано на каком именно элементе списка упал тест
# ===Тест-кейс 4.0====== https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit#gid=2009304920
    @pytest.mark.parametrize('country_code_list', ['ru', 'kz', 'kg', 'cz']) # В параметризации задаем список регионов для query параметра
    def test_country_code_valid_data(self, country_code_list):# Тест на проверку рабрты фильтра по коду региона
        errList = []# Лист для сбора данных пришедших с ошибками
        link_c_c = 'https://regions-test.2gis.com/1.0/regions?country_code={}'.format(country_code_list)# Адрес с query параметром в качестве подстроки
        resp = requests.get(link_c_c).text# отправляем запрос и ответ приводим к str
        resp = json.loads(resp)# приводим ответ к dict
        for i in range(len(resp['items'])):# в цикле перебираем элементы ответа и
            if resp['items'][i]['country']['code']==country_code_list:# если в элементе ответа пришел такой же код как мы указали в фильтре
                continue# то все хорошо идем к следующему элементу
            else:# иначе
                errList.append(resp["items"][i]['name'] + "|" + resp['items'][i]['country']['code'])# записываем в список ошибок
                # неправильно отфильтровавшийся регион
        assert len(errList)==0, "При запросе регионов с фильтром по коду - {}, пришел ответ с кодом - {}".format(country_code_list,errList)
        # если список ошибок пуст, то тест прошел, если нет, то выводим сообщение об ошибке с перечислением регионов, которые неправильно
        # отфильтровались

    # ====Тест-кейс 4.1===== https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit#gid=2009304920
    @pytest.mark.parametrize('integer_list', [12, 0, -32]) # создаем фикстуру со списком чисел для проверки
    def test_country_code_integer(self, integer_list): # Тест, который проверяет, что сервер правильно обрабатывает запрос с числами и возвращает ошибку
        link_c_c = 'https://regions-test.2gis.com/1.0/regions?country_code={}'.format(integer_list)  # Адрес с query параметром в качестве подстроки
        resp = requests.get(link_c_c).text  # отправляем запрос и ответ приводим к str
        resp = json.loads(resp)  # приводим ответ к dict
        result = True# резулььтирующая переменная для assert
        try:# обрабатываем исключение для того, чтобы при неизвестной структуре json в ответе проверка не останавливалась из за KeyError
            if resp['error']['message']=="Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz":# если сообщение об ошибке
                # пришло в правильном формате
                result=True# то результирующая переменная ==True
            else:# иначе
                result=False# Результирующая переменная равна false
        except Exception:# если же структура ответа вызывает ошибку, то обработаем ее
            result=False# и сделаем результирующую переменную False

        assert result==True, 'Система неправильно обработала ошибку и вернула {}'.format(resp)
        # Сраввниваем ответ сервера с тем сообщением, которое должно придти. В случае не верного ответа - выводим ответ на экран.

# ===Тест-кейс 4.2=== https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit#gid=2009304920
    def test_regions_of_regionList(self, list_items):# Тест который проверяет, что в списке регионов только регионы ru, kg, kz, cz
        # передаем фактический список регионов и их кодов в качестве аргумента из фикстуры list_items
        list_code = {'ru':0, 'kz':0, 'kg':0, 'cz':0}# создаем словарь с регионами и их количеством
        errList=[]# создаем список для ошибок

        for i in range(len(list_items)):# в циклу проходим по всему фактическому списку регионов
            s = list_items[i].split('|')# так как каждый элемент в списке записан в формате <region>|<region_code> то сплитуем элемент по '|'
            # теперь код региона в списке под индексом [1]
            if s[1] in list_code.keys():# если код проверяемого региона из фактического списка есть в словаре
                list_code[s[1]]+=1# то инкрементируем значение этого кода региона
            else:# иначе если такого кода нет в проверочном списке
                errList.append(list_items[i])# то помещаем его в список с ошибками
        print(list_code.items())# распечатаем словарь чтобы показать сколько и каких регионов в списке
        assert  len(errList)==0, 'Среди списка регионов есть регионы, кодов которых нет в списке для проверки - {}'.format(errList)
        # Проверка на то, что в списке ошибок пусто. Если нет, то выведем список со всеми ошибками

    # ===Тест-кейс 4.3=== https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit#gid=2009304920
    def test_invalid_data_in_country_code(self):# тест который проверяет, что при отправке запроса с query параметром country_code=rus
        # сервер правильно обработает запрос и вернет верную ошибку
        invalid_str_country_code = 'rus'# переменная подстрока для query параметра запроса
        link='https://regions-test.2gis.com/1.0/regions?country_code={}'.format(invalid_str_country_code)# url для запроса городов по country_code
        resp = requests.get(link).text# ответ на запрос помещаем в переменную и приводим ее к str
        resp = json.loads(resp)# приводим ее далее к dict
        result = True # результирующая переменная для assert
        try:# обрабатываем исключение в случае возврата с сервера ответа в неизвестном формате или неизвестной структурой
            if resp['error']['message']=="Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz":# если с сервера
                # пришла ожидаемая ошибка
                result = True#  результирующая переменнная True
            else:# иначе
                result = False # результирующая переменная False
        except Exception:# В случае ошибки
            result=False # Результирующая переменная False

        assert result==True , "Ошибка с сервера приходит не в том формате. Должно быть {}, а пришло {}".format("Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz", resp)
        # Проверка на то что результирующая переменная True, либо сообщаем об ошибке и выводим ожидаемое и фактическое сообщение


        # ===Тест-кейс 3.0=== https://docs.google.com/spreadsheets/d/1M7ps9n-pd9Bq5X0pvwRYNsqgR18h14KerdusKW5XjWs/edit#gid=2009304920

