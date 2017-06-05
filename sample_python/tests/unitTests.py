# -*- coding: utf-8 -*-

import unittest
import errno
from .context import code


class CoreTestSuite(unittest.TestCase):
	
	def test_countWords_check_input_is_string(self):
		test=code.CountWords('potatoe')
		self.assertEqual(test.check_input(),'potatoe')

	def test_countWords_check_input_is_bool(self):
		test=code.CountWords(False)
		self.assertEqual(test.check_input(),errno.EINVAL)
		
	def test_countWords_check_input_is_integer(self):
		test=code.CountWords(0)
		self.assertEqual(test.check_input(),errno.EINVAL)
	
	def test_countWords_check_convert_to_lowercase(self):
		test=code.CountWords('Welcome John')
		self.assertEqual(test.convert_to_lowercase(),"welcome john")

	def test_countWords_check_remove_special_characters(self):
		test = code.CountWords.remove_special_characters('mesa? arbol.??#')
		self.assertEquals(test, ['m', 'e', 's', 'a', 'a', 'r', 'b', 'o', 'l'])

	def test_countWords_check_is_number_string(self):
		test = code.CountWords.is_number('sword')
		self.assertEquals(test, False)

	def test_countWords_check_is_number_bool(self):
		test = code.CountWords.is_number(False)
		self.assertEquals(test, True)

	def test_countWords_check_is_number_int(self):
		test = code.CountWords.is_number(1)
		self.assertEquals(test, True)

	def test_countWords_check_is_number_float(self):
		test = code.CountWords.is_number(1.3)
		self.assertEquals(test, True)

	def test_countWords_check_word_list_to_freq_list(self):
		test = code.CountWords.word_list_to_freq_list(['hello', 'hello', 'hello'])
		self.assertEquals(test, {'hello' : 3})

	def test_countWords_check_sort_freq_dict(self):
		test = code.CountWords.sort_freq_dict({'apple' : 3, 'hello' : 2, 'boat' : 4})
		self.assertEquals(test, [('boat', 4), ('apple', 3), ('hello', 2)]
)



if __name__ == '__main__':
    unittest.main()
