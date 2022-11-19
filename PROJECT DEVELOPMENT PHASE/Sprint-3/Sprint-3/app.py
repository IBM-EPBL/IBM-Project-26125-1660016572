# import libraries
from flask import Flask, render_template, request
from newsapi import NewsApiClient

# init flask app
app = Flask(__name__)

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

@app.route("/index", methods=['GET', 'POST'])
def home():
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

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

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

@app.route("/login", methods=['GET', 'POST'])
def login():
	return render_template("login.html")

@app.route("/registration", methods=['GET', 'POST'])
def registration():
	return render_template("registration.html")


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


if __name__ == "__main__":
	app.run(debug = True)
