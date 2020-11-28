from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required

types = [ 'Other', 'Driver', 'Wood', '3-wood', '5-wood', 'Hybrid', '3-hybrid', '5-hybrid', 'Iron', '2-iron', '3-iron', '4-iron', '5-iron',
          '6-iron', '7-iron', '8-iron', '9-iron', 'Wedge', 'Pitching wedge', 'Approach wedge', 'Sand wedge', 'Lob wedge', 'Putter' ]
noUserClubs = []

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.sqlite'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "hgbh9dfgh432bf98y4bnfd8oyvoubh4098fydsvojbnwereg98ydsvojbne"
login_manager = LoginManager(app)
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    clubs = db.relationship('Club', backref='user', lazy=True)

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(40))
    type = db.Column(db.String(10))
    shaft = db.Column(db.String(10))
    flex = db.Column(db.String(15))
    degree = db.Column(db.Float)
    yards = db.Column(db.Integer)
    extra = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def home():
    Login = "Sign In"
    if current_user.is_authenticated:
        Login = "Sign Out"
    return render_template('home.html', login=Login)

@app.route('/add')
def add():
    Login = "Sign In"
    if current_user.is_authenticated:
        Login = "Sign Out"
    return render_template('add.html', login=Login, types=types)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    wrong = False
    wasSignUp = False
    if current_user.is_authenticated:
        return render_template('logout.html', login="Sign Out")
    if request.method == 'POST':
        try:
            if request.form['newusername'] != None:
                wasSignUp = True
                user = User(username=request.form['newusername'], password=request.form['newpassword'], name=request.form['name'])
                if User.query.filter_by(username=user.username).first() == None:
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('home'))
                else:
                    wrong = True
        except:
            user = User.query.filter_by(username=request.form['username']).first()
            if user != None and user.password == request.form['password']:
                login_user(user)
                return redirect(url_for('home'))
            else:
                wrong = True
    return render_template('login.html', login="Sign In", wrong=wrong, wasSignUp=wasSignUp)

@app.route('/update/<i>', methods=['GET','POST'])
def update(i):
    Login = "Sign In"
    if current_user.is_authenticated:
        Login = "Sign Out"
        club = Club.query.filter_by(id=i).first()
        print(club.extra)
        if request.method == 'POST':
            club.brand = request.form['name']
            club.type = request.form['type']
            club.flex = request.form['flex']
            club.shaft = request.form['shaft']
            club.degree = float(request.form['degree'])
            club.extra = request.form['extra']
            club.yards = int(request.form['yards'])
            db.session.commit()
            return redirect(url_for('read'))
    else:
        club = noUserClubs[int(i)]
        if request.method == 'POST':
            club.brand = request.form['name']
            club.type = request.form['type']
            club.flex = request.form['flex']
            club.shaft = request.form['shaft']
            club.degree = float(request.form['degree'])
            club.extra = request.form['extra']
            club.yards = int(request.form['yards'])
            return redirect(url_for('read'))
    return render_template('update.html', club=club, i=i, login=Login, types=types)

@app.route('/view/<i>')
def view(i):
    Login = "Sign In"
    name = "You"
    if current_user.is_authenticated:
        Login = "Sign Out"
        name = current_user.name
        club = Club.query.filter_by(id=i).first()
        if club == None:
            abort(404)
    else:
        if int(i) >= len(noUserClubs):
            abort(404)
        club = noUserClubs[int(i)]
        print(club.extra)
    return render_template('view.html', club=club, i=i, login=Login, types=types, name=name)

@app.route('/delete/<i>')
def delete(i):
    if current_user.is_authenticated:
        club = Club.query.filter_by(id=i).first()
        db.session.delete(club)
        db.session.commit()
    else:
        noUserClubs.remove(noUserClubs[int(i)])
    return redirect(url_for('read'))

@app.route('/read', methods=['GET','POST'])
def read():
    Login = "Sign In"
    if current_user.is_authenticated:
        Login = "Sign Out"
        if len(noUserClubs) > 0:
            for c in noUserClubs:
                c.user = current_user
                c.id = None
                db.session.add(c)
                noUserClubs.remove(c)
                db.session.commit()
            read()
        if request.method == 'POST':
            words = ""
            for line in request.form.getlist('extra'):
                words += line.replace("\r", " ").replace("\n", "")
            club = Club(brand=request.form['name'], type=request.form['type'], extra=words, shaft=request.form['shaft'],
                        flex=request.form['flex'], degree=float(request.form['degree']), yards=int(request.form['yards']), user=current_user)
            db.session.add(club)
            db.session.commit()
        clubs = Club.query.filter_by(user=current_user).all()
    else:
        if request.method == 'POST':
            words = ""
            for line in request.form.getlist('extra'):
                words += line.replace("\r", " ").replace("\n", "")
            club = Club(brand=request.form['name'], type=request.form['type'], extra=words, shaft=request.form['shaft'],
                        flex=request.form['flex'], degree=float(request.form['degree']),
                        yards=int(request.form['yards']))
            club.id = len(noUserClubs)
            noUserClubs.append(club)
        clubs = noUserClubs
    return render_template('read.html', clubs=clubs, login=Login)

@app.errorhandler(404)
def error(err):
    Login = "Sign In"
    if current_user.is_authenticated:
        Login = "Sign Out"
    return render_template('error.html', err=err, login=Login)

@app.errorhandler(401)
def error(err):
    Login = "Sign In"
    if current_user.is_authenticated:
        Login = "Sign Out"
    return render_template('error.html', err=err, login=Login)


if __name__ == '__main__':
    app.run(debug=True)