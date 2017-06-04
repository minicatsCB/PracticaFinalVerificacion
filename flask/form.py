# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import feedparser
from CountWords import CountWords
from flask_pymongo import PyMongo
import datetime  # For getting current date


app = Flask(__name__)
mongo = PyMongo(app)

# connect to another MongoDB database on the same host
app.config['MONGO2_DBNAME'] = 'analysis'
mongo2 = PyMongo(app, config_prefix='MONGO2')


@app.route('/')
def root():
	# Get all possible values for dates (as they are saved in database)
	dates = mongo.db.words.distinct('date')
	return render_template('form.html', dates = dates)


@app.route('/processForm', methods = ['GET', 'POST'])
def execute():
	if request.method == 'POST':
		# Obtain the introduced text through the form
		required_date = request.form['publication-date']

		# If the user want today articles, check if they are already in database
		# Only get them from RSS if they are not saved yet in database
		if(required_date == "today"):
			# Get current date (it can't be the string "today")
			required_date = str(datetime.datetime.now())[0:10]
			if(mongo.db.words.find_one({'date': required_date}) is None):
				# Get data from the RSS service (returns multiple items)
				d = feedparser.parse('http://www.20minutos.es/rss/')

				# Save articles to database
				for item in range(len(d)):
					text = d.entries[item].summary # type: unicode

					mongo.db.words.insert({'text': text, 'date': required_date})

		# If the user want older articles, get them from database
		result = mongo.db.words.find({'date': required_date})

		# Analyze each article
		list_to_show = []
		for doc in result:
			cw = CountWords(doc['text'])
			count_result = cw.text_analyzer()
			list_to_show.append(count_result)

		# Now that we have ALL articles analysis for the required date,
		# convert each article analysis to a dictionary (not sorted)
		all_dictionaries = []
		for i in range(len(list_to_show)):
			# New dictionary for the new article
			all_dictionaries.append({})
			# New article
			for j in range(len(list_to_show[i])):
				all_dictionaries[i].update({list_to_show[i][j][0]: list_to_show[i][j][1]})
		
		# Save all dictionaries in a different database, if they are not saved yet
		if(mongo2.db.words.find_one({'date': required_date}) is None):
			for i in range(len(all_dictionaries)):
				for j in range(len(all_dictionaries[i].keys())):
					# Create a document with two fields inside 'count' field: "word" and "number"
					# Do not differentiate articles, but do dates
					mongo2.db.words.insert({'date': required_date, 'count': {'word': all_dictionaries[i].keys()[j], 'number': all_dictionaries[i].values()[j]}})

		# Get top used words for the required date (sorted)
		pipeline = [{"$match": {"date": required_date}}, 
		{"$unwind": "$count"}, 
		{"$group": {"_id": "$count.word", "total_number": {"$sum": "$count.number"}}}, 
		{"$sort": {"total_number": -1}}, 
		{"$limit": 5}]
		aggregate = list(mongo2.db.words.aggregate(pipeline))

		# Get all possible values for dates (as they are saved in database)
		dates = mongo.db.words.distinct('date')

		# Pass the top used words to the template in order to be showed in the screen
		return render_template('form.html',  dates = dates, result = aggregate)


if __name__ == "__main__":
	app.run(debug = True)

