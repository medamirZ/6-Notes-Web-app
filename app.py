from flask import Flask,render_template,request,Request,url_for,redirect,session as se
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine,Column,String,Integer
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,mean_squared_error
import numpy as np
import os
password = os.getenv('mysql_password')
#init the model
model = pickle.load(file=open('model.pkl','rb'))
app = Flask(__name__,template_folder='templates',static_folder='static')
url = f'mysql://root:{password}@localhost/notes'

engine = create_engine(url)
base = declarative_base()
app.secret_key = 'MY MAN'
class Accounts(base):
    __tablename__ = 'accounts'
    id = Column(Integer,primary_key=True,nullable=True,unique=True)
    name = Column(String(100))
    username = Column(String(100),unique=True)
    password = Column(String(100),nullable=True)
    
class Notebyid(base):
    __tablename__ = 'notebyid'
    id = Column(Integer,primary_key=True,nullable=True,unique=True)
    note1 = Column(String(200))
    note2 = Column(String(200))
    note3 = Column(String(200))
    note4 = Column(String(200))
    note5 = Column(String(200))
    note6 = Column(String(200))

class Noteheader(base):
    __tablename__ = 'noteheader'
    id = Column(Integer,primary_key=True,nullable=True,unique=True)
    hdr1 = Column(String(200))
    hdr2 = Column(String(200))
    hdr3 = Column(String(200))
    hdr4 = Column(String(200))
    hdr5 = Column(String(200))
    hdr6 = Column(String(200))

loggedin = False
DN = []
DH = []
def getInfos(id,session) :
        global DATAHEADER
        global DATANOTE
        
        DATANOTE = []
        DATAHEADER = []
        noteData = session.query(Notebyid).all()
        headerData = session.query(Noteheader).all()
        for user in noteData :
            if(id == user.id) :
                    DATANOTE.append(user.note1)               
                    DATANOTE.append(user.note2)
                    DATANOTE.append(user.note3)
                    DATANOTE.append(user.note4)
                    DATANOTE.append(user.note5)
                    DATANOTE.append(user.note6)
        for user in headerData :
            if(id == user.id) :
                DATAHEADER.append(user.hdr1)
                DATAHEADER.append(user.hdr2)
                DATAHEADER.append(user.hdr3)
                DATAHEADER.append(user.hdr4)
                DATAHEADER.append(user.hdr5)
                DATAHEADER.append(user.hdr6)
                
        global DH
        global DN
        
        DH = DATAHEADER
        DN = DATANOTE       
        return redirect(url_for('loginin'))
@app.route('/')
def home():
    notedata = DN
    noteheader = DH
    feeling = ['undefined yet','undefined yet','undefined yet','undefined yet','undefined yet','undefined yet']
    if(len(notedata)!=0) :
        notedata = ['none' if (x==None) else x for x in notedata]
        feeling = notedata
        print(f'feelings : {feeling}')
        model = pickle.load(file=open('model.pkl','rb'))
        vect = pickle.load(file=open('vectorizer.pkl','rb'))
        feeling = vect.transform(feeling)
        feelingg = model.predict(feeling)
        return render_template('home.html',loggedin = loggedin,notedata =notedata,noteheader= noteheader,selectedName=selectedName,feeling =feelingg)
    else :
        return render_template('home.html',loggedin = loggedin,notedata =notedata,noteheader= noteheader,selectedName=selectedName,feeling =feeling)
        
    
        
#missing now html
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/sign')
def sign():
    return render_template('sign.html')

# methods
@app.route('/signin',methods =['post','get'])
def signin():
    #sessions
    Session = sessionmaker(bind=engine)
    session = Session()
    name = request.form['fname']
    username = request.form['username']
    password = request.form['password']
    
    Data = session.query(Accounts).all()
    isUsernameExist = False
    for data in Data:
        if(data.username == username):
            isUsernameExist = True
    if(isUsernameExist == False):
        instance = Accounts(name=name,username=username,password=password)
        session.add(instance)
        session.commit()
        data =  session.query(Accounts).all()
        for user in data :
            if (user.name == instance.name):
                id = user.id
        session.add(Notebyid(id=id))
        session.add(Noteheader(id=id))
        session.commit()
        session.close()
        return render_template('sign.html',message1 = 'Account has been created successfuly')
    else :
        return render_template('sign.html',message2 = 'Failed to create your account It seems this email is taken!')

idUser = ''
selectedName = ''

        
@app.route('/loginin',methods=['post','get'])

def loginin():
    global loggedin
    global idUser
    
    Session = sessionmaker(bind=engine)
    ses = Session()
    username = request.form['username']
    password = request.form['password']
    Data = ses.query(Accounts).all()
    accountFound = False    
        
    se['user_id'] = idUser
    global selectedName
    for user in Data :
        selectedUsername = user.username
        selectedPassword = user.password
        selectedName = user.name
        if(username == selectedUsername and password == selectedPassword):
            accountFound = True
            idUser = user.id
            
            getInfos(idUser,ses)
            break
         
    if accountFound :
        loggedin = True
        # return render_template('login.html',message1 = 'You logged in successfuly',message2 =f'Welcome {selectedName}')
        return redirect(url_for('home'))
    
    else :
        return render_template('login.html',message2 =f'Account not found!')

            
@app.route('/addnote',methods = ['POST','GET'])
def addNote() :
    
    header = request.form['hdr']  
    note = request.form['inpnote']
    id = idUser
    Session = sessionmaker(bind=engine)
    session = Session()
    dataNote = session.query(Notebyid).all()
    dataHeader = session.query(Noteheader).all()
    for user in dataNote :
        if(user.id == id):
            if(user.note1 is None) :
                session.query(Notebyid).filter_by(id = user.id).update({Notebyid.note1:note})
            elif(user.note1 is not None and (user.note2 is None)) :
                session.query(Notebyid).filter_by(id = user.id).update({Notebyid.note2:note})              
            elif(user.note2 is not None and (user.note3 is None)) :
                session.query(Notebyid).filter_by(id = user.id).update({Notebyid.note3:note})
            elif(user.note3 is not None and (user.note4 is None)) :
                session.query(Notebyid).filter_by(id = user.id).update({Notebyid.note4:note})
            elif(user.note4 is not None and (user.note5 is None)) :
                session.query(Notebyid).filter_by(id = user.id).update({Notebyid.note5:note})
            elif(user.note5 is not None and (user.note6 is None)) :
                session.query(Notebyid).filter_by(id = user.id).update({Notebyid.note6:note})
            else :
                pass
            
    for user in dataHeader :
        if(user.id == id):
            if(user.hdr1 is None) :
                session.query(Noteheader).filter_by(id = user.id).update({Noteheader.hdr1:header})
            elif(user.hdr1 is not None and (user.hdr2 is None)) :
                session.query(Noteheader).filter_by(id = user.id).update({Noteheader.hdr2:header})
            elif(user.hdr2 is not None and (user.hdr3 is None)) :
                session.query(Noteheader).filter_by(id = user.id).update({Noteheader.hdr3:header})
            elif(user.hdr3 is not None and (user.hdr4 is None)) :
                session.query(Noteheader).filter_by(id = user.id).update({Noteheader.hdr4:header})
            elif(user.hdr4 is not None and (user.hdr5 is None)) :
                session.query(Noteheader).filter_by(id = user.id).update({Noteheader.hdr5:header})
            elif(user.hdr5 is not None and (user.hdr6 is None)) :
                session.query(Noteheader).filter_by(id = user.id).update({Noteheader.hdr6:header})
            else :
                pass
            
    session.commit()
    
  
    getInfos(idUser,session)
    return redirect(url_for('home'))
    
@app.route('/editnote',methods=['POST'])
def modify_note() :
    
    noteheader = request.form['hdr2']
    notecontent = request.form['inpnote2']
    Session = sessionmaker(bind=engine)
    session = Session()
    dataNote = session.query(Notebyid).all()
    dataHeader = session.query(Noteheader).all()
    getInfos(idUser,session)  
    session.query(Notebyid).filter_by(id = idUser ).update({Notebyid.note1 : notecontent})
    session.query(Noteheader).filter_by(id = idUser).update({Noteheader.hdr1 : noteheader})
    session.commit()
    getInfos(session=session,id=idUser)
    return redirect(url_for('home'))
    
    
if(__name__ == "__main__") :
    app.run(debug=True)
    