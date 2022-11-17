
from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import ibm_db
import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL; SSLServerCertificateDigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bwp99066;PWD=qLyzyFcNwAu5sxde;", "", "")
print(conn)


app = Flask(__name__,template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/index")
def index():
  return render_template('index.html')

@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    phoneno = request.form['phoneno']
    password = request.form['password']

    if not username or not email or not phoneno or not password:
      return render_template('register.html',error='Please fill all fields')
    hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM user_detail WHERE email=? OR phoneno=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,phoneno)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    print(isUser)
    if not isUser:
      insert_sql = "INSERT INTO user_detail(username, email, phoneno, password) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phoneno)
      ibm_db.bind_param(prep_stmt, 4, hash)
      # param=username,email,phoneno,hash,
      ibm_db.execute(prep_stmt)
      return render_template('register.html',success="You can login")
    else:
      return render_template('register.html',error='Invalid Credentials')

  return render_template('register.html',name='Home')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      if not email or not password:
        return render_template('login.html',error='Please fill all fields')
      query = "SELECT * FROM user_detail WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('login.html',error='Invalid Credentials')
      
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('login.html',error='Invalid Credentials')

      session['email'] = isUser['EMAIL']
      return redirect("http://127.0.0.1:5000/dashboard")

    return render_template('login.html',name='Home')


@app.route("/addproduct",methods=['GET','POST'])
def addproduct():
  if request.method == 'POST':
    types=request.form['types']
    name = request.form['name']
    # image = request.form['image']
    quantity = request.form['quantity']
    # categorie = request.form['categorie']
    print(types)

    if types =='electronics':
      insert_sql = "INSERT INTO ELECTRONICS(name,quantity) VALUES (?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      # ibm_db.bind_param(prep_stmt, 2, image)
      # ibm_db.bind_param(prep_stmt, 3, categorie)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.execute(prep_stmt)
    if types =='mobiles':
      insert_sql = "INSERT INTO MOBILES(name, quantity) VALUES (?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      # ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.execute(prep_stmt)
    if types =='accessories':
      insert_sql = "INSERT INTO ACCESSORIES(name, quantity) VALUES (?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      # ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.execute(prep_stmt)
    if types =='appliances':
      insert_sql = "INSERT INTO APPLIANCES(name,quantity) VALUES (?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      # ibm_db.bind_param(prep_stmt, 2, image)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.execute(prep_stmt)
        
  return render_template('addproducts.html',success="success")

@app.route('/update',methods=['GET','POST'])
def update():

# UPDATE Customers
# SET ContactName = 'Alfred Schmidt', City= 'Frankfurt'
# WHERE CustomerID = 1;

  if(request.method=='POST'):
    types=request.form['types']
    name = request.form['name']
    # image = request.form['image']
    quantity = request.form['quantity']
    if types =='electronics':
      insert_sql = "UPDATE ELECTRONICS SET NAME=?,QUANTITY=? WHERE NAME=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.execute(prep_stmt)
    if types =='mobiles':
      insert_sql = "UPDATE MOBILES SET NAME=?,QUANTITY=? WHERE NAME=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.execute(prep_stmt)
    if types =='accessories':
      insert_sql = "UPDATE ACCESSORIES SET NAME=?,QUANTITY=? WHERE NAME=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.execute(prep_stmt)
    if types =='appliances':
      insert_sql = "UPDATE APPLIANCES SET NAME=?,QUANTITY=? WHERE NAME=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, quantity)
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.execute(prep_stmt)
  return render_template('update.html',success="success")

@app.route("/dashboard",methods=['GET','POST'])
def display():
  electronics_list=[]
  mobiles_list=[]
  accessories_list=[]
  appliance_list=[]
  if request.method=='GET':
  #selecting_shirt
    sql = "SELECT * FROM ELECTRONICS"
    stmt = ibm_db.exec_immediate(conn, sql)
    electronics = ibm_db.fetch_both(stmt)
    while electronics != False :
        electronics_list.append(electronics)
        electronics = ibm_db.fetch_both(stmt)
    
        for i in electronics_list:
          print(i.QUANTITY)
    
  #selecting_pant
    
    sql1="SELECT * FROM MOBILES"
    stmt1 = ibm_db.exec_immediate(conn, sql1)
    mobiles=ibm_db.fetch_both(stmt1)
    while mobiles != False :
        mobiles_list.append(mobiles)
        mobiles = ibm_db.fetch_both(stmt1)
    print(mobiles) 

  #selecting_watch
    sql2="SELECT * FROM ACCESSORIES"
    stmt2 = ibm_db.exec_immediate(conn, sql2)
    accessories=ibm_db.fetch_both(stmt2)
    while accessories != False :
        accessories_list.append(accessories)
        accessories = ibm_db.fetch_both(stmt2)
    print(accessories)

    #selecting_rings
    sql3="SELECT * FROM APPLIANCES"
    stmt3 = ibm_db.exec_immediate(conn, sql3)
    appliances=ibm_db.fetch_both(stmt3)
    while appliances != False :
        appliance_list.append(appliances)
        appliances = ibm_db.fetch_both(stmt3)
    print(appliances)  
    # if(electronics_list.QUANTITY==0 or mobiles_list.QUANTITY==0 or accessories_list.QUANTITY==0 or appliance_list.QUANTITY==0):
    #   sendMail()
    #returning to HTML
  return render_template('dashboard.html',electronics= electronics_list,mobiles=mobiles_list,accessories=accessories_list,appliances=appliance_list)
      


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def land():
  return redirect(url_for('login'))

# def sendMail():
  

#   message = Mail(
#       from_email='raghavan.v.2019.ece@ritchennai.edu.in',
#       to_emails='nitharshan.n.2019.ece@ritchennai.edu.in',
#       subject='Sendgrid Working',
#       html_content='<strong>Your stock needs to be updated</strong>')
#   try:
#       sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#       response = sg.send(message)
#       print(response.status_code)
#       print(response.body)
#       print(response.headers)
#   except Exception as e:
#       print(e.message)