from pathlib import Path
import re, sqlite3
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
BASE_DIR=Path(__file__).resolve().parent; DB=BASE_DIR/'lab.db'
app=Flask(__name__,template_folder=str(BASE_DIR/'templates')); app.secret_key='lab-chain-only'
SQLI_FLAG='CPF 123.456.789-00'; XSS_FLAG='FLAG{STORED_XSS_EXECUTED}'
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 c=db(); c.executescript('''
 DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS profiles; DROP TABLE IF EXISTS comments;
 CREATE TABLE users(id INTEGER PRIMARY KEY,username TEXT,password TEXT,role TEXT,cpf TEXT);
 CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT,author TEXT,body TEXT);
 CREATE TABLE profiles(id INTEGER PRIMARY KEY,user_id INTEGER,full_name TEXT,email TEXT,phone TEXT,birth_date TEXT,cpf TEXT,address TEXT,account_type TEXT,agency TEXT,account_number TEXT,pix_key TEXT,balance_cents INTEGER,investments_cents INTEGER,credit_limit_cents INTEGER,last_transaction TEXT);
 INSERT INTO users VALUES(1,'admin','SuperSecretDemo!','admin','123.456.789-00');
 INSERT INTO users VALUES(9,'alberto','disabled','user','987.654.321-00');
 INSERT INTO profiles VALUES(1,1,'Administrador do Portal (FICTÍCIO)','admin@laboratorio.invalid','(11) 90000-0001','12/03/1990','123.456.789-00','Rua Laboratório Seguro, 1 - São Paulo/SP','Conta Administrativa','0001','000001-0','admin@pix.invalid',125000,380000,200000,'Pagamento educacional - R$ 189,90');
 INSERT INTO profiles VALUES(9,9,'Alberto Monteiro (FICTÍCIO)','alberto@exemplo.invalid','(11) 90000-9009','09/09/1979','987.654.321-00','Alameda Cenário Fictício, 900 - São Paulo/SP','Private Black - Demonstração','0099','900009-9','alberto@pix.invalid',875000000,1432050000,95000000,'Transferência simulada - R$ 1.275.000,00');
 '''); c.commit(); c.close()
def brl(cents):
 v=f'{cents/100:,.2f}'.replace(',','X').replace('.',',').replace('X','.'); return f'R$ {v}'
def make_idor_flag(p):
 first=re.sub(r'\D','',p['cpf'])[:3]; balance=p['balance_cents']//100; return f'FLAG{{{first}_{balance}}}'
@app.context_processor
def ctx(): return {'current_user':session.get('user')}
@app.route('/')
def index(): return render_template('index.html',unlocked=session.get('chain_stage')==1)
@app.route('/login',methods=['GET','POST'])
def login():
 error=None
 if request.method=='POST':
  u=request.form.get('username',''); p=request.form.get('password','')
  query=f"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'" # SQLi intencional
  try:
   c=db(); row=c.execute(query).fetchone(); c.close()
   if row:
    session['user']={'id':row['id'],'username':row['username'],'role':row['role']}
    if row['role']=='admin': session['chain_stage']=1
    return redirect(url_for('dashboard'))
   error='Usuário ou senha inválidos.'
  except sqlite3.Error as e: error=f'Erro SQL: {e}'
 return render_template('login.html',error=error)
@app.route('/dashboard')
def dashboard():
 u=session.get('user')
 if not u:return redirect(url_for('login'))
 unlocked=u['role']=='admin' and session.get('chain_stage')==1
 return render_template('dashboard.html',unlocked=unlocked,sqli_flag=SQLI_FLAG if unlocked else None)
@app.route('/profile')
def profile_home():
 u=session.get('user')
 if not u:return redirect(url_for('login'))
 if u['role']!='admin' or session.get('chain_stage')!=1:return render_template('locked.html'),403
 return redirect(url_for('profile',profile_id=1))
@app.route('/profile/<int:profile_id>')
def profile(profile_id):
 u=session.get('user')
 if not u:return redirect(url_for('login'))
 if u['role']!='admin' or session.get('chain_stage')!=1:return render_template('locked.html'),403
 c=db(); row=c.execute('SELECT * FROM profiles WHERE id=?',(profile_id,)).fetchone(); c.close()
 if not row:abort(404)
 exposed=profile_id!=1
 return render_template('profile.html',p=row,exposed=exposed,balance=brl(row['balance_cents']),investments=brl(row['investments_cents']),credit=brl(row['credit_limit_cents']),idor_flag=make_idor_flag(row) if exposed else None)
@app.route('/comments',methods=['GET','POST'])
def comments():
 if request.method=='POST':
  c=db();c.execute('INSERT INTO comments(author,body) VALUES(?,?)',(request.form.get('author','Anônimo'),request.form.get('body','')));c.commit();c.close();return redirect(url_for('comments'))
 c=db();rows=c.execute('SELECT * FROM comments ORDER BY id DESC').fetchall();c.close();return render_template('comments.html',comments=rows)
@app.route('/api/xss-flag')
def xss_flag():
 return (jsonify(flag=XSS_FLAG),200) if request.headers.get('X-XSS-Lab')=='executed' else (jsonify(error='Cabeçalho ausente'),403)
@app.route('/logout')
def logout():session.clear();return redirect(url_for('index'))
if __name__=='__main__':
 if not DB.exists():init_db()
 app.run(host='0.0.0.0',port=5000,debug=False)
