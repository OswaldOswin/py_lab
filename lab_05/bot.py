import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    print(url)
    return web_page


def parse_schedule_for_a_day(web_page, day_number: str):
    soup = BeautifulSoup(web_page, "html5lib")
    schedule_table = soup.find("table", attrs={"id": day_number + "day"})

    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ", " + room.dd.text for room in locations_list]

    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def parse_lesson(web_page, day_number: str, para_number: int):
    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": day_number + "day"})

    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ", " + room.dd.text for room in locations_list]

    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    paras = {1: '8:20-9:50',
    2: '10:00-11:30',
    3: '11:40-13:10',
    4: '13:30-15:00',
    5: '15:20-16:50',
    6: '17:00-18:30',
    7: '18:40-20:10'}

    for i in range(len(times_list)):
        if times_list[i] == paras[para_number]:
            return times_list[i], locations_list[i], lessons_list[i]


def get_resp_for_a_day(web_page, day_number: str):
    times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(web_page, day_number)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>,  {}, {}\n'.format(time, location, lesson)
    return resp


def get_resp_for_a_lesson(web_page, day_number: str, para_number: int):
    time, location, lesson = parse_lesson(web_page, day_number, para_number)
    resp = ''
    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    return resp


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    a = message.text.split()
    if len(a) == 3:
        day, group, week = a
    else:
        day, group = a
        week = ''
    web_page = get_page(group, week)
    if day == "/monday":
        day_number = "1"
    elif day == "/tuesday":
        day_number = "2"
    elif day == "/wednesday":
        day_number = "3"
    elif day == "/thursday":
        day_number = "4"
    elif day == "/friday":
        day_number = "5"
    elif day == "/saturday":
        day_number = "6"
    elif day == "/sunday":
        day_number = "7"

    bot.send_message(message.chat.id, get_resp_for_a_day(web_page, day_number), parse_mode='HTML')


@bot.message_handler(commands=['near', 'next'])
def get_near_lesson(message):
    group = message.text.split()[1]
    week = datetime.date.today().isocalendar()[1]
    if week % 2 == 1:
        week = 2
    else:
        week == 1
    web_page = get_page(group, week)
    day_number = str(datetime.datetime.today().weekday() + 1)
    time = datetime.datetime.now().time()
    if time > datetime.time(18, 40, 0):
        day_number = str(int(day_number) + 1)
        para_number = 1
    elif time > datetime.time(17, 00, 0):
        para_number = 7
    elif time > datetime.time(15, 20, 0):
        para_number = 6
    elif time > datetime.time(13, 30, 0):
        para_number = 5
    elif time > datetime.time(11, 40, 0):
        para_number = 4
    elif time > datetime.time(10, 00, 0):
        para_number = 3
    elif time > datetime.time(8, 20, 0):
        para_number = 2
    print(web_page)
    print(group, week, para_number, day_number)
    while parse_lesson(web_page, day_number, para_number) is None:
        if para_number < 7:
            para_number += 1
        else:
            para_number = 1
            day_number = str(int(day_number) + 1)
    bot.send_message(message.chat.id, get_resp_for_a_lesson(web_page, day_number, para_number), parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
