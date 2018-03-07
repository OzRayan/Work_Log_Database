from unittest.mock import patch
import unittest
import datetime
import work_log


class Base(unittest.TestCase):
    pass


class TestEntry(Base):
    def setUp(self):
        self.timestamp = datetime.datetime.now()
        self.name = 'Feher Oszkar'
        self.task = 'Python'
        self.time = 23
        self.notes = 'Python Collections'

        self.timestamp_2 = datetime.datetime.now()
        self.name_2 = 'Rayan Oscar'
        self.task_2 = 'Java'
        self.time_2 = 33
        self.notes_2 = 'Java Core'

    def test_add_entry(self):
        self.assertEqual(self.timestamp, work_log.Entry.timestamp)
        self.assertEqual(self.name, work_log.Entry.name)
        self.assertEqual(self.task, work_log.Entry.task)
        self.assertEqual(self.time, work_log.Entry.time)
        self.assertEqual(self.notes, work_log.Entry.notes)

        self.assertEqual(self.timestamp_2, work_log.Entry.timestamp)
        self.assertEqual(self.name_2, work_log.Entry.name)
        self.assertEqual(self.task_2, work_log.Entry.task)
        self.assertEqual(self.time_2, work_log.Entry.time)
        self.assertEqual(self.notes_2, work_log.Entry.notes)

    def test_check(self):
        pass

    def test_get_option(self):
        poz = 0
        entry = 'entry'
        self.assertEqual(work_log.get_option(poz, entry), ['[N]ext', '[E]dit', '[D]elete', '[R]eturn to menu'])
        self.assertEqual(work_log.get_option(poz, entry, True), ['[N]ext', '[E]nter', '[R]eturn to menu'])
        poz = len(entry) - 1
        self.assertEqual(work_log.get_option(poz, entry), ['[P]revious', '[E]dit', '[D]elete', '[R]eturn to menu'])
        self.assertEqual(work_log.get_option(poz, entry, True), ['[P]revious', '[E]nter', '[R]eturn to menu'])


class TestSubMenu(Base):
    @patch('work_log.sub_menu')
    def test_sub_menu_quit(self, mock):
        with patch('builtins.input', return_value='g'):
            work_log.sub_menu()
        mock.called_once()

    @patch('work_log.search_by_date')
    def test_sub_menu_date(self, add_entry_mock):
        with patch('builtins.input', return_value='a', side_effect='g'):
            work_log.sub_menu()
        add_entry_mock.called_once()

    @patch('work_log.search_by_date_range')
    def test_sub_menu_range(self, add_entry_mock):
        with patch('builtins.input', return_value='b', side_effect='g'):
            work_log.sub_menu()
        add_entry_mock.called_once()

    @patch('work_log.search_employee_name')
    def test_sub_menu_name(self, add_entry_mock):
        with patch('builtins.input', return_value='c', side_effect='g'):
            work_log.sub_menu()
        add_entry_mock.called_once()

    @patch('work_log.search_task_name')
    def test_sub_menu_task(self, add_entry_mock):
        with patch('builtins.input', return_value='d', side_effect='g'):
            work_log.sub_menu()
        add_entry_mock.called_once()

    @patch('work_log.search_time_spent')
    def test_sub_menu_time(self, add_entry_mock):
        with patch('builtins.input', return_value='e', side_effect='g'):
            work_log.sub_menu()
        add_entry_mock.called_once()

    @patch('work_log.search_notes')
    def test_sub_menu_notes(self, add_entry_mock):
        with patch('builtins.input', return_value='f', side_effect='g'):
            work_log.sub_menu()
        add_entry_mock.called_once()


class TestMenu(Base):
    @patch('work_log.main_menu')
    def test_menu_quit(self, main_mock):
        with patch('builtins.input', return_value='q'):
            work_log.main_menu()
        main_mock.called_once()
        
    @patch('work_log.main_menu')
    def test_menu_invalid(self, main_mock):
        with patch('builtins.input', return_value='x', side_effect='q'):
            work_log.main_menu()
        main_mock.called_once()

    @patch('work_log.add_entry')
    def test_menu_add(self, add_entry_mock):
        with patch('builtins.input', side_effect='q'):
            work_log.main_menu()
        add_entry_mock.called_with('a')

    @patch('work_log.sub_menu')
    def test_menu_search(self, search_entry_mock):
        with patch('builtins.input', side_effect='q'):
            work_log.main_menu()
        search_entry_mock.called_with('s')


class TestCheck(Base):
    @patch('builtins.input', return_value='234 ')
    def test_check_time_valid(self, input):
        self.assertEqual(work_log.check('time'), 234)

    @patch('work_log.check')
    def test_check_time_invalid(self, check_mock):
        with patch('builtins.input', return_value='a', side_effect=ValueError):
            work_log.check('time')
        check_mock.called_once()

    @patch('builtins.input', return_value='oszkar ')
    def test_check_name_valid(self, input):
        self.assertEqual(work_log.check('name'), "Oszkar Oszkar")

    @patch('work_log.check')
    def test_check_name_invalid(self, check_mock):
        with patch('builtins.input', return_value=12, side_effect='JUST ALPHABET LETTERS!'):
            work_log.check('name')
        check_mock.called_once()

    @patch('work_log.check')
    def test_check_no_name(self, check_mock):
        with patch('builtins.input', return_value=None, side_effect='You must fill these fields!'):
            work_log.check('name')
        check_mock.called_once()

    @patch('builtins.input', return_value='Feher Oszkar ')
    def test_check_name_valid_true(self, input):
        self.assertEqual(work_log.check('name', True), "Feher Oszkar")

    @patch('builtins.input', return_value='python ')
    def test_check_task_valid(self, input):
        self.assertEqual(work_log.check('task'), "python")

    @patch('work_log.check')
    def test_check_no_task(self, check_mock):
        with patch('builtins.input', return_value=None, side_effect='You must fill this field!'):
            work_log.check('task')
        check_mock.called_once()

    @patch('builtins.input', return_value='02/16/2018')
    def test_check_date(self, input):
        self.assertEqual(work_log.check_date(), datetime.date(year=2018, month=2, day=16))

    @patch('work_log.check_date')
    def test_check_date_invalid(self, check_mock):
        with patch('builtins.input', return_value='13/32/4000', side_effect=ValueError):
            work_log.check_date()
        check_mock.called_once()



class TestValidate(Base):
    @patch('work_log.result_menu')
    def test_validate(self, result_mock):
        length = ['one', 'two', 'three']
        work_log.validate(length)
        result_mock.called_once()


class TestSearch(Base):
    def setUp(self):
        self.today = datetime.datetime.today()
        self.task = 'java'
        work_log.Entry.create(
            timestamp=self.today,
            name='rayan',
            task=self.task,
            time=234,
            notes='unittest notes'
        )
        work_log.Entry.create(
            timestamp=self.today,
            name='rayan',
            task=self.task,
            time=2345,
            notes='unittest notes2'
        )
        self.query = work_log.Entry.select() \
            .where(work_log.Entry.task == self.task)
        self.query_list = []
        for entry in self.query:
            if entry.task == 'java':
                self.query_list.append(entry)

    @patch('work_log.check', return_value='rayan')
    @patch('work_log.check', return_value='unittest')
    @patch('work_log.check', raturn_value='234')
    def test_add(self, name_mock, task_mock, time_mock):
        with patch('builtins.input', return_value='unittest notes3'):
            work_log.add_entry()
        name_mock.called_with('name')
        task_mock.called_with('task')
        time_mock.called_with('time')

    @patch('work_log.validate')
    def test_notes(self, validate_mock):
        with patch('builtins.input', return_value='unittest notes'):
            work_log.search_notes()
        validate_mock.called_with(work_log.Entry.select()
                                  .where(work_log.Entry.notes.contains('unittest notes')))

    @patch('work_log.validate')
    def test_time(self, validate_mock):
        with patch('builtins.input', return_value='234'):
            work_log.search_time_spent()
        validate_mock.called_with(work_log.Entry.select()
                                  .where(work_log.Entry.time.contains(234)))

    @patch('work_log.validate')
    def test_task(self, validate_mock):
        with patch('builtins.input', return_value='java'):
            work_log.search_task_name()
        validate_mock.called_with(work_log.Entry.select()
                                  .where(work_log.Entry.task.contains('java')))

    @patch('work_log.name_list_menu')
    def test_employee_name(self, validate_mock):
        with patch('builtins.input', return_value='rayan'):
            work_log.search_employee_name()
        validate_mock.called_once()

    @patch('work_log.validate')
    def test_by_date(self, validate_mock):
        with patch('builtins.input', return_value='02/27/2018'):
            work_log.search_by_date()
        validate_mock.called_with(work_log.Entry.select()
                                  .where((work_log.Entry.timestamp.day == 27)
                                         & (work_log.Entry.timestamp.month == 2)
                                         & (work_log.Entry.timestamp.year == 2018)))

    def tearDown(self):
        for entry in self.query:
            work_log.Entry.delete_instance(entry)


class TestUpdate(Base):
    list_records = []

    def setUp(self):
        self.today = datetime.datetime.today()
        self.task = 'unittest update'
        work_log.Entry.create(
            timestamp=self.today,
            name='rayan',
            task=self.task,
            time=234,
            notes='unittest notes'
        )
        self.query = work_log.Entry.select() \
            .where(work_log.Entry.task == self.task)
        for x in self.query:
            self.list_records.append(x)

    @patch('work_log.check_date', return_value='02/16/2018')
    @patch('work_log.check', raturn_value='567')
    @patch('work_log.check', return_value='oszkar')
    @patch('work_log.check', return_value='unittest2')
    @patch('work_log.RECORD', return_value=list_records)
    def test_update(self, timestamp_mock, time_mock, task_mock, name_mock, records):
        with patch('builtins.input', return_value='unittest notes'):
            work_log.update_entry(self.query[0], 0)
        records.called_once()
        timestamp_mock.called_once()
        name_mock.called_with('name')
        task_mock.called_with('task')
        time_mock.called_with('time')
        
    def test_remove_entry(self):
        self.assertEqual(work_log.remove_entry(self.list_records[0]), None)


    def tearDown(self):
        for query in self.query:
            work_log.Entry.delete_instance(query)
            
            
class TestNameListMenu(Base):
    names = []
    records = []

    def setUp(self):
        query = work_log.Entry.select()
        for x in query:
            self.names.append(x)
            self.records.append(x)

    @patch('work_log.result_menu')
    @patch('work_log.RECORD', return_value=records)
    @patch('work_log.NAMES', return_value=names)
    def test_enter(self, result_mock, records_mock, names_mock):
        with patch('builtins.input', return_value='e',
                   side_effect='r'):
            work_log.name_list_menu()
        records_mock.called_once()
        names_mock.called_once()
        result_mock.called_once()

    @patch('work_log.name_list_menu', return_value=len(names))
    @patch('work_log.NAMES', return_value=names)
    def test_next(self, index_mock, names_mock):
        with patch('builtins.input', return_value='n', side_effect='r'):
            work_log.name_list_menu()
        index_mock.called_with('n')
        names_mock.called_once()

    def test_bad_choice(self):
        with patch('builtins.input',
                   return_value='x',
                   side_effect='Choose from the available letters!'):
            self.assertEqual(work_log.name_list_menu(), None)


        
class TestResultMenu(Base):
    names = []
    records = []

    def setUp(self):
        query = work_log.Entry.select()
        for x in query:
            self.names.append(x)
            self.records.append(x)

    @patch('work_log.update_entry')
    @patch('work_log.RECORD', return_value=names)
    def test_edit(self, update_mock, record_mock):
        with patch('builtins.input', return_value='e', side_effect='r'):
            work_log.result_menu()
        record_mock.called_once()
        update_mock.called_once()

    @patch('work_log.remove_entry')
    @patch('work_log.NAMES', return_value=names)
    @patch('work_log.RECORD', return_value=records)
    def test_delete(self, remove_mock, name_mock, record_mock):
        with patch('builtins.input', return_value='d', side_effect='r'):
            work_log.result_menu()
        name_mock.called_once()
        record_mock.called_once()
        remove_mock.called_once()
        
    @patch('work_log.result_menu')
    def test_invalid_choice(self, result_mock):
        with patch('builtins.input', return_value='x', side_effect='r'):
            work_log.result_menu()
        result_mock.called_once()
        
        
class TestInit(Base):
    @patch('work_log.db')
    def test_init(self, db_mock):
        work_log.init()
        self.assertTrue(db_mock.connect.called)
        self.assertTrue(db_mock.create_tables.called)


if __name__ == '__main__':
    unittest.main()
