# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import feedparser
import unicodedata
from CountWords import CountWords
from flask_pymongo import PyMongo
import pprint

app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def hello():
	# Get all possible values for dates (as they are saved in database)
	dates = mongo.db.words.distinct('date')
	return render_template('form.html', dates = dates)

@app.route('/processForm', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		# Obtain the introduced text through the form
		required_date = request.form['publication-date']
		#required_date = '2017-06-02'  # To update

		# Get data from the RSS service (returns multiple items)
		d = feedparser.parse('http://www.20minutos.es/rss/')

		# Save articles to database
		for item in range(len(d)):
			text = d.entries[item].summary # type: unicode
			date = d.entries[item].updated[0:10] # type: unicode

			#mongo.db.words.insert({'text': text, 'date': date})

			# Encode text to ASCII before analyzing it
			#text = text.encode('ascii', 'ignore')

		result = mongo.db.words.find({'date': required_date}) # Aquí es donde habria que decirle que busque por fecha

		# Analyze each article
		list_to_show = []
		for doc in result:
			cw = CountWords(doc['text'])
			count_result = cw.text_analyzer()
			list_to_show.append(count_result)  # Show only top used words. (Optional: [:])

		
		# list_to_show tiene todos los recuentos de palabras de todos los articulos.
		# Convert it to dictionary (not sorted)
		all_dictionaries = []
		for i in range(len(list_to_show)):
			# New dictionary for the new article
			all_dictionaries.append({})
			# New article
			for j in range(len(list_to_show[i])):
				all_dictionaries[i].update({list_to_show[i][j][0]: list_to_show[i][j][1]})
		'''
		for i in range(len(all_dictionaries)):
			for j in range(len(all_dictionaries[i].keys())):
				#mongo.db.words.insert({'date': date, 'count': all_dictionaries[i]}) # Inserta todo dentro de 'count' para cada noticia
				mongo.db.words.insert({'date': date, 'count': {'word': all_dictionaries[i].keys()[j], 'number': all_dictionaries[i].values()[j]}}) # Crea un documento palabra número dentro de 'count' (mejorar para que guarde por cada noticia)

		'''
		required_date = "2017-06-02"
		print(required_date)
		# Consulta
		pipeline = [{"$match": {"date": required_date}}, 
		{"$unwind": "$count"}, 
		{"$group": {"_id": "$count.word", "total_number": {"$sum": "$count.number"}}}, 
		{"$sort": {"total_number": -1}}, 
		{"$limit": 5}]
		aggregate = list(mongo.db.words.aggregate(pipeline))

		

		'''
		for i in range(len(result)):
			result[i][1] = result[i][1].encode('ascii', 'ignore')
		'''
		# Pass the text to the template in order to be showed in the screen
		return render_template('form.html', result = aggregate);


if __name__ == "__main__":
	app.run(debug = True)
