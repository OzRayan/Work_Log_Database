#!/usr/bin/env python3

import datetime
import os

from collections import OrderedDict
from peewee import *


db = SqliteDatabase('record.db')
NAMES = []
RECORD = []
LETTERS = 'abcdefghijklmnopqrstuvwxyz '


class Entry(Model):
    """Entry Model"""
    timestamp = DateTimeField(default=datetime.date.today)
    name = CharField(max_length=100)
    task = CharField(max_length=255)
    time = IntegerField()
    notes = TextField(default='')

    class Meta:
        database = db


def init():
    """Initialize"""
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()


def clear_screen():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def check(prompt, boolean=None):
    """Check the correct input"""
    while True:
        clear_screen()
        if prompt == 'time':
            try:
                clear_screen()
                print('Enter time spent on task')
                time = int(input('>').strip())
                if not time:
                    clear_screen()
                    print('You must fill this field!')
                    continue
                return time
            except ValueError:
                clear_screen()
                print('JUST NUMBERS!!')
        elif prompt == 'name':
            clear_screen()
            if boolean:
                print('Enter {}'.format(prompt))
                name = input('>').strip()
                if not name:
                    clear_screen()
                    print('You must provide a name!')
                    continue
            else:
                print('Enter first{}'.format(prompt))
                first_name = input('>').strip().capitalize()
                print('Enter last{}'.format(prompt))
                last_name = input('>').strip().capitalize()
                if not first_name or not last_name:
                    clear_screen()
                    print('You must fill this field!')
                    continue
                if not first_name and not last_name:
                    clear_screen()
                    print('You must fill these fields!')
                    continue
                name = first_name + ' ' + last_name

            # CHECK AGAIN THE CONTINUITY OF WRONG INPUT!!
            if [x for x in name if x.lower() not in LETTERS]:
                clear_screen()
                print('JUST ALPHABET LETTERS!')
            else:
                return name
        elif prompt == 'task':
            clear_screen()
            print('Enter {}'.format(prompt))
            task = input('>').strip()
            if not task:
                clear_screen()
                print('You must fill this field!')
                continue
            return task


def check_date():
    """Checks date"""
    while True:
        clear_screen()
        try:
            m, d, y = input('Enter date(MM/DD/YYYY):\n>').split('/')
            return datetime.date(year=int(y), month=int(m), day=int(d))
        except ValueError:
            clear_screen()
            print('Enter a valid date!')


def get_option(poz, entry, name=None):
    """The result menu options, removes the not wanted option """
    if name:
        prompt = ['[P]revious', '[N]ext', '[E]nter', '[R]eturn to menu']
    else:
        prompt = ['[P]revious', '[N]ext', '[E]dit', '[D]elete', '[R]eturn to menu']
    if poz == 0:
        prompt.remove('[P]revious')
    if poz == len(entry) - 1:
        prompt.remove('[N]ext')
    return prompt


def add_entry():
    """Add new record"""
    clear_screen()
    name = check('name')
    task = check('task')
    time = check('time')
    print('Enter additional notes(Optional)')
    notes = input('>').strip()
    # noinspection PyBroadException
    try:
        Entry.create(name=name,
                     task=task,
                     time=time,
                     notes=notes)
        print("Record successfully saved!")
    except Exception:
        pass


def update_entry(query, index):
    """Get new input for each field and save it"""
    timestamp = query.timestamp.strftime('%B %d, %Y')
    clear_screen()
    print('{}\n'
          'Old employee name: {}\n'
          'Old task name: {}\n'
          'Old time spent: {}\n'
          'Old notes: {}'.format(timestamp,
                                 query.name,
                                 query.task,
                                 query.time,
                                 query.notes))
    new_timestamp = check_date()
    new_name = check('name')
    new_task = check('task')
    new_time = check('time')
    new_notes = input('Enter notes(Optional): \n>').strip()
    new_record = Entry.get(name=query.name,
                           timestamp=query.timestamp,
                           task=query.task,
                           time=query.time,
                           notes=query.notes)
    new_record.timestamp = new_timestamp
    new_record.name = new_name
    new_record.task = new_task
    new_record.time = new_time
    new_record.notes = new_notes
    new_record.save()
    RECORD.pop(index)
    entry = Entry.get(name=new_name,
                      timestamp=new_timestamp,
                      task=new_task,
                      notes=new_notes)
    RECORD.insert(index, entry)
    # if query.name != new_name:
    #     NAMES.remove(query.name)
    print('New record saved!')


def remove_entry(query):
    """Delete instance from query"""
    Entry.delete_instance(query)


def validate(query):
    """Checks if query exist, if is populates the RECORD list"""
    RECORD.clear()
    if not query:
        print("Record doesn't exist!")
    for x in query:
        RECORD.append(x)
    if len(RECORD) != 0:
        result_menu()


def search_by_date():
    """Search by date"""
    query = check_date()
    return_value = Entry.select().where(Entry.timestamp.contains(query))
    validate(return_value)


def search_by_date_range():
    """Search by date range"""
    start = check_date() - datetime.timedelta(days=1)
    end = check_date() + datetime.timedelta(days=1)
    return_value = Entry.select().where(Entry.timestamp.between(start, end))
    validate(return_value)


def search_employee_name():
    """Search employee name"""
    NAMES.clear()
    RECORD.clear()
    query = check('name', True)
    return_value = Entry.select().where(Entry.name.contains(query))
    if not return_value:
        print("Record doesn't exist!")
    for x in return_value:
        if x.name in NAMES:
            continue
        else:
            NAMES.append(x.name)
    if len(NAMES) != 0:
        name_list_menu()


def search_task_name():
    """Search task name"""
    query = input('Search for task: \n>')
    return_value = Entry.select().where(Entry.task.contains(query))
    validate(return_value)


def search_time_spent():
    """Search time spent"""
    query = check('time')
    return_value = Entry.select().where(Entry.time == query)
    validate(return_value)


def search_notes():
    """Search notes"""
    query = input('Search for notes: \n>')
    return_value = Entry.select().where(Entry.notes.contains(query))
    validate(return_value)


def name_list_menu():
    """Name list"""
    action = None
    index = len(NAMES) - len(NAMES)
    while action != 'r':
        clear_screen()
        if len(NAMES) == 1:
            index = 0
        if len(NAMES) == 0:
            break
        print_bar = '=' * (15 + len(NAMES[index]))
        print(print_bar)
        print('Employee name: {}'.format(NAMES[index]))
        print(print_bar)
        print('Result {} of {}\n'.format(index + 1, len(NAMES)))
        print(' '.join(get_option(index, NAMES, True)))
        action = input('>').lower().strip()
        if action not in ['p', 'n', 'e', 'r']:
            print('Choose from the available letters!')
            continue
        if (index + 1) == 1 and action == 'p':
            print('Choose from the available letters!')
            continue
        if (index + 1) == len(NAMES) and action == 'n':
            print('Choose from the available letters!')
            continue
        if action == 'p':
            clear_screen()
            index -= 1
        if action == 'n':
            clear_screen()
            index += 1
        if action == 'e':
            clear_screen()
            RECORD.clear()
            entries = Entry.select()\
                .where(Entry.name.contains(NAMES[index]))
            for x in entries:
                RECORD.append(x)
            result_menu()
            if index == 1:
                index += 1
            if index == len(NAMES):
                index -= 1
            continue


def result_menu():
    """Shows the searched entries one by one with detailed description,
    Navigation included"""
    action, index = None, 0
    prompt = 'Choose from the available letters!'
    while action != 'r':
        clear_screen()
        if len(RECORD) == 1:
            index = 0
        timestamp = RECORD[index].timestamp.strftime('%B %d, %Y')
        print('=' * len(timestamp))
        print('{}\n'
              'Employee name: {}\n'
              'Task name: {}\n'
              'Time spent: {}\n'
              'Notes: {}'.format(timestamp,
                                 RECORD[index].name,
                                 RECORD[index].task,
                                 RECORD[index].time,
                                 RECORD[index].notes))
        print('=' * (len(RECORD[index].notes) + 7) + '\n')
        print('Result {} of {}'.format(index + 1, len(RECORD)))
        print(' '.join(get_option(index, RECORD)))
        action = input('>').lower().strip()
        if action not in ['p', 'n', 'e', 'd', 'r']:
            clear_screen()
            print(prompt)
            continue
        if (index + 1) == 1 and action == 'p':
            print(prompt)
            continue
        if (index + 1) == len(RECORD) and action == 'n':
            print(prompt)
            continue
        if action == 'n':
            clear_screen()
            index += 1
        if action == 'p':
            clear_screen()
            index -= 1
        if action == 'e':
            clear_screen()
            update_entry(RECORD[index], index)
            continue
        if action == 'd':
            clear_screen()
            if input("Are you sure? [y/N] ").lower() == 'y':
                remove_entry(RECORD[index])
                name = RECORD[index].name
                RECORD.pop(index)
                if index == 1:
                    index += 1
                if index == len(RECORD):
                    index -= 1
                if len(RECORD) == 0 and len(NAMES) != 0:
                    NAMES.remove(name)
                    break
                if len(RECORD) == 0:
                    break
            print('Record deleted!')
            continue


def sub_menu():
    """Search records"""
    action = None
    while action != 'g':
        clear_screen()
        if len(Entry.select()) == 0:
            break
        for key, value in s_menu.items():
            print(' {}] {}'.format(key, value.__doc__))
        print(' g] Return to menu')
        action = input('>').lower().strip()
        if action in s_menu:
            clear_screen()
            s_menu[action]()


def main_menu():
    """Show the menu"""
    init()
    action = None
    while action != 'q':
        clear_screen()
        length = len(Entry.select())
        if length == 1:
            plural = ''
        else:
            plural = 's'
        print(' {} record{} in record.db.\n'.format(length, plural))
        for key, value in menu.items():
            print(' {}] {}'.format(key, value.__doc__))
        print(' q] Quit')
        action = input('>').lower().strip()
        if action in menu:
            clear_screen()
            menu[action]()


menu = OrderedDict([
    ('a', add_entry),
    ('s', sub_menu)])
s_menu = OrderedDict([
    ('a', search_by_date),
    ('b', search_by_date_range),
    ('c', search_employee_name),
    ('d', search_task_name),
    ('e', search_time_spent),
    ('f', search_notes)])


if __name__ == "__main__":
    main_menu()
