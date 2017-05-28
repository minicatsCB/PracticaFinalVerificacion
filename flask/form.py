# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import feedparser
import unicodedata
from CountWords import CountWords
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def hello():
	# Get all possible values for dates (as the are saved in database)
	dates = mongo.db.words.distinct('date')
	return render_template('form.html', dates = dates)

@app.route('/processForm', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		# First, obtain the introduced text through the form
		required_date = request.form['publication-date']
		#required_date = '2017-05-28'

		# Get data from the RSS service
		d = feedparser.parse('http://www.20minutos.es/rss/')

		for item in range(len(d)):
			text = d.entries[item].summary # type: unicode
			date = d.entries[item].updated[0:10] # type: unicode

			# Save the result to database
			mongo.db.words.insert({'text': text, 'date': date})

			# Encode text to ASCII before analyzing it
			#text = text.encode('ascii', 'ignore')

		result = mongo.db.words.find({'date': required_date}) # Aquí es donde habria que decirle que busque por fecha

		# Analyze it
		list_to_show = []
		for doc in result:
			cw = CountWords(doc['text'])
			list_to_show.append(cw.text_analyzer()[0:6])  # Show only top used words
		'''
		for i in range(len(result)):
			result[i][1] = result[i][1].encode('ascii', 'ignore')
		'''
		# Pass the text to the template in order to be showed in the screen
		return render_template('form.html', result = list_to_show);


if __name__ == "__main__":
	app.run(debug = True)
