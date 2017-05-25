# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

import errno
import sys

import unicodedata


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]





    def check_input(self):
	print("Check Check Check Check Check Check Check Check Check Check Check Check")
	# print(self._text)
        if type(self._text) is str:
            return str(self._text)
        else:
            return errno.EINVAL

    def convert_to_lowercase(self):
        '''Convert all the strings of
        the list received to lowercase
        '''
        word_list = self._text
        return [w.lower() for w in word_list]

    @classmethod
    def remove_special_characters(self, word_list):
        return ''.join(e for e in word_list if e.isalnum() or e == ' ')

    @classmethod
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @classmethod
    def remove_words_with_digits(self, word_list):
        '''
        Check if a word contains one or
        more digits and remove it
        '''
        cleaned_list = []
        is_digit = False
        for word in word_list:
            is_digit = False
            for ch in word:
                if(self.is_number(ch)):
                    is_digit = True
            if(is_digit == False):
                cleaned_list.append(word)
        return cleaned_list

    @classmethod
    def remove_stopwords(self, word_list):
        '''Returns only the words
        which are not a stopword
        '''
        stopwords = {'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'for', 'by',
                       'are', 'i', 'you', 'he', 'she', 'we', 'do', 'does', 'did',
                       'say', 'said', 'says', 'tell', 'told', 'what', 'where',
                       'when', 'how', 'who', 'whose', 'why', 'would'}
        return [w for w in word_list if w not in stopwords]

    @classmethod
    def word_list_to_freq_list(self, word_list):
        """ Returns a list with the number
        of times each word appears in the text
        """
        word_freq = [word_list.count(w) for w in word_list]  # A list comprehension
        return dict(zip(word_list, word_freq))

    @classmethod
    def sort_freq_dict(self, freq_dict):
        '''Order the elements in the dictionary
        based on each's frequency (by descending frecuency)
        '''
        aux = [(freq_dict[key], key) for key in freq_dict]
        aux.sort()
        aux.reverse()
        return aux

    def text_analyzer(self):
        self.check_input()  # Is a valid input?
        word_list = self.convert_to_lowercase()  # Convert to lowercase
        word_list = self.remove_special_characters(word_list)  # Remove special characters
        word_list = word_list.split()  # Separate words
        word_list = self.remove_words_with_digits(word_list)
        word_list = self.remove_stopwords(word_list)
        freq_list = self.word_list_to_freq_list(word_list)  # Pairs word:freq (not sorted)
        sorted_list = self.sort_freq_dict(freq_list)  # Pairs word:freq (sorted)
        return sorted_list


    def process_item(self, item, spider):
	self._text = ' '.join(item['text'])
	self._text = self._text.encode('ascii', 'ignore')
	print("En MongoooooooooooooooooooooooooDB")
	#print(self._text)
	print("Imprimidoooooooooooooooooooooooooo")
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
	    result = self.text_analyzer()
	    my_dict = {'count': result}
	    #print(result)
            self.collection.insert(dict(my_dict))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

