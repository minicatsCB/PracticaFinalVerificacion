from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def hello():
	return render_template('form.html')

@app.route('/', methods = ['POST'])
def signup():
	if request.method == 'POST':
		# First, obtain the introduced text through the form
		result = request.form
		text_to_analyze = result['textArea']
		# Proccess the text
		words = "Hola desde 'form.py'!"
		print words
		# Pass the text to the template in order to be showed in the screen
		return render_template('form.html', result = words)


if __name__ == "__main__":
	app.run(debug = True)
