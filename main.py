from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/test'
db = SQLAlchemy(app)

# 定义用户模型


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# 创建数据库表
with app.app_context():
    db.create_all()

# 开始界面


@app.route('/')
def home():
    return render_template('home.html')

# 登录界面


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash('登录成功！', 'success')
            return redirect(url_for('home'))
        else:
            flash('登录失败，请检查用户名和密码。', 'danger')
    return render_template('login.html')

# 注册界面


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在，请选择其他用户名。', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
