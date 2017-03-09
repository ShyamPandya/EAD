from flask import Flask,request,render_template
from flask import json
from flask import redirect
from requests.packages import urllib3

app = Flask(__name__)
app.secret_key = 'super secret key'





@app.route('/login/', methods=['GET','POST'])   #This is the login page function which will send the post to the server once username password is added
def loginpage():
    flag = 0
    error = ' '
    try:
        if request.method == "POST":
            print 'Testing'
            temp = request.form['inputName']
            temp2 = request.form['inputPassword']
            print temp
            print temp2
            encoded_body=json.dumps({"username":temp,"password":temp2,"requestCode":"LOGIN"}).encode('utf-8')
            http=urllib3.PoolManager()
            r=http.urlopen('POST', 'http:localhost:5001/todo/tasks/',headers={'Content-Type':'application/json'},body=encoded_body)
            json.loads(r.data.decode('utf-8'))['json']
            print temp
            print temp2
            print r.status
            return redirect("create_tasks")

        else:
            return render_template("login.html", error=error)

    except Exception as e:
        return render_template("login.html", error=error)


@app.route("/", methods=['GET','POST'])      #Starting page to choose from Login and SignUp
def homepage():
	if request.method=='POST':
		if request.form['Login'] == 'login':
			return render_template("login.html")
		elif request.form['SignUP'] == 'signup':
			pass
	elif request.method=='GET':
		return render_template("profile.html")


if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
