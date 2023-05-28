import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import requests
from myconfig import TOKEN, chain, address

vk_session = vk_api.VkApi(
    token=TOKEN)
vk = vk_session.get_api()

if chain == 'POLYGON':
    val = 'MATIC'
if chain == 'ETHEREUM':
    val = 'ETH'
if chain == 'FLOW':
    val = 'FLOW'
if chain == 'POLYGON':
    val = 'MATIC'

urlr = f'https://api.rarible.org/v0.1/data/collections/{chain}:{address}/floorPrice?currency={val}'


def sendmessage(event, text, kboard=None):
    if kboard:
        vk.messages.send(user_id=event.user_id,
                         message=text,
                         random_id=random.randint(0, 100000),
                         keyboard=kboard.get_keyboard())
    else:
        vk.messages.send(user_id=event.user_id,
                         message=text,
                         random_id=random.randint(0, 100000))


longpoll = VkLongPoll(vk_session)

go_back = False
celp = None
agep = None
genp = None

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print(event.text)
        if event.text == '/флор' or event.text == '/Флор' or event.text == '/akjh' or event.text == '/Akjh':
            request = requests.get(urlr).json()
            actual_floor = round(float(request['currentValue']), 2)
            yesterday_floor = request['historicalValues'][-1]
            ayesterday_floor = request['historicalValues'][-2]
            kboard = VkKeyboard(inline=True)
            kboard.add_openlink_button('Rarible', 'https://rarible.com/')
            kboard.add_openlink_button('Opensea', 'https://opensea.io/')
            sendmessage(event, f'''📈 Актуальный флор коллекции: {actual_floor} MATIC
            
Флор вчера: {yesterday_floor} MATIC
Флор позавчера: {ayesterday_floor} MATIC


''', kboard)

        text = event.text
        print(text)
        if text == 'Начать':
            sendmessage(event, 'Здравствуйте, это бот магазина "Pichshop"!')
            go_back = True

        #
        # elif text == 'Товары':
        #     sendmessage(event, 'Все товары наши товары, имеющиеся в наличии:')
        #     #res = cursor.execute('''SELECT * FROM goods''').fetchall()
        #     txt = ''
        #     for i in res:
        #         txt = f'''{i[0]}
        #                 Наличие: {i[1]}
        #                 Цена: {i[2]} руб.
        #                 Ссылка: {i[5]}
        #                 '''
        #
        #         sendmessage(event, txt)
        #     go_back = True
        #
        # cels = ['День рождения', 'Свадьба', 'День защитника отечества', '8 марта', 'Новый год']
        # if text == 'Подбор подарка':
        #     cel_kboard = VkKeyboard(one_time=True)
        #     count = 1
        #     for cel in cels:
        #         cel_kboard.add_button(cel, VkKeyboardColor.SECONDARY)
        #         if count != 2:
        #             count += 1
        #         else:
        #             cel_kboard.add_line()
        #             count = 1
        #     cel_kboard.add_line()
        #     cel_kboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        #     sendmessage(event, 'Выберите праздник', cel_kboard)
        # ages = ['0-14', '15-29', '30-49', '50-69', '70-100']
        #
        # if text in cels and text != '8 марта' and text != 'День защитника отечества' and text != 'Свадьба':
        #     celp = text.replace(' ', '_')
        #
        #     gift_kboard = VkKeyboard(one_time=True)
        #
        #     counter = 0
        #     for age in ages:
        #         gift_kboard.add_button(age, VkKeyboardColor.SECONDARY)
        #         if counter != 4:
        #             counter += 1
        #         else:
        #             gift_kboard.add_line()
        #             counter = 0
        #     gift_kboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        #     sendmessage(event, 'Выберите возраст', gift_kboard)
        #
        # if text in ages:
        #     agep = text
        #     male_or_fmale_kboard = VkKeyboard(one_time=True)
        #     male_or_fmale_kboard.add_button('Мужской', VkKeyboardColor.POSITIVE)
        #     male_or_fmale_kboard.add_line()
        #     male_or_fmale_kboard.add_button('Женский', VkKeyboardColor.POSITIVE)
        #     male_or_fmale_kboard.add_line()
        #     male_or_fmale_kboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        #     sendmessage(event, 'Выберите пол', male_or_fmale_kboard)
        #
        # if text == 'Мужской' or text == 'Женский':
        #     genp = text
        #     if celp and agep and genp:
        #         if agep == '0-14':
        #             #res = cursor.execute(f'''SELECT * FROM goods
        #             #                         WHERE cel = '{celp}' AND age = '{agep}' ''').fetchall()
        #             if len(res) != 1:
        #                 sendmessage(event, f'Нашлось {len(res)} наиболее подходящих варианта(-ов):')
        #             else:
        #                 sendmessage(event, f'Нашёлся {len(res)} наиболее подходящий вариант:')
        #             txt = ''
        #             for i in res:
        #                 txt = f'''{i[0]}
        #                         Наличие: {i[1]}
        #                         Цена: {i[2]} руб.
        #                         Ссылка: {i[5]}
        #                         '''
        #                 sendmessage(event, txt)
        #
        #         else:
        #             #res = cursor.execute(f'''SELECT * FROM goods
        #                                      WHERE cel = '{celp}' AND age = '{agep}' AND gender = '{genp}' ''').fetchall()
        #             if len(res) != 1:
        #                 sendmessage(event, f'Нашлось {len(res)} наиболее подходящих варианта(-ов):')
        #             else:
        #                 sendmessage(event, f'Нашёлся {len(res)} наиболее подходящий вариант:')
        #             txt = ''
        #             for i in res:
        #                 txt = f'''{i[0]}
        #                         Наличие: {i[1]}
        #                         Цена: {i[2]} руб.
        #                         Ссылка: {i[5]}
        #                         '''
        #                 sendmessage(event, txt)
        #
        #         celp, agep, genp = None, None, None
        #         go_back = True
        #
        # if text == 'День защитника отечества':
        #     res = cursor.execute('''SELECT * FROM goods
        #                              WHERE cel = '23' ''').fetchall()
        #     if len(res) != 1:
        #         sendmessage(event, f'Нашлось {len(res)} наиболее подходящих варианта(ов):')
        #     else:
        #         sendmessage(event, f'Нашёлся {len(res)} наиболее подходящий вариант:')
        #     txt = ''
        #     for i in res:
        #         txt = f'''{i[0]}
        #             Наличие: {i[1]}
        #             Цена: {i[2]} руб.
        #             Ссылка: {i[5]}
        #             '''
        #
        #         sendmessage(event, txt)
        #     go_back = True
        #
        # if text == '8 марта':
        #     res = cursor.execute('''SELECT * FROM goods
        #                              WHERE cel = '8' ''').fetchall()
        #     if len(res) != 1:
        #         sendmessage(event, f'Нашлось {len(res)} наиболее подходящих варианта(ов):')
        #     else:
        #         sendmessage(event, f'Нашёлся {len(res)} наиболее подходящий вариант:')
        #     txt = ''
        #     for i in res:
        #         txt = f'''{i[0]}
        #                 Наличие: {i[1]}
        #                 Цена: {i[2]} руб.
        #                 Ссылка: {i[5]}
        #                 '''
        #
        #         sendmessage(event, txt)
        #     go_back = True
        # if text == 'Свадьба':
        #     res = cursor.execute('''SELECT * FROM goods
        #                              WHERE cel = 'mr' ''').fetchall()
        #     if len(res) != 1:
        #         sendmessage(event, f'Нашлось {len(res)} наиболее подходящих варианта(ов):')
        #     else:
        #         sendmessage(event, f'Нашёлся {len(res)} наиболее подходящий вариант:')
        #     txt = ''
        #     for i in res:
        #         txt = f'''{i[0]}
        #                 Наличие: {i[1]}
        #                 Цена: {i[2]} руб.
        #                 Ссылка: {i[5]}
        #                 '''
        #
        #         sendmessage(event, txt)
        #
        #     go_back = True
        #
        #
        #
        # if go_back:
        #     keyboard = VkKeyboard(one_time=True)
        #     keyboard.add_button('Товары', VkKeyboardColor.PRIMARY)
        #     keyboard.add_line()
        #     keyboard.add_button('Подбор подарка', VkKeyboardColor.POSITIVE)
        #     keyboard.add_line()
        #     keyboard.add_button('Контакты', VkKeyboardColor.NEGATIVE)
        #     keyboard.add_openlink_button('Сайт', 'https://www.pichshop.ru/')
        #     sendmessage(event, 'Выберите желаемое действие в меню', keyboard)
        #     go_back = False
