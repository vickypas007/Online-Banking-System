from flask import Flask, render_template,url_for, redirect, request, session
from flask_mysqldb import MySQL,MySQLdb

app = Flask(__name__, static_url_path='/static0')

word=''
bankid=''

@app.route('/')


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/customer", methods=['GET','POST'])
def customer():
    fname = request.form['fname']
    lname = request.form['lname']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    email= request.form['email']
    pin = request.form['pin']
    # session['email'] = request.form['email']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    # query = "INSERT INTO customer (fname, lname, street, city,state,phone,email,pin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s )"
    # val=(fname, lname, street, city,state,phone,email,pin)
    # ob=db.cursor()
    # ob.execute(query,val)
    # db.commit()
    session['name'] = request.form['fname']
    ob1 = db.cursor()
    result = ob1.execute("select customerid, fname, lname, street, city,state,phone,email,pin FROM customer WHERE fname =%s", [fname])

    if result > 0:
        data = ob1.fetchone()
        return render_template('customer.html' ,m=data)
@app.route('/acc')
def acc():
    global word
    global bankid
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    name = session['name']
    ob = db.cursor()
    res = ob.execute("select customerid FROM customer WHERE fname = %s", [name])
    userid = ob.fetchone()
    ob1 =db.cursor()
    sol =ob.execute("SELECT `bankid` FROM `bank`")
    banki=ob.fetchone()
    bank=str(banki)
    nn = (bank.replace('(', ''))
    nn = (nn.replace(',', ''))
    nn = (nn.replace(')', ''))
    s = str(userid)
    nw =(s.replace('(', ''))
    nw = (nw.replace(',', ''))
    nw = (nw.replace(')', ''))
    word=nw
    bankid=nn
    session['customerid'] = word
    return render_template('account.html' )
    # return bankid


@app.route("/account", methods=['GET','POST'])
def account():

    atype= request.form['atype']
    mbal=request.form['mbal']
    bal=request.form['bal']
    nname=request.form['nname']
    nrel=request.form['nrel']
    bank_id =bankid
    cid=session['customerid']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    ob=db.cursor()
    # query = "INSERT INTO account (bankid, customerid, account_type, mbal, bal, nom_name, nom_rel) VALUES (%s,%s,%s,%s,%s,%s, %s )"
    # val =(bank_id,cid, atype, mbal, bal, nname, nrel)
    # ob.execute(query,val)
    # db.commit()
    ob1=db.cursor()
    result = ob1.execute( "select accountid, account_type, mbal, bal, nom_name, nom_rel FROM account WHERE customerid =%s", [cid])
    if result > 0:
        data = ob1.fetchone()
        session.clear()
        return render_template('account_create.html' ,m=data)

@app.route("/ad")
def ad():
    return render_template('ad1.html')

@app.route("/bal")
def bal():
    return render_template('balance.html')

@app.route("/depo")
def depo():
    return render_template('deposit.html')

@app.route("/deposit", methods=['POST', 'GET'])
def deposit():
    id = request.form['id']
    money=request.form['money']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    ob = db.cursor()
    res = ob.execute("select  bal  from account WHERE accountid=%s", [id])
    if res > 0:
        data = ob.fetchone()
        st = (str(data))
        nw = (st.replace('(', ''))
        nw = (nw.replace(',', ''))
        nw = (nw.replace(')', ''))
        nw = (nw.replace('\'', ''))
        bal = nw

        nbal =int(bal)+int(money)
        newbal=str(nbal)
        query= "insert into transaction ( accountid,amount,balance, description) values ( %s , %s ,%s,'Credited') "
        val =(id,money,newbal )
        res= ob.execute(query,val)
        ob.execute("update account set bal=%s where accountid=%s",(newbal,id))
        db.commit()

        return render_template('depositresult.html', m=id, n=money)


    else:
        return "Wrong Account ID"

@app.route("/get_balance" ,methods=['POST','GET'])
def get_balance():
    id = request.form['id']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    ob = db.cursor()
    res = ob.execute("select account_type,mbal, bal ,date from account WHERE accountid=%s", [id])
    if res > 0:
        data = ob.fetchone()
        return render_template('c_balance.html', m=data)

    else:
        return "Wrong Account ID"


@app.route("/detail", methods=['POST','GET'])
def detail():
    id=request.form['id']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    ob = db.cursor()
    res = ob.execute("select account_type,mbal, bal, nom_name,nom_rel from account WHERE accountid=%s", [id])
    if res> 0:
        data=ob.fetchone()
        return render_template('account_Detail.html', m=data)

    else:
        return "Wrong Account ID"

@app.route("/withdraw")
def withdraw():
    return render_template('withdraw.html')

@app.route("/withd", methods=['POST','GET'])
def withd():
    id = request.form['id']
    money = request.form['money']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    ob = db.cursor()
    res = ob.execute("select  bal,mbal  from account WHERE accountid=%s", [id])
    if res > 0:
        data = ob.fetchall()
        for row in data:
            ball =  row[0]
            mbal = row[1]

        nbal = int(ball) - int(money)
        if(nbal >= int(mbal)):
            newbal = str(nbal)
            query = "insert into transaction ( accountid,amount,balance, description) values ( %s , %s ,%s,'Debited') "
            val = (id, money, newbal)
            res = ob.execute(query, val)
            ob.execute("update account set bal=%s where accountid=%s", (newbal, id))
            db.commit()
            return render_template('depositresult.html', m=id, n=money)
            # return newbal
        else:
            return "Your Balance is Low"


    else:
        return "Wrong Account ID"

@app.route("/trans")
def trans():
    return render_template('transation.html')

@app.route("/transaction", methods=['POST','GET'])
def transaction():
    id = request.form['id']
    db = MySQLdb.connect(user='root', password='', host='localhost', database='banking')
    ob = db.cursor()
    res = ob.execute("SELECT time, amount, balance, description FROM transaction WHERE accountid=%s GROUP BY time DESC LIMIT 5", [id])
    if res >0:
        data=ob.fetchall()
    # SELECT time, amount, balance, description FROM transaction GROUP BY time DESC LIMIT 5
    return render_template('trans5.html', m=data)



if __name__ == '__main__':
    app.secret_key = "012#!ApaAjaBoleh)(*^%"
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)