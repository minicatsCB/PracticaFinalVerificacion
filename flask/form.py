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
	return render_template('form.html')

@app.route('/processForm', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		# First, obtain the introduced text through the form
		result = request.form
		required_date = result['publication-date']

		# Get data from the RSS service
		d = feedparser.parse('http://www.20minutos.es/rss/')

		for item in range(len(d)):
			text = d.entries[item].summary # type: unicode
			date = d.entries[item].updated[0:10] # type: unicode

			# Encode text to ASCII before analyzing it
			#text = text.encode('ascii', 'ignore')

			# Analyze it
			cw = CountWords(text)
			sorted_list = cw.text_analyzer()
		
			# Save the result to database
			mongo.db.words.insert({'count': sorted_list, 'date': date})
			
		result = mongo.db.words.find({'date': '2017-05-28'}) # Aquí es donde habria que decirle que busque por fecha
		'''
		for i in range(len(result)):
			result[i][1] = result[i][1].encode('ascii', 'ignore')
		'''
		#print(result[0]['count'][0:6])
		# Show only top used words
		list_to_show = []
		for doc in result:
			list_to_show.append(doc['count'][0:6])
		# Pass the text to the template in order to be showed in the screen
		return render_template('form.html', result = list_to_show);


if __name__ == "__main__":
	app.run(debug = True)
