import unittest
from client import create_message

create_message()

class TestSalary(unittest.TestCase):

    def test_get_salary_summ(self):
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000'),
                         ('Лютиков Руслан', 60000))

    def test_get_salary_fio(self):
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000')[0],
                         'Лютиков Руслан')

    def test_get_salary_empty(self):
        self.assertEqual(get_salary(''), ('1', '2'))


if __name__ == "__main__":
    unittest.main()
