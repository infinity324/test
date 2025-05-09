from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/test'
db = SQLAlchemy(app)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            logger.info(f"用户 {username} 登录成功")
            return redirect(url_for('home'))
        else:
            flash('登录失败，请检查用户名和密码。', 'danger')
            logger.warning(f"用户 {username} 登录失败")
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
            logger.warning(f"用户名 {username} 已存在")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！', 'success')
            logger.info(f"用户 {username} 注册成功")
            return redirect(url_for('login'))
    return render_template('register.html')

# 显示日志接口


@app.route('/logs')
def show_logs():
    with open('app.log', 'r') as log_file:
        logs = log_file.read()
    return logs


# main
# 1
if __name__ == '__main__':
    app.run(debug=True, port=8080)
