from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Newblog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id_a = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Article %r' % self.id_a


class People(db.Model):
    id_f = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    story = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<People %r' % self.id_f


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/about')
def about():
    articles = Article.query.all()
    return render_template('about.html', articles=articles)


@app.route('/about/<int:id_a>')
def post(id_a):
    article = Article.query.get(id_a)
    return render_template('post.html', article=article)


@app.route('/add_about', methods=['POST', 'GET'])
def add_about():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/about')
        except:
            return "Ой! Что-то пошло не так!"
    else:
        return render_template('add_about.html')


@app.route('/about/<int:id_a>/update_post', methods=['POST', 'GET'])
def update_post(id_a):
    article = Article.query.get(id_a)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/about')
        except:
            return "Ошибка при редактировании статьи"
    else:
        return render_template("update_post.html", article=article)


@app.route('/about/<int:id_a>/delete_post')
def delete_post(id_a):
    article = Article.query.get_or_404(id_a)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/about')
    except:
        return "Ошибка при удалении статьи"


@app.route('/friends')
def friends():
    friend = People.query.all()
    return render_template('friends.html', friend=friend)


@app.route('/add_friends', methods=['POST', 'GET'])
def add_friends():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        story = request.form['story']

        friend = People(name=name, age=age, story=story)

        try:
            db.session.add(friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "Ой! Что-то пошло не так!"
    else:
        return render_template('add_friends.html')


@app.route('/friends/<int:id_f>/update_friend', methods=['POST', 'GET'])
def update_friend(id_f):
    friend = People.query.get(id_f)
    if request.method == 'POST':
        friend.name = request.form['name']
        friend.age = request.form['age']
        friend.story = request.form['story']

        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "Ошибка при редактировании"
    else:
        return render_template("update_friend.html", friend=friend)


@app.route('/friends/<int:id_f>/delete_friend')
def delete_friend(id_f):
    friend = People.query.get_or_404(id_f)

    try:
        db.session.delete(friend)
        db.session.commit()
        return redirect('/friends')
    except:
        return "Ошибка при удалении статьи"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
