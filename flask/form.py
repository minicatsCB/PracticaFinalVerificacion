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
		date = result['publication-date']

		# Get data from the RSS service
		d = feedparser.parse('http://www.20minutos.es/rss/')
		text = d.entries[0].summary

		# Encode text to ASCII before analyzing it
		text = text.encode('ascii', 'ignore')

		# Analyze it
		cw = CountWords(text)
		sorted_list = cw.text_analyzer()
		print(sorted_list)
		
		# Save the result to database
		mongo.db.words.insert({'count': sorted_list})

		# Pass the text to the template in order to be showed in the screen
		return render_template('form.html', result = sorted_list);


if __name__ == "__main__":
	app.run(debug = True)
