#!/usr/bin/env python3

import datetime
import os

from collections import OrderedDict
from peewee import *
from string import ascii_letters


db = SqliteDatabase('record.db')


class Entry(Model):
    """Entry Model"""
    timestamp = DateTimeField(default=datetime.datetime.now)
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


def clear():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
def check_date():
    """Checks date"""
    while True:
        try:
            m, d, y = input('Enter date(MM/DD/YYYY):').split('/')
            return datetime.datetime(year=int(y), month=int(m), day=int(d))
        except ValueError:
            print('Enter a valid date!')


def check(prompt):
    """Check the correct input"""
    while True:
        if prompt == 'time':
            try:
                print('Enter time spent on task')
                time = int(input('>').strip())
                if not time:
                    print('You must fill this field!')
                    continue
                return time
            except ValueError:
                print('JUST NUMBERS!!')
        elif prompt == 'name':
            print(f'Enter {prompt}')
            name = input('>')
            if not name:
                print('You must fill this field!')
            letters = ascii_letters + ' '
            if [x for x in name if x not in letters]:
                print('JUST ALPHABET LETTERS!')
            else:
                return name
        elif prompt == 'task':
            print(f'Enter {prompt}')
            task = input('>').strip()
            if not task:
                print('You must fill this field!')
                continue
            return task


def get_option(poz, entry):
    """The result menu options, removes the not wanted option """
    prompt = ['[P]revious', '[N]ext', '[E]dit', '[D]elete', '[R]eturn to menu']
    if poz == 0:
        prompt.remove('[P]revious')
    if poz == len(entry) - 1:
        prompt.remove('[N]ext')
    return prompt


def get_option_name(poz, entry):
    prompt = ['[P]revious', '[N]ext', '[E]nter', '[R]eturn to menu']
    if poz == 0:
        prompt.remove('[P]revious')
    if poz == len(entry) - 1:
        prompt.remove('[N]ext')
    return prompt


def add_entry():
    """Add new entry"""
    name = check('name')
    task = check('task')
    time = check('time')
    print('Enter additional notes(Optional)')
    notes = input('>').strip()
    try:
        Entry.create(name=name,
                     task=task,
                     time=time,
                     notes=notes)
    except IntegrityError:
        Entry.get(name=name,
                  task=task,
                  time=time,
                  notes=notes)
        print('This record already exist!')


def edit(entry):
    timestamp = entry.timestamp.strftime(' %B %d, %Y %I:%M%p')
    print('{}\n'
          'Old employee name: {}\n'
          'Old task name: {}\n'
          'Old time spent: {}\n'
          'Old notes: {}'.format(timestamp,
                                 entry.name,
                                 entry.task,
                                 entry.time,
                                 entry.notes))
    new_timestamp = check_date()
    new_name = check('name')
    new_task = check('task')
    new_time = check('time')
    new_notes = input('Enter notes(Optional): ').strip()
    new_record = Entry.get(name=entry.name)
    new_record.timestamp = new_timestamp
    new_record.name = new_name
    new_record.task = new_task
    new_record.time = new_time
    new_record.notes = new_notes
    new_record.save()
    print('New record saved!')


def search_entries(choice):
    """Search entries."""
    clear()
    while True:
        if choice == 'a':
            search_query = check_date()
            entries = Entry.select().where(Entry.timestamp.contains(search_query))
            if not entries:
                print('No record was found!')
                break
            else:
                result_menu(entries)
        if choice == 'b':
            start = check_date()
            end = check_date()
            entries = Entry.select().where(Entry.timestamp.between(start, end))
            if not entries:
                print('No record was found!')
                break
            else:
                result_menu(entries)
        if choice == 'd':
            search_query = input('Search for task: ')
            entries = Entry.select().where(Entry.task.contains(search_query))
            if not entries:
                print('No record was found!')
                break
            else:
                result_menu(entries)
        if choice == 'c':
            search_query = input('Search for name: ')
            name_list(search_query)
            break
        if choice == 'e':
            search_query = check('time')
            entries = Entry.select().where(Entry.time == search_query)
            if not entries:
                print('No record was found!')
                break
            else:
                result_menu(entries)
        if choice == 'f':
            search_query = input('Search for notes: ')
            entries = Entry.select().where(Entry.notes.contains(search_query))
            if not entries:
                print('No record was found!')
                break
            else:
                result_menu(entries)


def name_list(search_query):
    """Name list"""
    entries = Entry.select().where(Entry.name.contains(search_query))
    names = []
    for entry in entries:
        if entry.name not in names:
            names.append(entry.name)
    if len(names) == 1:
        result_menu(entries)
    else:
        index = 0
        while True:
            if not entries:
                print("No record was found!")
                break
            print(f'Employee name {names[index]}\n')
            print(f'Result {index + 1} of {len(names)}')
            print(' '.join(get_option_name(index, names)))
            action = input('>').lower().strip()
            if action not in ['p', 'n', 'e', 'r']:
                print('Choose from the available letters!')
                continue
            if (index + 1) == 1 and action == 'p':
                print('Choose from the available letters!')
                continue
            if (index + 1) == len(names) and action == 'n':
                print('Choose from the available letters!')
                continue
            if action == 'p':
                index -= 1
            if action == 'n':
                index += 1
            if action == 'r':
                break
            if action == 'e':
                entries = Entry.select().where(Entry.name.contains(names[index]))
                result_menu(entries)
                continue


def result_menu(entries):
    index = 0
    clear()
    while True:
        timestamp = entries[index].timestamp.strftime(' %B %d, %Y %I:%M%p')
        print('{}\n'
              'Employee name: {}\n'
              'Task name: {}\n'
              'Time spent: {}\n'
              'Notes: {}\n'.format(timestamp,
                                   entries[index].name,
                                   entries[index].task,
                                   entries[index].time,
                                   entries[index].notes))
        print(f'Result {index + 1} of {len(entries)}')
        print(' '.join(get_option(index, entries)))
        action = input('>').lower().strip()
        if action not in ['p', 'n', 'e', 'd', 'r']:
            print('Choose from the available letters!')
            continue
        if (index + 1) == 1 and action == 'p':
            clear()
            print('Choose from the available letters!')
            continue
        if (index + 1) == len(entries) and action == 'n':
            clear()
            print('Choose from the available letters!')
            continue
        if action == 'r':
            break
        if action == 'n':
            clear()
            index += 1
        if action == 'p':
            clear()
            index -= 1
        if action == 'e':
            clear()
            edit(entries[index])
            continue
        if action == 'd':
            print(entries[index].id)
            if input("Are you sure? [y/N] ").lower() == 'y':
                entries[index].delete_instance()
                print(len(entries))
                # if index == len(entries):
                #     index -= 1
            clear()
            print('Record deleted!')
            continue


def search_menu():
    """Search records"""
    clear()
    while True:
        for key, value in sub_menu.items():
            print(f'{key}] {value}')
        print('\n')
        action = input('>').lower().strip()
        if action not in sub_menu:
            print('Choose the available letters!')
        elif action == 'g':
            break
        else:
            search_entries(action)


def menu_loop():
    """Show the menu"""
    choice = None
    while choice != 'q':
        clear()
        print(f'There is {len(Entry.select())} record(s) in record.db.')
        for key, value in menu.items():
            print(f'{key}] {value.__doc__}')
        print('q] Quit')
        choice = input('>').lower().strip()
        if choice in menu:
            clear()
            menu[choice]()


menu = OrderedDict([
    ('a', add_entry),
    ('s', search_menu),
])

sub_menu = OrderedDict([
    ('a', 'Search by date'),
    ('b', 'Search by date range'),
    ('c', 'Search employee name'),
    ('d', 'Search task name'),
    ('e', 'Search time spent'),
    ('f', 'Search notes'),
    ('g', "Return to menu"),
])


if __name__ == "__main__":
    init()
    # add_entry()
    # search_entries('task', 'python')
    menu_loop()
