import pymongo
import pprint
from bson.son import SON

def palabrasMasUsadas(fecha):
	pipeline = [{"$match": {"date": fecha}}, 
	{"$unwind": "$count"}, 
	{"$group": {"_id": "$count.word", "total_number": {"$sum": "$count.number"}}}, 
	{"$sort": {"total_number": -1}}, 
	{"$limit": 5})]
	pprint.pprint(list(db.cities.aggregate(pipeline)))