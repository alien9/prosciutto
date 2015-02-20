from flask import *
import os, sqlite3, re
from flask.ext.mail import Mail, Message

app = Flask(__name__)
app.debug = True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("ham.db", timeout=300) #connect_to_database()
    return db

@app.route('/')
def index():
    print("hihihihi")
    data={}
    return json.dumps({})

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
        print(filename)
        fu=open("db/%s"%filename,"r+")
        lines+=fu.readlines()
        fu.close()
    fak=re.compile("\t|\n")
    for li in lines:
        print(li)
        l = fak.split(li)
        print(l)
        cur.execute("insert into prospect (name,phone,uf,email,url,click,view) VALUES (?,?,?,?,?,0,0)", (l[0],l[1],l[2],l[3],l[4]))
        #['ZUM BRAZIL', '(71) 3341.7870', 'BA', 'zumbrazil@zumbrazil.com.br', 'http://www.zumbrazil.com.br']
    db.commit()
    cur.close()
    db.close()
    return json.dumps({})
@app.route('/send')
def send():
    m=Message()
@app.route('/image')
def image():
    i=request.form.get('i')
    db=get_db()
    cur=db.cursor()
    cur.execute("update prospect set view = view+1 where token=?",(i))
    db.commit()
    cur.close()
    db.close()
    return send_file("img/tumblr_my9qfzwqWj1srv10po1_500.jpg", mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
