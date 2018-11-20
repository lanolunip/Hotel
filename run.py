from flask import Flask, render_template

app = Flask(__name__)


author = {
    'name'    :   'Michael',
    'age'       :   '19',
    'address'   :   'Kanser.11'
}


@app.route('/')
def hello():
    return render_template('home.html',author=author,title='IKI HOME TA ??')

@app.route('/1')
def makudonarudo():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)