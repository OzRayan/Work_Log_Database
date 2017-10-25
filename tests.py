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

    def test_check(self):
        pass
    
    def test_get_option(self):
        poz = 0
        entry = 'entry'
        self.assertEqual(work_log.get_option(poz, entry), ['[N]ext', '[E]dit', '[D]elete', '[R]eturn to menu'])
        self.assertEqual(work_log.get_option_name(poz, entry), ['[N]ext', '[E]nter', '[R]eturn to menu'])
        poz = len(entry) - 1
        self.assertEqual(work_log.get_option(poz, entry), ['[P]revious', '[E]dit', '[D]elete', '[R]eturn to menu'])
        self.assertEqual(work_log.get_option_name(poz, entry), ['[P]revious', '[E]nter', '[R]eturn to menu'])

    @patch('builtins.input', return_value='Feher Oszkar')
    def test_search_entry(self, input):
        choice = 'c'
        self.assertEqual(work_log.search_entries(choice), 'Feher Oszkar')
        
    #   THIS METHOD RETURNS AN INFINITE RESULT LOOP, I DON'T KNOW HOW TO FIX IT


if __name__ == '__main__':
    unittest.main()
