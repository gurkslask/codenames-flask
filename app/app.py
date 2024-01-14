from flask import render_template, Flask
import gen_cards


app = Flask(__name__)
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

class Card():
    def __init__(self, name, color):
        self.Color = color
        self.Name = name


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)