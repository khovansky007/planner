import pickle
import os, sys


sys.setrecursionlimit(1000000)

today = '31.07.2023' # need to parse info from google or use some lib

# data = {
#             '31.07.2023': [
#                 [0.40, 1.20, 'read book'], #дата: [время начала, время конца, задача]
#                 [1.1, None, 'take money']
#                 ] 
#         }

storage_filename = 'data.pickle'
def save_data(storage_filename, data={}, clear_data=False):
    if not os.path.exists(storage_filename): # Если файла не существует
        with open(storage_filename, "wb") as f: # То создаем его
            pickle.dump(data, f) # Сохрняя в него наш список
    elif data != {} or clear_data: # Если же существует
        with open(storage_filename, "wb") as f:
            pickle.dump(data, f) # Сохраняем измененный список в файл

def get_data(storage_filename):
    with open(storage_filename, "rb") as f:
        data = pickle.load(f) # То загружаем из него список
    return data



def handle_time(time):
    time = str(time).split('.')
    time_1 = time[0]
    time_2 = time[1]
    if len(time_2) != 2:
        time_2 += '0'
    return f"{time_1}:{time_2}"
    
def set_time(time: str):
    if time != None:
        time = time.split(':')
        time = int(time[0]) + int(time[1])/100
        return time
    else: return None

def set_task(text_task: str, date: str, time_start: str, time_end: str = None) -> None:
    global data
    if date in data:
        data[date].append([set_time(time_start), set_time(time_end), text_task])
    else:
        data[date] = [[set_time(time_start), set_time(time_end), text_task]]
def delete_tasks(date: str, num_tasks) -> None:
    try:
        global data
        num_tasks.sort(reverse=True)
        for num_task in num_tasks:
            del data[date][num_task-1]
    except:
        print('Ошибка, возможно, вы ввели не правильно номера задач')

def pop_sort(data):
    d = data
    for _ in range(len(d)):
        for i in range(len(d)-1):
            if d[i][0] > d[i+1][0]:
                copy_2 = d[i+1]
                copy_1 = d[i]
                d[i] = copy_2
                d[i+1] = copy_1
    return d
def get_plan_day(date: str):
        global data
        if date in data:
            

            tasks = pop_sort(data[date])
            data[date] = tasks
            if date == today: print(date,'СЕГОДНЯ')
            else: print(date)
            num_task = 0
            for task in tasks:
                num_task += 1
                if task[1] == None:
                    print(f"{num_task}. {handle_time(task[0])}        {task[-1]}")
                else:
                    print(f"{num_task}. {handle_time(task[0])}-{handle_time(task[1])}   {task[-1]}")
            # else:
            #     print('Нет задач')
    

   
    
def sort_data(data) -> list:
    frame_data = []
    for date in data:
        frame_data.append(list(map(int, date.split('.')))[::-1] + data[date])
    return sorted(frame_data)

def menu(day=today, show_planner=True):
    global today
    global data
    if show_planner == True:
        print('\n'*10)
        print('-' * 40)
        get_plan_day(day)
    print()
    print(*'1.Добавить_задачу 2.Удалить_задач(-у/-и) 3.Выбрать_день 4.Ближайшие_задачи 5.Все_задачи 6.Отчистить_весь_планер'.split())
    print('-' * 40)
    action = input('Введите номер действия: ')
    print('\n')
    
    if action == '1':
        if data == {}:
            print('Выберите день (нажмите 3)')
            menu()
        
        text_task = input('Текст задачи: ')
        while True:
            time_start, time_end = input('время начала XX:XX : '), input('Ничего не пишите, если нет времени окончания: ')
            if ':' not in time_start or len(time_start) != 5:
                print('Неверно ввели время начала')
            else:
                if time_end == '':
                    break
                else:
                    if ':' not in time_end or len(time_end) != 5:
                        print('Неверно ввели время окончания')
                    else:
                        break
            
        if time_end == '':
            time_end = None
        
        set_task(text_task, day, time_start, time_end)
    elif action == '2':
        if data == {}:
            try:
                if data[day] not in data:
                    print('Нечего удалять (нажмите 3, чтобы создать день)')
                    menu()
            except:
                    print('Нечего удалять (нажмите 3, чтобы создать день)')
                    menu()
        delete_tasks(day, list(map(int, input('номер(-а) задач(-и) вводите через пробел: ').split())))
    elif action == '3':
        while True:
            date = input('Введите дату ДД.ММ.ГГГГ: ')
            day, month, year = list(map(int, date.split('.')))
            if len(date) == 10 and 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100:
                break
            else: print('Ошибка, введите дату правильно ДД.ММ.ГГГГ')
    
        if date not in data:
            data[date] = []
        menu(date)

    elif action == '4':
        if len(data) == 0:
            print('Нет ни одного дня и задачи, чтобы создать, нажмите 3')
            menu(day)
        frame_data = sort_data(data)
        for i in range(len(frame_data)):
            if list(map(int, day.split('.')))[::-1] == frame_data[i][:3]:
                index = i
                break
        #print(frame_data)
        for num_date in range(index-3, index+3):
            
            if num_date < 0: continue
            try:
                iter_day = str(frame_data[num_date][2])
                month = str(frame_data[num_date][1])
            except:
                continue
            if len(iter_day) == 1: iter_day = '0'+ iter_day
            if len(month) == 1: month = '0'+ month
            get_plan_day(f"{iter_day}.{month}.{frame_data[num_date][0]}")
            print()
        show_planner = False

    elif action == '5':
        if len(data) == 0:
            print('Нет ни одного дня и задачи, чтобы создать, нажмите 3')
            menu(day)
        frame_data = sort_data(data)
        for num_date in range(len(frame_data)):
            iter_day = str(frame_data[num_date][2])
            month = str(frame_data[num_date][1])
            if len(iter_day) == 1: iter_day = '0'+ iter_day
            if len(month) == 1: month = '0'+ month
            get_plan_day(f"{iter_day}.{month}.{frame_data[num_date][0]}")
            print()
        show_planner = False

    elif action == '6':
        data = {}
    save_data(storage_filename, data, clear_data=True)
    menu(day=day, show_planner=show_planner)


if __name__ == '__main__':
    save_data(storage_filename) # создание файла, если его нет
    data = get_data(storage_filename)
    if today not in data:
        data[today] = []

    menu()

    
