# -*- coding: utf-8 -*-
from flask import *
import os, sqlite3,re,random,hashlib
from flask.ext.mail import Mail, Message

mail = Mail()
app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.dobralab.com.br',
	MAIL_PORT=587,
	MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
	MAIL_USERNAME = 'contato@dobralab.com.br',
	MAIL_PASSWORD = 'furacao2000'
	)
app.config.from_pyfile('config.py')

mail.init_app(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("database/ham.db", timeout=300) #connect_to_database()
    return db

@app.route('/')
def index():
    i=request.args.get('i')
    db=get_db()
    cur=db.cursor()
    cur.execute("update prospect set click = click+1 where token=?",(str(i),))
    db.commit()
    cur.close()
    db.close()
    return redirect("http://dobralab.com.br")

@app.route('/load')
def load():
    print("loading files")
    db=get_db()
    cur=db.cursor()
    cur.execute("delete from prospect")
    db.commit()
    #CREATE TABLE prospect (id INTEGER PRIMARY KEY, email TEXT, uf TEXT, token TEXT, sent NUMERIC, name TEXT, url TEXT);
    lines=[]
    for filename in os.listdir('db'):
        fu=open("db/%s"%filename,"r+")
        lines+=fu.readlines()
        fu.close()
    fak=re.compile("\t|\n")
    for li in lines:
        print(li)
        l = fak.split(li)
        print(l)
        cur.execute("insert into prospect (name,phone,uf,email,url,click,view,sent) VALUES (?,?,?,?,?,0,0,0)", (l[0],l[1],l[2],l[3],l[4]))
        #['ZUM BRAZIL', '(71) 3341.7870', 'BA', 'zumbrazil@zumbrazil.com.br', 'http://www.zumbrazil.com.br']
    db.commit()
    cur.close()
    db.close()
    return json.dumps({})
@app.route('/send')
def send():
    db=get_db()
    cur=db.cursor()
    cur.execute("select name,email,id from prospect where sent=0 limit 1")
    data=cur.fetchone()
    if data is None:
        cur.close()
        db.close()
        return "Nada mais a enviar"
    token=hashlib.sha224(data[1].encode('utf-8')).hexdigest()
    t=render_template('mail.html', link="%s?i=%s"%(app.config.get('URL'),token,), image="%simage?i=%s"%(app.config.get('URL'),token,))
    cur.execute("update prospect set sent=1,token=? where id=?", (token,data[2],))
    db.commit()
    cur.close()
    db.close()
    msg = Message(app.config.get('SUBJECT'), sender='contato@dobralab.com.br', bcc=['barufi@gmail.com'], recipients=[data[1]])
    #msg = Message(app.config.get('SUBJECT'), sender='contato@dobralab.com.br', bcc=['barufi@gmail.com'], recipients=['leandro@dobralab.com.br'])
    msg.html = t
    mail.send(msg)
    return json.dumps({"status":"OK"})
@app.route('/image')
def image():
    i=request.args.get('i')
    db=get_db()
    cur=db.cursor()
    cur.execute("update prospect set view = view+1 where token=?",(str(i),))
    db.commit()
    cur.close()
    db.close()
    fs=[]
    r=re.compile('.*png$')
    for filename in os.listdir('img'):
        if r.match(filename):
            fs.append(filename)
    filename=fs[round(random.random()*len(fs)-1)]
    return send_file("img/%s"%filename, mimetype='image/png')
