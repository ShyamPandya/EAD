import hashlib
from flask import Flask, request, render_template, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'super secret key'
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Pvms6972'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class switch(object):
    def __init__(self,value):
        self.value=value
        self.fall=False
    def __iter__(self):
        yield self.match
        raise StopIteration
    def match(self, *args):
        if self.fall or not args:
                return True
        elif self.value in args:
                self.fall=True
                return True
        else:
                return False

def validate(requestCode,clientRequest):
    for case in switch(requestCode):
        if case('LOGIN'):                        #These are the possible request codes that can be sent by the client and according to the code response will be given from the sql server
            username = ''
            password = ''
            temp = clientRequest['username'],
            temp2 = clientRequest['password'],
            for i in temp:
                if i == '<':
                    outchar = '&lt;'
                elif i == '>':
                    outchar = '&gt;'
                else:
                    outchar = i
                username += outchar
            for i in temp2:
                if i == '<':
                    outchar = '&lt;'
                elif i == '>':
                    outchar = '&gt;'
                else:
                    outchar = i
                password += outchar
            hashobj = hashlib.md5(username.encode('utf8'))
            hasheduname = hashobj.hexdigest()
            hashobj1 = hashlib.md5(password.encode('utf8'))
            hashedpword = hashobj1.hexdigest()
            print hasheduname
            print hashedpword
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                sql = "SELECT Username,Password FROM USER WHERE Username=%s"
                cursor.execute(sql, hasheduname)
                results = cursor.fetchall()
                if results:
                    for row in results:
                        pword = row[1]
                    if hashedpword == pword:
                        return "Succesful"
                        flag = 1
                    if flag == 0:
                        return "Login id password not found"

                else:
                    return "Login id password not found,LOL"
                conn.close()
            except Exception as e:
                flash(e)
                return error
        if case('REGISTER_NEW_COMPANY'):
            try:
                uname = clientRequest['username']
                cname=clientRequest['companyName']
                password = clientRequest['password']
                category = clientRequest['category']
                desc = clientRequest['description']
                date = clientRequest['starttDate']
                timeo = clientRequest['openTime']
                timec = clientRequest['closeTime']
                website = clientRequest['Website']
                phone = clientRequest['phone']
                email = clientRequest['email']
                details = clientRequest['detail']
                motto = clientRequest['motto']
                privacypolicy=clientRequest['privacyPolicy']
                hashobj = hashlib.md5(uname.encode('utf8'))
                hashedcname = hashobj.hexdigest()
                hashobj1 = hashlib.md5(password.encode('utf8'))
                final_password = hashobj1.hexdigest()
                conn = mysql.connect()
                cursor = conn.cursor()
                insert_stmt = (
                    "INSERT INTO company (CompanyName,Category,Description,DetailInfo,StartDate,Opening,Closing,Website,Email,Phone,Username,Motto,PrivacyPolicy) "
                    "VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                )
                data = (cname, category, desc, details, date, timeo, timec, website, email, phone, hashedcname,motto,privacypolicy)
                cursor.execute(insert_stmt, data)
                insert_stmt1 = (
                    "INSERT INTO USER(Username,Password) "
                    "VALUES (%s, %s)"
                )
                data1 = (hashedcname, final_password)
                cursor.execute(insert_stmt1, data1)
                conn.commit()
                conn.close()
                return "Successbitches"
            except Exception as e:
                return e
        if case('GET_MY_COMPANY'):
            id=1
            results={"COMPANIES":[]}
            username=clientRequest['username']
            hashobj = hashlib.md5(username.encode('utf8'))
            hasheduname = hashobj.hexdigest()
            conn=mysql.connect()
            cursor=conn.cursor()
            sql = "SELECT * FROM company WHERE username=%s"
            cursor.execute(sql, hasheduname)
            result=cursor.fetchall()
            for row in result:
                results["COMPANIES"].append({"companyName": row[1], "Category": row[2], "description": row[3],"DetailInfo": row[4], "startDate": str(row[5]), "openTime": row[6],"closeTime": row[7], "webpage": row[8], "email": row[9],"phone": row[10], "username": row[11], "motto": row[12],"privacyPolicy": row[13]})
                id += 1
            if result:
                print results
            else:
                print "Company doesn't exist"
                return "chudoz"
            return "Waah"
        if case('REGISTER_NEW_CLIENT'):
            name = clientRequest['name']
            username = clientRequest['username']
            password = clientRequest['password']
            email = clientRequest['email']
            phone = clientRequest['phone']
            hashobj = hashlib.md5(username.encode('utf8'))
            hashedcname = hashobj.hexdigest()
            hashobj1 = hashlib.md5(password.encode('utf8'))
            final_password = hashobj1.hexdigest()
            conn = mysql.connect()
            cursor = conn.cursor()
            insert_stmt = (
                "INSERT INTO USER (Username,Password,Email,Phone,Name) "
                "VALUES (%s, %s, %s, %s)"
            )
            data = (hashedcname,final_password,email,phone,name)
            cursor.execute(insert_stmt, data)
            return "Ho gaya bro"
        if case('GET_FRESH_POST'):
            id=1
            Cname = clientRequest['companyname']
            username = clientRequest['username']
            results = {"POSTS": []}
            conn=mysql.connect()
            cursor=conn.cursor()
            sql="SELECT * FROM post ORDER BY PostDate desc"
            cursor.execute(sql,Cname)
            result=cursor.fetchall()
            for row in result:
                results["POSTS"].append({"PID": row[1], "companyname": row[2], "Title": row[3],
                                                        "Category": row[4], "ShortDescription": row[5], "FullDescription": row[6],
                                                      "Image": row[7], "PostDate": row[8]})
                id += 1
            if result:
                print results
            else:
                print "Post doesn't exist"
                return "chudoz"
            return "Waah"
        if case('CREATE_POST'):
            cname=clientRequest['companyName']
            title=clientRequest['postTitle']
            shortdesc = clientRequest['postDescription']
            content = clientRequest['postContent']
            category = clientRequest['postCategory']
            date = clientRequest['postDate']
            image=clientRequest['image']
            conn = mysql.connect()
            cursor = conn.cursor()
            insert_stmt = (
                "INSERT INTO post (CompanyName,Title,Category,ShortDescription,FullDescription,Image,PostDate) "
                "VALUES (%s, %s, %s, %s,%s,%s,%s)"
            )
            data = (cname,title,category,shortdesc,content,image,date)
            cursor.execute(insert_stmt, data)
            return "Done scenes bro"
        if case('GET_COMPANY_POSTS'):
            id=1
            results = {"POSTS": []}
            username=clientRequest['username']
            companyName=clientRequest['companyName']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT * FROM post WHERE CompanyName=%s"
            cursor.execute(sql, companyName)
            result = cursor.fetchall()
            for row in result:
                results["POSTS"].append({"PID": row[1], "companyname": row[2], "Title": row[3],
                                         "Category": row[4], "ShortDescription": row[5], "FullDescription": row[6],
                                         "Image": row[7], "PostDate": row[8]})
                id += 1
            if result:
                print results
            else:
                print "Post doesn't exist"
                return "chudoz"
            return "Waah"
        if case('GET_FEATURED_POST'):
            id = 1
            results = {"POSTS": []}
            username = clientRequest['username']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT * FROM post p,postpriority q WHERE p.PID=q.PID  ORDER BY PriorityLevel desc"
            cursor.execute(sql, companyName)
            result = cursor.fetchall()
            for row in result:
                results["POSTS"].append({"PID": row[1], "companyname": row[2], "Title": row[3],
                                         "Category": row[4], "ShortDescription": row[5], "FullDescription": row[6],
                                         "Image": row[7], "PostDate": row[8]})
                id += 1
            if result:
                print results
            else:
                print "Post doesn't exist"
                return "chudoz"
            return "Waah"
        if case('GET_RECOMMENDED_POST'):
            id = 1
            results = {"POSTS": []}
            username = clientRequest['username']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT * FROM post WHERE PID in(SELECT PID,Datestamp FROM history WHERE Username=%s ORDER BY Datestamp desc)"
            cursor.execute(sql, companyName)
            result = cursor.fetchall()
            for row in result:
                results["POSTS"].append({"PID": row[1], "companyname": row[2], "Title": row[3],
                                         "Category": row[4], "ShortDescription": row[5], "FullDescription": row[6],
                                         "Image": row[7], "PostDate": row[8]})
                id += 1
            if result:
                print results
            else:
                print "Post doesn't exist"
                return "chudoz"
            return "Waah"


@app.route('/todo/tasks/', methods=['POST'])            #Function that will call validate() if a post is requested at this url
def create_tasks():
    error = ''
    try:
        clientRequest = request.get_json()
        requestCode = clientRequest['requestCode']
        print requestCode
        s = validate(requestCode, clientRequest)
        if s=="Succesful":
            res={'requestCode':'LOGIN','response':'Succesful'}
        else:
            res={'requestCode':'LOGIN','response':'Unsuccesful'}
        return jsonify(res)
    except Exception as e:
        print "Error"
        return e

@app.route('/todo/tasks/', methods=['GET'])
def send_tasks():
    print "yo"
    error="Bhaag BC"
    return render_template("main.html", error=error)

if __name__ == '__main__':
    app.run(host='localhost',port=5001,debug=True,use_reloader=False)
