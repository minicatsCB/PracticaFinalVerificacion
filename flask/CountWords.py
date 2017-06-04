# -*- coding: utf-8 -*-

import re  # For removing HTML tags
import collections # For count frequency
import operator  # For sorting by fequency
import errno

class CountWords(object):
    def __init__(self, text):
        self._text = text

    def check_input(self):
        if type(self._text) is str:
            return str(self._text)
        else:
            return errno.EINVAL

    def convert_to_lowercase(self):
        '''Convert all the strings of
        the list received to lowercase
        '''
        return self._text.lower()

    @classmethod
    def remove_special_characters(self, word_list):
        return [e for e in word_list if e.isalpha() or e.isdigit()]

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
	'''
        stopwords = {'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'for', 'by',
                       'are', 'i', 'you', 'he', 'she', 'we', 'do', 'does', 'did',
                       'say', 'said', 'says', 'tell', 'told', 'what', 'where',
                       'when', 'how', 'who', 'whose', 'why', 'would'}
	'''

	stopwords = {'un','una','unas','unos','uno','sobre','todo','también','tras','otro','algún','alguno','alguna','algunos','algunas',
			'ser','es','soy','eres','somos','sois','estoy','esta','estamos','estais','estan','como','en','para','atras','estado',
			'estaba','ante','antes','siendo','ambos','pero','por','poder','puede','puedo','podemos','podeis','pueden','fui',
			'fue','fuimos','fueron','hacer','hago','hace','hacemos','haceis','hacen','cada','fin','incluso','primero','desde',
			'conseguir','consigo','consigue','consigues','conseguimos','consiguen','ir','voy','va','vamos','vais','van','vaya',
			'ha','tener','tengo','tiene','tenemos','teneis','tienen','el','la','lo','las','los','su','aqui','mio','tuyo','ellos','ellas',
			'nos','nosotros','vosotros','vosotras','si','dentro','solo','solamente','saber','sabes','sabe','sabemos','sabeis',
			'saben','ultimo','largo','bastante','haces','muchos','aquellos','aquellas','sus','entonces','verdadero','verdadera',
			'ciertos','ciertas','intentar','intento','intenta','intentas','intentamos','intentais','intentan','bajo','arriba',
			'encima','usar','uso','usas','usa','usamos','usais','usan','emplear','empleas','emplean','empleamos','empleais','valor',
			'muy','era','eras','eramos','eran','modo','mientras','con','entre','sin','trabajar','trabajas','trabajamos','trabajais',
			'trabajan','podria','podrias','podriamos','podrian','podriais','yo','aquel', 'de', 'que', 'en', 'a', 'el', 'la', 'y', 'del', 'se', 'al', 'han', 'h', 'o'}
	
	# Convert string to list
	word_list = word_list.split()

        return [word for word in word_list if word not in stopwords]

    @classmethod
    def word_list_to_freq_list(self, word_list):
        """ Returns a list with the number
        of times each word appears in the text
        """
	return dict(collections.Counter(word_list))


    @classmethod
    def sort_freq_dict(self, freq_dict):
        '''Order the elements in the dictionary
        based on each's frequency (by descending frecuency)
        '''
	sorted_freq_dict = sorted(freq_dict.items(), key=operator.itemgetter(1), reverse = True)
        return sorted_freq_dict


    def text_analyzer(self):
	# Remove HTML tags
	p = re.compile(r'<.*?>')
	self._text = p.sub('', self._text)
        self.check_input()  # Is a valid input?
        word_list = self.convert_to_lowercase()  # Convert to lowercase
	word_list = self.remove_stopwords(word_list)
        word_list = self.remove_special_characters(word_list)  # Remove special characters
        freq_list = self.word_list_to_freq_list(word_list)  # Pairs word:freq (not sorted)
        sorted_list = self.sort_freq_dict(freq_list)  # Pairs word:freq (sorted)
        return sorted_list

