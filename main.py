from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from random import randint

cart_dict={}

order_id=''
cart_quantity={}
msg=''
item_dict={}
ord_id=00000
num=0
flag=0
id_list=set()
def get_restaurant(item_id):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM menu WHERE item_id = %s', [item_id])
	restaurant=cursor.fetchone()
	cursor.execute('SELECT * FROM restaurant WHERE restaurant_id = %s', [restaurant['Restaurant_id']])
	res_name=cursor.fetchone()
	return restaurant['Restaurant_id'],res_name['Restaurant_Name']




#generate unique id
def unique_id():
	return randint(10000,99999)




app = Flask(__name__)

# Intialize MySQL
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'shravya'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'foodify1'

app.secret_key = '123!@#123'




@app.route('/')
def main():

	return render_template('main.html')
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/Employee',methods=['GET'])
def Employee():
	return render_template('employee.html')
@app.route('/employeeDetails',methods=['GET','POST'])
def EmployeeDetails():
	if 'emp_id' in request.form:
		employee_id=request.form['emp_id']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM employee WHERE employee_id = %s', [employee_id])
		emp_account=cursor.fetchone()
		cursor.execute('SELECT no_of_orders FROM employee WHERE employee_id = %s',[employee_id])
		count=cursor.fetchone()
	return render_template('employee_details.html',emp_account=emp_account,count=count['no_of_orders'])	




@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		# Create variables for easy access
		username = request.form['username']
		password = request.form['password']
		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM customer WHERE username = %s AND password = %s', (username, password))
		# Fetch one record and return result
		account = cursor.fetchone()
		# If account exists in accounts table in out database
		if account:
			# Create session data, we can access this data in other routes
			session['loggedin'] = True
			session['username'] = account['username']
			# Redirect to home page
			cart_dict.clear()
			cart_quantity.clear()
			return redirect(url_for('home'))
		else:
			# Account doesnt exist or username/password incorrect
			msg = 'Incorrect username/password!'
	return render_template('login.html',msg='')


@app.route('/register',methods=['GET', 'POST'])
def register():
	msg = ''
	# Check if "username", "password" and "email" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password1' in request.form and 'email' in request.form:
		# Create variables for easy access
		username = request.form['username']
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		password1 = request.form['password1']
		pass_len=len(password1)
		password2 = request.form['password2']
		email = request.form['email']
		address=request.form['address']
		dob=request.form['dob']
		contact_number=request.form['contact_number']
		cno_len=len(contact_number)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM customer WHERE username = %s', [username])
		account = cursor.fetchone()
		# If account exists show error and validation checks
		if account:
			msg = 'Account already exists!'
		elif pass_len<5:
			msg = 'Password too short!'
		elif password1.isdigit()==True or password1.isalpha()==True:
			msg='Password should contain both letters and digits..'
		elif cno_len != 10 or contact_number.isdigit()==False:
			msg='Invalid contact number'

		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address!'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers!'
		elif not username or not password1 or not email:
			msg = 'Please fill out the form!'
		elif password1 != password2:
			msg = 'Confirm password not matching'

		else:
			# Account doesnt exists and the form data is valid, now insert new account into accounts table
			cursor.execute('INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (username, firstname, lastname,password1,email,address,dob,contact_number))
			mysql.connection.commit()
			msg = ''
			return render_template('login.html',msg='')
	elif request.method == 'POST':
		# Form is empty... (no POST data)
		msg = 'Please fill out the form!'
	# Show registration form with message (if any)

	return render_template('sign_up.html', msg=msg)


@app.route('/login/logout')
def logout():
	# Remove session data, this will log the user out
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
   # Redirect to login page
	cart_dict.clear()
	cart_quantity.clear()
	return redirect(url_for('main'))

@app.route('/home')
def home():

	if 'loggedin' in session:
		# User is loggedin show them the home page
		return render_template('foodify_home.html', username=session['username'])
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))
@app.route('/dominos_menu')
def dominos():
	if 'loggedin' in session:
		return render_template('dominos_menu.html',username=session['username'],cart_dict=cart_dict)

@app.route('/add_to_cart',methods=['POST'])
def add_to_cart():
		if 'DOM002' in request.form:
			if 'DOM002' in cart_dict:
				cart_quantity["DOM002"]=cart_quantity["DOM002"]+1
			else:
				cart_dict["DOM002"]=235
				cart_quantity["DOM002"]=1
		elif "DOM001" in request.form:
			if 'DOM001' in cart_dict:
				cart_quantity['DOM001']=cart_quantity['DOM001']+1
			else:
				cart_dict['DOM001']=195
				cart_quantity["DOM001"]=1
		elif "DOM003" in request.form:
			if 'DOM003' in cart_dict:
				cart_quantity['DOM003']=cart_quantity['DOM003']+1
			else:
				cart_dict['DOM003']=99
				cart_quantity["DOM003"]=1
		elif "DOM004" in request.form:
				
			if 'DOM004' in cart_dict:
				cart_quantity['DOM004']=cart_quantity['DOM004']+1
			else:
				cart_dict['DOM004']=250
				cart_quantity["DOM004"]=1
		elif "DOM005" in request.form:
			if 'DOM005' in cart_dict:
				cart_quantity['DOM005']=cart_quantity['DOM005']+1
			else:	
				cart_dict['DOM005']=300
				cart_quantity["DOM005"]=1
		elif "DOM006" in request.form:
			if 'DOM006' in cart_dict:
				cart_quantity['DOM006']=cart_quantity['DOM006']+1
			else:
				cart_dict['DOM006']=199
				cart_quantity["DOM006"]=1
		elif 'MCD001' in request.form:
			if 'MCD001' in cart_dict:
				cart_quantity["MCD001"]=cart_quantity["MCD001"]+1
			else:
				cart_dict["MCD001"]=70
				cart_quantity["MCD001"]=1
		elif "MCD002" in request.form:
			if 'MCD002' in cart_dict:
				cart_quantity['MCD002']=cart_quantity['MCD002']+1
			else:
				cart_dict['MCD002']=212
				cart_quantity["MCD002"]=1
		elif "MCD003" in request.form:
			if 'MCD003' in cart_dict:
				cart_quantity['MCD003']=cart_quantity['MCD003']+1
			else:
				cart_dict['MCD003']=25
				cart_quantity["MCD003"]=1
		elif "MCD004" in request.form:
				
			if 'MCD004' in cart_dict:
				cart_quantity['MCD004']=cart_quantity['MCD004']+1
			else:
				cart_dict['MCD004']=120
				cart_quantity["MCD004"]=1
		elif "MCD005" in request.form:
			if 'DOM005' in cart_dict:
				cart_quantity['MCD005']=cart_quantity['MCD005']+1
			else:	
				cart_dict['MCD005']=262
				cart_quantity["MCD005"]=1
		elif "MCD006" in request.form:
			if 'MCD006' in cart_dict:
				cart_quantity['MCD006']=cart_quantity['MCD006']+1
			else:
				cart_dict['MCD006']=120
				cart_quantity["MCD006"]=1
		elif "COR001" in request.form:
			if 'COR001' in cart_dict:
				cart_quantity['COR001']=cart_quantity['COR001']+1
			else:
				cart_dict['COR001']=211
				cart_quantity["COR001"]=1
		elif "COR002" in request.form:
			if 'COR002' in cart_dict:
				cart_quantity['COR002']=cart_quantity['COR002']+1
			else:
				cart_dict['COR002']=150
				cart_quantity["COR002"]=1
		elif "COR003" in request.form:
			if 'COR003' in cart_dict:
				cart_quantity['COR003']=cart_quantity['COR003']+1
			else:
				cart_dict['COR003']=180
				cart_quantity["COR003"]=1
		elif "COR004" in request.form:
			if 'COR004' in cart_dict:
				cart_quantity['COR004']=cart_quantity['COR004']+1
			else:
				cart_dict['COR004']=150
				cart_quantity["COR004"]=1
		elif "KFC001" in request.form:
			if 'KFC001' in cart_dict:
				cart_quantity['KFC001']=cart_quantity['KFC001']+1
			else:
				cart_dict['KFC001']=120
				cart_quantity["KFC001"]=1
		elif "KFC002" in request.form:
			if 'KFC002' in cart_dict:
				cart_quantity['KFC002']=cart_quantity['KFC002']+1
			else:
				cart_dict['KFC002']=200
				cart_quantity["KFC002"]=1
		elif "KFC003" in request.form:
			if 'KFC003' in cart_dict:
				cart_quantity['KFC003']=cart_quantity['KFC003']+1
			else:
				cart_dict['KFC003']=180
				cart_quantity["KFC003"]=1
		elif "KFC004" in request.form:
			if 'KFC004' in cart_dict:
				cart_quantity['KFC004']=cart_quantity['KFC004']+1
			else:
				cart_dict['KFC004']=200
				cart_quantity["KFC004"]=1
		elif "KFC005" in request.form:
			if 'KFC005' in cart_dict:
				cart_quantity['KFC005']=cart_quantity['KFC005']+1
			else:
				cart_dict['KFC005']=250
				cart_quantity["KFC005"]=1
		elif "KFC006" in request.form:
			if 'KFC006' in cart_dict:
				cart_quantity['KFC006']=cart_quantity['KFC006']+1
			else:
				cart_dict['KFC006']=75
				cart_quantity["KFC006"]=1
		elif "PIZ001" in request.form:
			if 'PIZ001' in cart_dict:
				cart_quantity['PIZ001']=cart_quantity['PIZ001']+1
			else:
				cart_dict['PIZ001']=195
				cart_quantity["PIZ001"]=1
		elif "PIZ002" in request.form:
			if 'PIZ002' in cart_dict:
				cart_quantity['PIZ002']=cart_quantity['PIZ002']+1
			else:
				cart_dict['PIZ002']=300
				cart_quantity["PIZ002"]=1
		elif "PIZ003" in request.form:
			if 'PIZ003' in cart_dict:
				cart_quantity['PIZ003']=cart_quantity['PIZ003']+1
			else:
				cart_dict['PIZ003']=120
				cart_quantity["PIZ003"]=1
		elif "PIZ004" in request.form:
			if 'PIZ004' in cart_dict:
				cart_quantity['PIZ004']=cart_quantity['PIZ004']+1
			else:
				cart_dict['PIZ004']=300
				cart_quantity["PIZ004"]=1
		elif "PIZ005" in request.form:
			if 'PIZ005' in cart_dict:
				cart_quantity['PIZ005']=cart_quantity['PIZ005']+1
			else:
				cart_dict['PIZ005']=350
				cart_quantity["PIZ005"]=1
		elif "PIZ006" in request.form:
			if 'PIZ006' in cart_dict:
				cart_quantity['PIZ006']=cart_quantity['PIZ006']+1
			else:
				cart_dict['PIZ006']=150
				cart_quantity["PIZ006"]=1
		elif "POB001" in request.form:
			if 'POB001' in cart_dict:
				cart_quantity['POB001']=cart_quantity['POB001']+1
			else:
				cart_dict['POB001']=199
				cart_quantity["POB001"]=1
		elif "POB002" in request.form:
			if 'POB002' in cart_dict:
				cart_quantity['POB002']=cart_quantity['POB002']+1
			else:
				cart_dict['POB002']=200
				cart_quantity["POB002"]=1
		elif "POB003" in request.form:
			if 'POB003' in cart_dict:
				cart_quantity['POB003']=cart_quantity['POB003']+1
			else:
				cart_dict['POB003']=150
				cart_quantity["POB003"]=1	
		elif "POB004" in request.form:
			if 'POB004' in cart_dict:
				cart_quantity['POB004']=cart_quantity['POB004']+1
			else:
				cart_dict['POB004']=250
				cart_quantity["POB004"]=1
		elif "POB005" in request.form:
			if 'POB005' in cart_dict:
				cart_quantity['POB005']=cart_quantity['POB005']+1
			else:
				cart_dict['POB005']=180
				cart_quantity["POB005"]=1	
		elif "POB006" in request.form:
			if 'POB006' in cart_dict:
				cart_quantity['POB006']=cart_quantity['POB006']+1
			else:
				cart_dict['POB006']=200
				cart_quantity["POB006"]=1		
		elif "TAC001" in request.form:
			if 'TAC001' in cart_dict:
				cart_quantity['TAC001']=cart_quantity['TAC001']+1
			else:
				cart_dict['TAC001']=169
				cart_quantity["TAC001"]=1
		elif "TAC002" in request.form:
			if 'TAC002' in cart_dict:
				cart_quantity['TAC002']=cart_quantity['TAC002']+1
			else:
				cart_dict['TAC002']=139
				cart_quantity["TAC002"]=1
		elif "TAC003" in request.form:
			if 'TAC003' in cart_dict:
				cart_quantity['TAC003']=cart_quantity['TAC003']+1
			else:
				cart_dict['TAC003']=149
				cart_quantity["TAC003"]=1
		elif "TAC004" in request.form:
			if 'TAC004' in cart_dict:
				cart_quantity['TAC004']=cart_quantity['TAC004']+1
			else:
				cart_dict['TAC004']=79
				cart_quantity["TAC004"]=1
		elif "TAC005" in request.form:
			if 'TAC005' in cart_dict:
				cart_quantity['TAC005']=cart_quantity['TAC005']+1
			else:
				cart_dict['TAC005']=169
				cart_quantity["TAC005"]=1
		elif "TAC006" in request.form:
			if 'TAC006' in cart_dict:
				cart_quantity['TAC006']=cart_quantity['TAC006']+1
			else:
				cart_dict['TAC006']=250
				cart_quantity["TAC006"]=1	
		elif "PAR001" in request.form:
			if 'PAR001' in cart_dict:
				cart_quantity['PAR001']=cart_quantity['PAR001']+1
			else:
				cart_dict['PAR001']=180
				cart_quantity["PAR001"]=1	
		elif "PAR002" in request.form:
			if 'PAR002' in cart_dict:
				cart_quantity['PAR002']=cart_quantity['PAR002']+1
			else:
				cart_dict['PAR002']=59
				cart_quantity["PAR002"]=1	
		elif "PAR003" in request.form:
			if 'PAR003' in cart_dict:
				cart_quantity['PAR003']=cart_quantity['PAR003']+1
			else:
				cart_dict['PAR003']=210
				cart_quantity["PAR003"]=1	
		elif "PAR004" in request.form:
			if 'PAR004' in cart_dict:
				cart_quantity['PAR004']=cart_quantity['PAR004']+1
			else:
				cart_dict['PAR004']=350
				cart_quantity["PAR004"]=1
		elif "PAR005" in request.form:
			if 'PAR005' in cart_dict:
				cart_quantity['PAR005']=cart_quantity['PAR005']+1
			else:
				cart_dict['PAR005']=250
				cart_quantity["PAR005"]=1	
		elif "PAR006" in request.form:
			if 'PAR006' in cart_dict:
				cart_quantity['PAR006']=cart_quantity['PAR006']+1
			else:
				cart_dict['PAR006']=280
				cart_quantity["PAR006"]=1


			
		return render_template('foodify_home.html', username=session['username'])


@app.route('/cart',methods=['GET','POST'])
def cart():
	msg=' '
	order_id='abc'
	restaurant_id_list=list()
	if request.method=='GET':
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		for key,value in cart_dict.items():
			cursor.execute('SELECT item_name FROM menu where item_id=%s',[key])
			item=cursor.fetchone()
			if item:
				item_dict[key]=item['item_name']
	if request.method=='POST':
		if 'order' in request.form:
			if bool(cart_dict)==True:
				msg = 'order confirmed!'
				username=session['username']
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM employee ORDER BY RAND() LIMIT 1;')
				employee=cursor.fetchone()
				employee_id=employee['Employee_id']
				while True:
					ord_id=unique_id()
					order_id='ORD'+str(ord_id)
					cursor.execute('SELECT order_id from order_distribution where order_id= %s ',[order_id])
					duplicate_id=cursor.fetchone()
					if duplicate_id:
						pass
					else:
						break
		

				cursor.execute('INSERT INTO order_distribution(order_id,username,employee_id) VALUES (%s,%s,%s)', (order_id,username, employee_id))

				mysql.connection.commit()
				total=0

				for key,value in cart_quantity.items():
				
					cursor.execute('SELECT restaurant_id from MENU where item_id=%s',[key])
					restaurant=cursor.fetchone()
					restaurant_id=restaurant['restaurant_id']
					quantity=request.form[key]
					price=cart_dict[key]*int(quantity)
					total=total+price
					cursor.execute('INSERT INTO orders(order_id,restaurant_id,item_id,quantity,price) VALUES (%s,%s,%s,%s,%s)', (order_id,restaurant_id,key,quantity,price))

					mysql.connection.commit()

				payment_id='PAY'+str(ord_id)
				mode_of_payment=request.form['modePayment']


				cursor.execute('INSERT INTO PAYMENT(payment_id,order_id,mode_of_payment,order_amount) VALUES (%s,%s,%s,%s)', (payment_id,order_id,mode_of_payment,total))

				mysql.connection.commit()
				restaurant_id_list=dict()
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				msg='Every review matters to us...'
				for key,value in cart_dict.items():
					res_id,res_name=get_restaurant(key)
					if res_id not in restaurant_id_list:
						restaurant_id_list[res_id]=res_name
				

					

					
				

				
				return render_template('reviews.html', restaurant_id_list=restaurant_id_list,order_id=order_id,msg=msg)

				

		else:
			msg="Cart Empty!!"

		if 'clear_cart' in request.form:
			cart_dict.clear()
			cart_quantity.clear()

		if 'remove' in request.form:
			remove_keys=request.form.getlist("remove_from_cart")
			for remove_key in remove_keys:
				del cart_dict[remove_key]
				del cart_quantity[remove_key]
		



	return render_template('cart.html',cart_dict=cart_dict,cart_quantity=cart_quantity,item_dict=item_dict,msg=msg,restaurant_id_list=restaurant_id_list,order_id=order_id)


		
@app.route('/mcd_menu')
def mcd():
	if 'loggedin' in session:
		return render_template('mcd_menu.html',username=session['username'],cart_dict=cart_dict)

@app.route('/polar_bear_menu')
def polarbear():
	if 'loggedin' in session:
		return render_template('polarbear_menu.html',username=session['username'],cart_dict=cart_dict)
@app.route('/cornerhouse_menu')
def corner_house():
	if 'loggedin' in session:
		return render_template('cornerhouse_menu.html',username=session['username'],cart_dict=cart_dict)
@app.route('/kfc_menu')
def kfc():
	if 'loggedin' in session:
		return render_template('kfc_menu.html',username=session['username'],cart_dict=cart_dict)
@app.route('/paradise_menu')
def paradise():
	if 'loggedin' in session:
		return render_template('paradise_menu.html',username=session['username'],cart_dict=cart_dict)
@app.route('/pizzahut_menu')
def pizzahut():
	if 'loggedin' in session:
		return render_template('pizzahut_menu.html',username=session['username'],cart_dict=cart_dict)
@app.route('/tacobell_menu')
def tacobell():
	if 'loggedin' in session:
		return render_template('tacobell_menu.html',username=session['username'],cart_dict=cart_dict)

@app.route('/review',methods=['GET','POST'])
def review():
	msg=''
	username=session['username']
	restaurant_id_list=list()
	if 'review_submit' in request.form:
		order_id=request.form['review_submit']
		restaurant_id_list=dict()
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		for key,value in cart_dict.items():
			res_id,res_name=get_restaurant(key)
			if res_id not in restaurant_id_list:
				restaurant_id_list[res_id]=res_name
		try:		
			if request.form['FRD001']:
				comment=request.form['FRD001']
				rating=request.form['review_rating_1']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD001',rating,comment))
		except:
			pass
		try:
			if request.form['FRD002']:
				comment=request.form['FRD002']
				rating=request.form['review_rating_2']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD002',rating,comment))
		except:
			pass
		try:
			if request.form['FRD003']:
				comment=request.form['FRD003']
				rating=request.form['review_rating_3']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD003',rating,comment))
		except:
			pass
		try:
			if request.form['FRD004']:
				comment=request.form['FRD004']
				rating=request.form['review_rating_4']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD004',rating,comment))
		except:
			pass
		try:
			if request.form['FRD005']:
				comment=request.form['FRD005']
				rating=request.form['review_rating_5']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD005',rating,comment))
		except:
			pass
		try:
			if request.form['FRD006']:
				comment=request.form['FRD006']
				rating=request.form['review_rating_6']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD006',rating,comment))
		except:
			pass
		try:
			if request.form['FRD007']:
				comment=request.form['FRD007']
				rating=request.form['review_rating_7']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD007',rating,comment))
		except:
			pass
		try:
			if request.form['FRD008']:
				comment=request.form['FRD008']
				rating=request.form['review_rating_8']
				cursor.execute('INSERT INTO REVIEWS(username,order_id,restaurant_id,review_rating,comments) VALUES(%s,%s,%s,%s,%s)',(username,order_id,'FRD008',rating,comment))
		except:
			pass

		mysql.connection.commit()
		msg='Thank you...'
		return render_template('foodify_home.html', username=session['username'])

	return render_template('reviews.html', restaurant_id_list=restaurant_id_list,order_id=order_id,msg=msg)


if __name__=='__main__':
	app.run(debug=True)