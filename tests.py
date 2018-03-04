from unittest.mock import patch
import unittest
import datetime
import work_log


class TestEntry(unittest.TestCase):
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
        
        
class Sub_menu_Tests(unittest.TestCase):
#    @patch('builtins.input', return_value='g')
#    def test_menu_quit(self, input):
#        self.assertEqual(work_log.main_menu(), None)

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


class MenuTests(unittest.TestCase):
#    @patch('builtins.input', return_value='q')
#    def test_menu_quit(self, input):
#        self.assertEqual(work_log.main_menu(), None)
        
    @patch('work_log.add_entry')
    def test_menu_add(self, add_entry_mock):
        with patch('builtins.input', side_effect='q'):
            work_log.main_menu()
        add_entry_mock.called_with('a')

    @patch('work_log.sub_menu')
    def test_menu_search(self, add_entry_mock):
        with patch('builtins.input', return_value='s', side_effect='q'):
            work_log.main_menu()
        add_entry_mock.called_once()

        
class TestCheck(unittest.TestCase):
    @patch('builtins.input', return_value='234 ')
    def test_check_time_valid(self, input):
        self.assertEqual(work_log.check('time'), 234)

    # @patch('builtins.input', return_value='')
    # def test_check_time_invalid(self, input):
    #     self.assertRaises(ValueError, work_log.check('time'))
    
    @patch('builtins.input', return_value='oszkar ')
    def test_check_name_valid(self, input):
        self.assertEqual(work_log.check('name'), "Oszkar Oszkar")
        
    @patch('builtins.input', return_value='Feher Oszkar ')
    def test_check_name_valid_true(self, input):
        self.assertEqual(work_log.check('name', True), "Feher Oszkar")


    @patch('builtins.input', return_value='python ')
    def test_check_task_valid(self, input):
        self.assertEqual(work_log.check('task'), "python")
        
    @patch('builtins.input', return_value='02/16/2018')
    def test_check_date(self, input):
        self.assertEqual(work_log.check_date(), datetime.datetime(year=2018, month=2, day=16))
        # self.assertRaises(ValueError, work_log.check_date())
        
        
class TestValidate(unittest.TestCase):
    @patch('work_log.result_menu')
    def test_validate(self, result_mock):
        length = ['one', 'two', 'three']
        work_log.validate(length)
        result_mock.called_once()
        
        
class TestSearch(unittest.TestCase):
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
        self.query = work_log.Entry.select()\
            .where(work_log.Entry.task == self.task)
        self.query_list = []
        for entry in self.query:
            if entry.task == 'java':
                self.query_list.append(entry)

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

#    @patch('work_log.validate')
#    def test_employee_name(self, validate_mock):
#        with patch('builtins.input', return_value='rayan'):
#            work_log.search_employee_name()
#        validate_mock.called_with(work_log.Entry.select()
#                                  .where(work_log.Entry.name == 'rayan'))

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


        

if __name__ == '__main__':
    unittest.main()
