from flask import render_template, Flask, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
import gen_cards


app = Flask(__name__)
app.secret_key = "SuperS3cret"

class TextInputForm(FlaskForm):
    text_input = TextAreaField('Enter Text:')
    submit = SubmitField('Submit')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/')
def index():
    with open("./input.txt", 'r') as f:
        data = f.readlines()

    data = [i.strip() for i in data]
    variable_list = gen_cards.GenText(data)

    color_list, blue = gen_cards.GenColors()# True = Blue, False = red

    card_list = [ Card(name, color_list[key]) for key, name in enumerate(variable_list)]

    return render_template('SKUA.html', variable_list=card_list, blue=blue)

@app.route('/testin')
def indexin():
    data = session['saved_text'].split(" ")
    print(data)

    data = [i.strip() for i in data]
    print(data)
    variable_list = gen_cards.GenText(data)

    color_list, blue = gen_cards.GenColors()# True = Blue, False = red

    card_list = [ Card(name, color_list[key]) for key, name in enumerate(variable_list)]

    return render_template('SKUA.html', variable_list=card_list, blue=blue)

@app.route('/input', methods=['GET', 'POST'])
def inpp():
    form = TextInputForm()
    print(session['saved_text'])

    if form.validate_on_submit():
        text_input = form.text_input.data
        # Save the input text to the session
        session['saved_text'] = text_input
        return indexin()

    return render_template('input.html', form=form, saved_text=session.get('saved_text', ''))


class Card():
    def __init__(self, name, color):
        self.Color = color
        self.Name = name


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)