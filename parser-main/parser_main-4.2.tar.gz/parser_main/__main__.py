import parser_module.parser_2_3 as parser_2_3
import parser_module.wiki as wiki
import parser_module.parser_12_13 as parser_12_13
import parser_module.parser_14_15 as parser_14_15
import parser_module.parser_16 as parser_16
import parser_module.parser_19 as parser_19
import parser_module.parser_21 as parser_21
import parser_module.parser_24 as parser_24
import parser_module.parser_28 as parser_28
import parser_module.parser_29_30 as parser_29_30
import parser_module.parser_34_36 as parser_34_36
import parser_module.parser_38_41 as parser_38_41
import time
import parser_libraries.SQL as SQL

# Оболочка выполнения каждого парсера, проверка на ошибки
def decore(fn, arg=None, cont_id=None, cont_work=None):
    def wrapper():
        sleep_Time = 2
        while sleep_Time < 600 and sleep_Time != 1:
            print('Script starts working')
            if arg == None:
                people = fn()
            elif cont_id == None:
                people = fn(arg)
            else:
                people = fn(arg, cont_id=cont_id, cont_id_work=cont_work)
            print('Script stopped working')
            try:
                a = people[0]['bday']
                sleep_Time = 1
                return people
            except KeyError:
                print('Error ' + str(people[-1]['code']) + '.\nCorruption while executing ' + people[-1]['script'])
                if people[-1]['code'] == 1:
                    print('Corruption while parsing.')
                    sleep_Time += 1
                    print(f'Trying to reconnect in {sleep_Time} seconds')
                    time.sleep(sleep_Time)
                else:
                    print('Access denied by server.')
                    sleep_Time += 5
                    print(f'Trying to reconnect in {sleep_Time} seconds')
                    time.sleep(sleep_Time)
                    print('\n')
        if sleep_Time != 1:
            print('Connection denied for a while, stopped working.')
    return wrapper


# Отработка всех скриптов
def __main__():
    people = []
    func = decore(parser_19.parser)
    people.extend(func())
    func = decore(wiki.parser,
                  arg='https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%B5%D0%B7%D0%B8%D0%B4%D0%B5%D0%BD%D1%82_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8')
    people.extend(func())
    func = decore(parser_2_3.parser)
    people.extend(func())
    func = decore(parser_12_13.parser)
    people.extend(func())
    func = decore(parser_14_15.parser)
    people.extend(func())
    func = decore(parser_16.parser)
    people.extend(func())
    func = decore(parser_21.parser)
    people.extend(func())
    func = decore(parser_24.parser)
    people.extend(func())
    func = decore(wiki.parser,
                  arg='https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%BF%D1%80%D0%BE%D0%BA%D1%83%D1%80%D0%BE%D1%80_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8')
    people.extend(func())
    func = decore(parser_28.parser)
    people.extend(func())
    func = decore(parser_29_30.parser)
    people.extend(func())
    func = decore(wiki.parser, arg='https://ru.wikipedia.org/wiki/%D0%A3%D0%BF%D0%BE%D0%BB%D0%BD%D0%BE%D0%BC%D0%BE%D1%87%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BF%D0%BE_%D0%BF%D1%80%D0%B0%D0%B2%D0%B0%D0%BC_%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA%D0%B0_%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8')
    people.extend(func())
    func = decore(wiki.parser, arg='https://ru.wikipedia.org/wiki/%D0%A3%D0%BF%D0%BE%D0%BB%D0%BD%D0%BE%D0%BC%D0%BE%D1%87%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BF%D0%BE_%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B5_%D0%BF%D1%80%D0%B0%D0%B2_%D0%BF%D1%80%D0%B5%D0%B4%D0%BF%D1%80%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9_%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8')
    people.extend(func())
    func = decore(parser_34_36.parser)
    people.extend(func())
    func = decore(wiki.parser, arg='https://ru.wikipedia.org/wiki/%D0%91%D0%B0%D0%BD%D0%BA_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8', cont_id=6, cont_work=37)
    people.extend(func())
    func = decore(parser_38_41.parser)
    people.extend(func())
    SQL.mySQL_save(people)


__main__()