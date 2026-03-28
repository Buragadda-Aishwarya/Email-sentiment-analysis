from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import numpy as np
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

global uname

analyzer = SentimentIntensityAnalyzer()

def getSentiment(comment):
    sentiment = -1
    vs = analyzer.polarity_scores(comment)
    compound = vs['compound']
    if compound >= 0.5:
        sentiment =  'Extremely Happy'
    elif compound < 0.5 and compound >= 0.1:
        sentiment = 'Happy'
    elif compound < 0.1 and compound >= 0.05:
        sentiment = 'Positive'
    elif compound < 0.05 and compound > -0.05:
        sentiment = 'Neutral'
    else:
        sentiment = 'Negative'
    return sentiment, compound

def ViewEmail(request):
    if request.method == 'GET':
        global uname
        output='<table border=1 align=center width=100%><tr><th><font size="" color="black">Sender Name</th>'
        output += '<th><font size="" color="black">Receiver</th><th><font size="" color="black">Date</th>'
        output += '<th><font size="" color="black">Email Text</th><th><font size="" color="black">Sentiment</th>'
        output +='</tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'sentimentapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from mails where receiver = '"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+row[1]+'</td>'
                output+='<td><font size="" color="black">'+row[2]+'</td><td><font size="" color="black">'+row[3]+'</td>'
                output+='<td><font size="" color="black">'+row[4]+'</td></tr>'
        output+= "</table></br>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def ComposeAction(request):
    global uname
    if request.method == 'POST':
        #global uname
        receiver = request.POST.get('t1', True)
        email = request.POST.get('t2', True)
        sentiment, hatred = getSentiment(email)#finding hatred percentage
        email = email.replace("'","")
        today = str(datetime.now())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'sentimentapp',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO mails(sender,receiver,mail_date,mail_text,sentiment) VALUES('"+uname+"','"+receiver+"','"+today+"','"+email+"','"+sentiment+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':"Email successfully sent to "+receiver+"<br/>Predicted Sentiment = "+sentiment}
        return render(request, 'Compose.html', context)

def Compose(request):
    global uname
    if request.method == 'GET':
        global uname
        output = '<tr><td><font size="" color="black">Receiver</b></td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'sentimentapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup where username != '"+str(uname)+"'")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+row[0]+'">'+row[0]+'</option>'
        output += '</select></td></tr>'
        context= {'data1':output}
        return render(request, 'Compose.html', context)

def SingleEmail(request):
    if request.method == 'GET':
       return render(request, 'SingleEmail.html', {})

def MultiEmail(request):
    if request.method == 'GET':
       return render(request, 'MultiEmail.html', {})    

def SingleEmailAction(request):
    if request.method == 'POST':
        email = request.FILES['t1'].read()
        email = email.decode()
        sentiment, hatred = getSentiment(email)#finding hatred percentage
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Email Text</th><th><font size="" color="black">Predicted Sentiment</th>'
        output +='</tr>'        
        output+='</tr><td><font size="" color="black">'+email+'</td><td><font size="" color="black">'+str(sentiment)+'</td></tr>'
        output+= "</table></br>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def MultiEmailAction(request):
    if request.method == 'POST':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="" color="black">Email Text</th><th><font size="" color="black">Predicted Sentiment</th>'
        output +='</tr>'

        fname = request.FILES['t1']
        print(fname.name)

        for root, dirs, directory in os.walk('Emails'):
            for j in range(len(directory)):
                with open(root+"/"+directory[j], "rb") as file:
                    data = file.read()
                file.close()
                data = data.decode()
                sentiment, hatred = getSentiment(data)#finding hatred percentage
                output+='</tr><td><font size="" color="black">'+data+'</td><td><font size="" color="black">'+str(sentiment)+'</td></tr>'
                print(j)
        output+= "</table></br>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)          

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'sentimentapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username from signup where username = '"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == email:
                    status = 'Given Username already exists'
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'sentimentapp',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,email_id,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Signup Process Completed'
        context= {'data':status}
        return render(request, 'Signup.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'sentimentapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    uname = username
                    option = 1
                    break
        if option == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

