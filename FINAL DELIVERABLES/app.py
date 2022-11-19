from flask import Flask, render_template, request,redirect,g,session
import ibm_db
import uuid
import os
from newsapi import NewsApiClient
import dbconn

app = Flask(__name__)

app.secret_key=os.urandom(24)


# Init news api
newsapi = NewsApiClient(api_key='bf36fc6aa93142989b0d224ed1176a22')

# helper function
def get_sources_and_domains():
	all_sources = newsapi.get_sources()['sources']
	sources = []
	domains = []
	for e in all_sources:
		id = e['id']
		domain = e['url'].replace("http://", "")
		domain = domain.replace("https://", "")
		domain = domain.replace("www.", "")
		slash = domain.find('/')
		if slash != -1:
			domain = domain[:slash]
		sources.append(id)
		domains.append(domain)
	sources = ", ".join(sources)
	domains = ", ".join(domains)
	return sources, domains


@app.route('/')
def index():
    if "UID" in session:
       return redirect("/home")
    else:
        return render_template("index.html")
@app.route('/signup')
def register():
    return render_template("signup.html")

@app.route('/signin')
def login():
    return render_template("signin.html")



#registration page code


@app.route("/registration", methods=['POST'])
def signup():
       if request.method == 'POST':
         name = request.form.get('name')
         email = request.form.get('email')
         pwd = request.form.get('pwd')
         emailcheck="SELECT * FROM authentication WHERE EMAIL='{0}' "
         smt = ibm_db.prepare(dbconn.con, emailcheck.format(email))
         ibm_db.execute(smt)
         mailres=ibm_db.fetch_assoc(smt)
         if mailres:
              return render_template("signup.html",msg="Email Is Already Taken")
         else:
           sql = "INSERT INTO authentication (id,username,email,password) VALUES ('{0}','{1}','{2}','{3}')"
           res = ibm_db.exec_immediate(dbconn.con, sql.format(uuid.uuid4(),name, email, pwd,))
           if sql:
              return redirect("/signin")
           else:
              return redirect("/")
       else:
        print("Could'nt store anything...")



#login page code      


@app.route("/login", methods=['POST'])
def signin():
       if request.method == 'POST':
            email = request.form.get('email')
            pwd = request.form.get('pwd')
            sql = "SELECT * FROM authentication WHERE EMAIL='{0}' AND PASSWORD='{1}'"
            smt = ibm_db.prepare(dbconn.con, sql.format(email,pwd))
            ibm_db.execute(smt)
            res=ibm_db.fetch_assoc(smt)
            
            if res: 
                 session["UID"]=res['ID']
                 return redirect("/home")
            else:
                  return render_template("signin.html",msg="Invalid Email Or Password")
       else:
         print("Could'nt store anything...")

@app.route('/home', methods=['GET','POST'])
def home():
      if "UID" in session:
         sql = "SELECT * FROM authentication WHERE ID='{0}' "
         smt = ibm_db.prepare(dbconn.con, sql.format(session["UID"]))
         ibm_db.execute(smt)
         res=ibm_db.fetch_assoc(smt)
         
         if res: 
            if request.method == "POST":
               sources, domains = get_sources_and_domains()
               keyword = request.form["keyword"]
               related_news = newsapi.get_everything(q=keyword,
									sources=sources,
									domains=domains,
									language='en',
									sort_by='relevancy')
               no_of_articles = related_news['totalResults']
               if no_of_articles > 100:
                  no_of_articles = 100
               all_articles = newsapi.get_everything(q=keyword,
									sources=sources,
									domains=domains,
									language='en',
									sort_by='relevancy',
									page_size = no_of_articles)['articles']
               return render_template("home.html", all_articles = all_articles,
							keyword=keyword)
            else:
               top_headlines = newsapi.get_top_headlines(country="in", language="en")
               total_results = top_headlines['totalResults']
               if total_results > 100:
                  total_results = 100
               all_headlines = newsapi.get_top_headlines(country="in",
													language="en",
													page_size=total_results)['articles']
               return render_template("home.html", all_headlines = all_headlines)
            return render_template("home.html")
         else:
            return redirect("/signin")
      else:
        return redirect("/signin")
@app.route("/index1", methods=['GET', 'POST'])
def index1():
	return render_template("index1.html")

@app.route("/Business", methods=['GET', 'POST'])
def Business():
	return render_template("Business.html")

@app.route("/Cricket", methods=['GET', 'POST'])
def Cricket():
	return render_template("Cricket.html")

@app.route("/Entertainment", methods=['GET', 'POST'])
def Entertainment():
	return render_template("Entertainment.html")

@app.route("/Health", methods=['GET', 'POST'])
def Health():
	return render_template("Health.html")

@app.route("/India", methods=['GET', 'POST'])
def India():
	return render_template("India.html")

@app.route("/searchlist", methods=['GET', 'POST'])
def searchlist():
	return render_template("searchlist.html")


@app.route("/Sports", methods=['GET', 'POST'])
def Sports():
	return render_template("Sports.html")


@app.route("/TechScience", methods=['GET', 'POST'])
def TechScience():
	return render_template("TechScience.html")


@app.route("/World", methods=['GET', 'POST'])
def World():
	return render_template("World.html")        





@app.route('/logout')
def logout():
        session.pop("UID",None)
        return redirect("/signin")

if __name__ == '__main__':
    app.run(debug=True)
