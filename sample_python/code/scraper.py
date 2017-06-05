from pymongo import MongoClient
import errno


class Scraper(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.words_database
        # Collections are created in a lazy way, therefore it is not declared nor initialized here


    def get_words_list_from_db(self):
        # Retrieve all the word lists excluding the ID attribute
        cursor = self.db.words.find()

        # Save all the documents in the database
        words_list = []
        for record in cursor:
            words_list.append(record)
        return words_list

    def save_words_in_db(self, words_list):
        '''
        Insert the frequence list in the database if it
        does not exist in it yet
        '''
        if type(words_list) is dict:
            input_id = None
            if self.exists_in_db(words_list):
                input_id = self.db.words.insert_one(words_list).inserted_id
            return input_id
        else:
            return errno.EINVAL

        return cursor

    def exists_in_db(self, words_list):
        if type(words_list) is dict:
            element = self.db.words.find_one(words_list)
            return element is None
        else:
            return errno.EINVAL
