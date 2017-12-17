from flask import Flask, render_template, flash, redirect, url_for, g, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DecimalField, DateField
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.fields import DateField
import pandas as pd

# APP creation
app = Flask(__name__)


#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'motorockr'
app.config['MYSQL_DB'] = 'flask_mankatoexpenses'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initialize database
mysql = MySQL(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

#Wrap session
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
        	flash('Not logged in, Please login first.','danger')
        	return redirect(url_for('login'))
    return wrap

#Route to dashboard
@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')


# Resister form
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Password do not mathc')
		])
	confirm = PasswordField('Confirm Password')

#Registration
@app.route('/register', methods= ['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#create a cursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

		#commit
		mysql.connection.commit()

		#close cursor
		cur.close()

		flash('Resistration Successful!', 'success')
		redirect(url_for('index'))
	return render_template('register.html', form=form)


#Login
@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		#Get data from login form
		#name = request.form['name']
		username = request.form['username']
		form_pass = request.form['password']

		#login cursor
		cur = mysql.connection.cursor()
		cur_2 = mysql.connection.cursor()
		#Get username
		name = cur_2.execute("select name from users where username = %s", ([username]))
		result = cur.execute("select username, password from users where username = %s", ([username]))

		if result > 0:
			#get stored hash
			data = cur.fetchone()
			users_name = cur_2.fetchone()
			user_pass = data['password']
			#Compare pass
			if sha256_crypt.verify(form_pass, user_pass):
				session['logged_in'] = True
				session['username'] = username
				session['nickname'] = users_name

				flash('Welcome', 'success')
				return redirect(url_for('dashboard'))
				#return render_template('index.html')
			else:
				error = 'Login failed.'
				return render_template('login.html', error=error)				

		else:
			error = 'User not found.'
			return render_template('login.html', error=error)

	return render_template('login.html')

#Logout
@app.route('/logout')
def logout():
	session.clear()
	flash('You are logged', 'success')
	return redirect(url_for('login'))

# Transaction Entry form
class TransactionForm(Form):
	comment = TextAreaField('comment', [validators.Length(min=3, max=200)])
	entry_date = DateField('entry_date', format='%m/%d/%Y') 
	#DateField('entry_date', format='%y/%m/%d')
	item = StringField('item', [validators.Length(min=4, max=101)])
	payer = StringField('payer', [validators.Length(min=3, max=51)])
	amount = DecimalField('amount')
	status = StringField('status', [validators.Length(min=1, max=15)])

#Transaction form
@app.route('/trans_form', methods= ['GET', 'POST'])
@login_required
def TransactionEntry():
	form = TransactionForm(request.form)
	if request.method == 'POST' and form.validate():
		comment = form.comment.data
		entry_date = form.entry_date.data
		item = form.item.data
		payer = form.payer.data
		amount = form.amount.data
		status = form.status.data

		#create a cursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO transaction(entry_date, comment, item, payer, amount, status) VALUES(%s, %s, %s, %s, %s, %s)", (entry_date, comment, item, payer, amount, status))

		#commit
		mysql.connection.commit()

		#close cursor
		cur.close()

		flash('Record inserted!', 'success')
		redirect(url_for('TransactionEntry'))
	return render_template('transaction_form.html', form=form)

#Transactions
@app.route('/trans_view')
@login_required
def tran_view():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM transaction")

	data = cur.fetchall()

	if result > 0:
		return render_template('transactions.html', data=data)
	else:
		msg = 'No data found.'
		return render_template('transactions.html', msg=msg)

	#close conn
	cur.close()

# #Mysql To Dataframe
# @app.route('/df')
# @login_required
# def df():
# 	cur = mysql.connection.cursor()
# 	df = pd.read_sql('select * from transaction', con = MySQL(app))

# 	return render_template('df.html')

if __name__ == '__main__':
	app.secret_key = 'lenovoideapad123456789'
	app.run(debug=True)