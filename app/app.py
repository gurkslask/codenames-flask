from flask import render_template, Flask, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
import json
import gen_cards
import db


app = Flask(__name__)
app.secret_key = "SuperS3cret"
dbCon, dbCur = db.initDB()

class TextInputForm(FlaskForm):
    text_input = TextAreaField('Enter Text:')
    submit = SubmitField('Submit')
    
class CreateNewForm(FlaskForm):
    listname = TextAreaField('Name of list')
    words = TextAreaField('Words')
    submit = SubmitField('Submit')
    
@app.route('/createnew/', methods=['GET', 'POST'])
def createnew():
    # return render_template('create_new.html')
    form = CreateNewForm()

    if form.validate_on_submit():
        listname = form.listname.data
        words = form.words.data
        # Save the input text to the session
        # session['saved_text'] = text_input
        # return indexin()
        print(f"{listname}")
        words = gen_cards.FixInput(words)
        print(f"{words}")
        db.InsertList(listname, dbCon, dbCur)
        for word in words:
            db.InsertWord(word, listname, dbCon, dbCur)
        return lists()

    return render_template('createnew.html', form=form)

@app.route('/lists/')
def lists(listnames=None):
    listnames = db.GetLists(dbCon, dbCur)
    return render_template('lists.html', listnames=listnames)

@app.route('/wordsinlist/')
@app.route('/wordsinlist/<name>')
def wordsinlist(name=None):
    print('hej')
    names = db.GetWordsFromList(name, dbCon, dbCur)
    return render_template('wordsinlist.html', names=names, listname=name)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/playtest')
def playtest():
    with open("./input.txt", 'r') as f:
        data = f.readlines()

    data = [i.strip() for i in data]
    variable_list = gen_cards.GenText(data)

    color_list, blue = gen_cards.GenColors()# True = Blue, False = red

    card_list = [ Card(name, color_list[key]) for key, name in enumerate(variable_list)]
    session['card_list'] = [c.toJson() for c in card_list]
    session['blue'] = blue

    return render_template('SKUA.html', variable_list=card_list, blue=blue)

@app.route('/playmap/')
def playmap():
    card_list = session['card_list']
    card_list = [json.loads(c) for c in card_list]
    blue = session['blue']

    return render_template('SKUA_map.html', variable_list=card_list, blue=blue)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testin')
def indexin():
    data = gen_cards.FixInput(session['saved_text'])
    print(data)

    #data = [i.strip() for i in data]
    print(data)
    variable_list = gen_cards.GenText(data)

    color_list, blue = gen_cards.GenColors()# True = Blue, False = red

    card_list = [ Card(name, color_list[key]) for key, name in enumerate(variable_list)]

    session['card_list'] = [c.toJson() for c in card_list]
    session['blue'] = blue
    return render_template('SKUA.html', variable_list=card_list, blue=blue)

@app.route('/play/<name>')
def play(name=None):
    data = db.GetWordsFromList(name, dbCon, dbCur)
    print(data)

    #data = [i.strip() for i in data]
    print(data)
    variable_list = gen_cards.GenText(data)

    color_list, blue = gen_cards.GenColors()# True = Blue, False = red

    card_list = [ Card(name, color_list[key]) for key, name in enumerate(variable_list)]

    session['card_list'] = [c.toJson() for c in card_list]
    session['blue'] = blue
    return render_template('SKUA.html', variable_list=card_list, blue=blue)

@app.route('/input', methods=['GET', 'POST'])
def inpp():
    form = TextInputForm()

    if form.validate_on_submit():
        text_input = form.text_input.data
        # Save the input text to the session
        session['saved_text'] = text_input
        return indexin()

    return render_template('input.html', form=form, saved_text=session.get('saved_text', ''))

@app.route('/rules')
def rules():
    return render_template('rules.html')


class Card():
    def __init__(self, name, color):
        self.Color = color
        self.Name = name
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
