from unittest import TestCase
from code.scraper import Scraper
import mock

from mock import *
import mongomock
import errno

class TestScraper(TestCase):
    def setUp(self):
        self.scraper = Scraper()
        self.scraper.client = mongomock.MongoClient()
        self.scraper.db = self.scraper.client.words_database

    def tearDown(self):
        self.scraper.db.drop_collection('words')

    def test_get_words_list_from_db_with_only_one(self):
        temp_words_list = {"casa": 5, "mesa": 3, "patata": 2}
        self.scraper.db.words.insert_one(temp_words_list)

        mock = Mock()
        mock(self.scraper.db.words.insert_one, temp_words_list)
        mock.assert_called_once_with(self.scraper.db.words.insert_one, temp_words_list)

        received_words_list = self.scraper.get_words_list_from_db()
        self.assertEqual([temp_words_list], received_words_list)

    def test_get_words_list_from_db_with_two_lists(self):
        temp_words_list1 = {"casa": 5, "mesa": 3, "patata": 2}
        temp_words_list2 = {"casa": 5, "mesa": 3, "patata": 2, "tomate":4}
        self.scraper.db.words.insert_one(temp_words_list1)
        self.scraper.db.words.insert_one(temp_words_list2)

        received_words_list = self.scraper.get_words_list_from_db()
        self.assertEqual([temp_words_list1, temp_words_list2], received_words_list)

    def test_get_words_list_from_db_with_multiple_lists(self):
        temp_words_list1 = {"casa": 5, "mesa": 3, "patata": 2}
        temp_words_list2 = {"casa": 4, "mesa": 2, "patata": 2, "tomate": 4}
        temp_words_list3 = {"casa": 3, "mesa": 3, "tomate": 4}
        temp_words_list4 = {"casa": 2, "mesa": 2, "patata": 2, "tomate": 7}
        temp_words_list5 = {"casa": 1, "patata": 2, "tomate": 4}
        self.scraper.db.words.insert_one(temp_words_list1)
        self.scraper.db.words.insert_one(temp_words_list2)
        self.scraper.db.words.insert_one(temp_words_list3)
        self.scraper.db.words.insert_one(temp_words_list4)
        self.scraper.db.words.insert_one(temp_words_list5)

        received_words_list = self.scraper.get_words_list_from_db()
        self.assertEqual([temp_words_list1, temp_words_list2, temp_words_list3, temp_words_list4, temp_words_list5],
                         received_words_list)


    def test_remove_words_list_from_db_with_only_one(self):
        temp_words_list = {"casa": 2, "mesa": 2, "patata": 2, "tomate": 7}
        self.scraper.db.words.insert_one(temp_words_list)
        self.scraper.db.words.delete_one(temp_words_list)

        mock = Mock()
        mock(self.scraper.db.words.delete_one, temp_words_list)
        mock.assert_called_once_with(self.scraper.db.words.delete_one, temp_words_list)

        received_words_list = self.scraper.get_words_list_from_db()
        self.assertEqual([], received_words_list)

    def test_remove_words_list_from_db_with_two_lists(self):
        temp_words_list1 = {"casa": 5, "mesa": 3, "patata": 2}
        temp_words_list2 = {"casa": 5, "mesa": 3, "patata": 2, "tomate":4}
        self.scraper.db.words.insert_one(temp_words_list1)
        self.scraper.db.words.insert_one(temp_words_list2)
        self.scraper.db.words.delete_one(temp_words_list1)

        received_words_list = self.scraper.get_words_list_from_db()
        self.assertEqual([temp_words_list2], received_words_list)

    def test_remove_words_list_from_db_with_multiple_lists(self):
        temp_words_list1 = {"casa": 5, "mesa": 3, "patata": 2}
        temp_words_list2 = {"casa": 4, "mesa": 2, "patata": 2, "tomate": 4}
        temp_words_list3 = {"casa": 3, "mesa": 3, "tomate": 4}
        temp_words_list4 = {"casa": 2, "mesa": 2, "patata": 2, "tomate": 7}
        temp_words_list5 = {"casa": 1, "patata": 2, "tomate": 4}
        self.scraper.db.words.insert_one(temp_words_list1)
        self.scraper.db.words.insert_one(temp_words_list2)
        self.scraper.db.words.insert_one(temp_words_list3)
        self.scraper.db.words.insert_one(temp_words_list4)
        self.scraper.db.words.insert_one(temp_words_list5)
        self.scraper.db.words.delete_one(temp_words_list3)

        received_words_list = self.scraper.get_words_list_from_db()
        self.assertEqual([temp_words_list1, temp_words_list2, temp_words_list4, temp_words_list5],
                         received_words_list)

    def test_update_words_list_from_db_with_only_one(self):

        temp_words_list = {"_id": 1, "casa": 5, "mesa": 3, "patata": 2}
        self.scraper.db.words.insert_one(temp_words_list)
        self.scraper.db.words.update_one({"casa": 5}, {"$inc": {"casa": 1}})
        expected_words_list = {"_id": 1, "casa": 6, "mesa": 3, "patata": 2}

        mock = Mock()
        mock(self.scraper.db.words.update_one, {"casa": 5}, {"$inc": {"casa": 1}})
        received_words_list = self.scraper.get_words_list_from_db()

        self.assertEqual([expected_words_list], received_words_list)

    def test_update_words_list_from_db_with_two_lists(self):

        temp_words_list1 = {"_id": 1, "casa": 5, "mesa": 3, "patata": 2}
        temp_words_list2 = {"_id": 2, "casa": 5, "mesa": 3, "patata": 2, "tomate": 4}
        self.scraper.db.words.insert_one(temp_words_list1)
        self.scraper.db.words.insert_one(temp_words_list2)
        self.scraper.db.words.update_one({"_id": 1, "casa": 5}, {"$inc": {"casa": 1}})
        self.scraper.db.words.update_one({"_id": 2, "tomate": 4}, {"$inc": {"tomate": 2}})
        expected_words_list1 = {"_id": 1, "casa": 6, "mesa": 3, "patata": 2}
        expected_words_list2 = {"_id": 2, "casa": 5, "mesa": 3, "patata": 2, "tomate": 6}

        received_words_list = self.scraper.get_words_list_from_db()

        self.assertEqual([expected_words_list1, expected_words_list2], received_words_list)

    def test_update_words_list_from_db_with_multiple_lists(self):

        temp_words_list1 = {"_id": 1, "casa": 5, "mesa": 3, "patata": 2}
        temp_words_list2 = {"_id": 2, "casa": 4, "mesa": 2, "patata": 2, "tomate": 4}
        temp_words_list3 = {"_id": 3, "casa": 3, "mesa": 3, "tomate": 4}
        temp_words_list4 = {"_id": 4, "casa": 2, "mesa": 2, "patata": 2, "tomate": 7}
        temp_words_list5 = {"_id": 5, "casa": 1, "patata": 2, "tomate": 4}
        self.scraper.db.words.insert_one(temp_words_list1)
        self.scraper.db.words.insert_one(temp_words_list2)
        self.scraper.db.words.insert_one(temp_words_list3)
        self.scraper.db.words.insert_one(temp_words_list4)
        self.scraper.db.words.insert_one(temp_words_list5)
        self.scraper.db.words.update_one({"_id": 1, "casa": 5}, {"$inc": {"casa": 1}})
        self.scraper.db.words.update_one({"_id": 2, "tomate": 4}, {"$inc": {"tomate": 1}})
        self.scraper.db.words.update_one({"_id": 4, "patata": 2}, {"$inc": {"patata": -1}})
        expected_words_list1 = {"_id": 1, "casa": 6, "mesa": 3, "patata": 2}
        expected_words_list2 = {"_id": 2, "casa": 4, "mesa": 2, "patata": 2, "tomate": 5}
        expected_words_list3 = {"_id": 3, "casa": 3, "mesa": 3, "tomate": 4}
        expected_words_list4 = {"_id": 4, "casa": 2, "mesa": 2, "patata": 1, "tomate": 7}
        expected_words_list5 = {"_id": 5, "casa": 1, "patata": 2, "tomate": 4}

        received_words_list = self.scraper.get_words_list_from_db()

        self.assertEqual([expected_words_list1, expected_words_list2, expected_words_list3, expected_words_list4,
                          expected_words_list5], received_words_list)

    def test_save_words_in_db_if_not_exists_yet(self):
        self.scraper.exists_in_db = Mock(return_value=True)
        # If we can insert, the returned value from save function must be different from None value
        self.assertIsNotNone(self.scraper.save_words_in_db({"dinero": 1000000}))

    def test_save_words_in_db_if_exists_already(self):
        self.scraper.exists_in_db = Mock(return_value=False)
        self.assertIsNone(self.scraper.save_words_in_db({"dinero": 1000000}))

    def test_save_words_in_db_is_int(self):
        self.assertEqual(self.scraper.save_words_in_db(3), errno.EINVAL)

    def test_save_words_in_db_is_bool(self):
        self.assertEqual(self.scraper.save_words_in_db(True), errno.EINVAL)

    def test_save_words_in_db_is_string(self):
        self.assertEqual(self.scraper.save_words_in_db("Ordenador"), errno.EINVAL)

