import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
print(os.environ['FS_DB'])
print(os.environ['twilio_account_SID'])
print(os.environ['twilio_auth_token'])
app = Flask(__name__)
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI']=os.environ['HS_DB']
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

try:
    account_sid = os.environ['twilio_account_SID']
    auth_token = os.environ['twilio_auth_token']
except:
    print("Twilio keys not found. SMS function will not work. (optional anyway)")

client = Client(account_sid, auth_token)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    score = db.Column(db.Integer)
    value = db.Column(db.Integer)
    cleanliness = db.Column(db.Integer)
    location = db.Column(db.Integer)
    service = db.Column(db.Integer)

    def __init__(self, name, score, value, cleanliness, location, service):
        self.name = name
        self.score = score
        self.value = value
        self.cleanliness = cleanliness
        self.location = location
        self.service = service

    def __repr__(self):
        return '<Site %r>' % self.name

@app.route('/')
def index():
    refSite = Site.query.limit(10).all()
    entries = Site.query.count()
    latest = Site.query.order_by(Site.id.desc()).first()
    return render_template('app.html', refSite=refSite, entries=entries, latest=latest)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    try:
        body = request.values.get('Body', None)
        print(body)
        site = Site(body.replace(' ','')[:-1], body.strip()[-1], 5, 5, 5, 5)
        print(site)
        db.session.add(site)
        db.session.commit()
        resp = MessagingResponse()
        resp.message("Thanks. Record added! View it at: https://hotels.gspncr.com/site/"+body.replace(' ','')[:-1])
        return str(resp)
    except exc.IntegrityError as e:
        resp = MessagingResponse()
        resp.message("Sorry. That site already exists.")
        return str(resp)

def apiReturnValues(refSite):
    return jsonify(
        dict(name=refSite[0].name, score=refSite[0].score, value=refSite[0].value, cleanliness=refSite[0].cleanliness, location=refSite[0].location, service=refSite[0].service),
        dict(name=refSite[1].name, score=refSite[1].score, value=refSite[1].value, cleanliness=refSite[1].cleanliness, location=refSite[1].location, service=refSite[1].service),
        dict(name=refSite[2].name, score=refSite[2].score, value=refSite[2].value, cleanliness=refSite[2].cleanliness, location=refSite[2].location, service=refSite[2].service),
        dict(name=refSite[3].name, score=refSite[3].score, value=refSite[3].value, cleanliness=refSite[3].cleanliness, location=refSite[3].location, service=refSite[3].service),
        dict(name=refSite[4].name, score=refSite[4].score, value=refSite[4].value, cleanliness=refSite[4].cleanliness, location=refSite[4].location, service=refSite[4].service),
        dict(name=refSite[5].name, score=refSite[5].score, value=refSite[5].value, cleanliness=refSite[5].cleanliness, location=refSite[5].location, service=refSite[5].service),
        dict(name=refSite[6].name, score=refSite[6].score, value=refSite[6].value, cleanliness=refSite[6].cleanliness, location=refSite[6].location, service=refSite[6].service),
        dict(name=refSite[7].name, score=refSite[7].score, value=refSite[7].value, cleanliness=refSite[7].cleanliness, location=refSite[7].location, service=refSite[7].service),
        dict(name=refSite[8].name, score=refSite[8].score, value=refSite[8].value, cleanliness=refSite[8].cleanliness, location=refSite[8].location, service=refSite[8].service),
        dict(name=refSite[9].name, score=refSite[9].score, value=refSite[9].value, cleanliness=refSite[9].cleanliness, location=refSite[9].location, service=refSite[9].service)
    )

@app.route('/api/latest-10')
def latestTen():
    refSite = Site.query.limit(10).all()
    return apiReturnValues(refSite)

@app.route('/api/cleanest-10')
def cleanestTen():
    #results = db.session.query(User).filter(User.name == "Bob").order_by(User.age.desc()).limit(10)
    refSite = Site.query.order_by(Site.cleanliness.desc()).limit(10).all()
    return apiReturnValues(refSite)

@app.route('/api/top-overall-10')
def topOverallTen():
    #results = db.session.query(User).filter(User.name == "Bob").order_by(User.age.desc()).limit(10)
    refSite = Site.query.order_by(Site.score.desc()).limit(10).all()
    return apiReturnValues(refSite)

@app.route('/api/best-value-10')
def bestValueTen():
    #results = db.session.query(User).filter(User.name == "Bob").order_by(User.age.desc()).limit(10)
    refSite = Site.query.order_by(Site.value.desc()).limit(10).all()
    return apiReturnValues(refSite)

@app.route('/api/top-location-10')
def toplocationTen():
    #results = db.session.query(User).filter(User.name == "Bob").order_by(User.age.desc()).limit(10)
    refSite = Site.query.order_by(Site.location.desc()).limit(10).all()
    return apiReturnValues(refSite)

@app.route('/api/best-service-10')
def bestServiceTen():
    #results = db.session.query(User).filter(User.name == "Bob").order_by(User.age.desc()).limit(10)
    refSite = Site.query.order_by(Site.service.desc()).limit(10).all()
    return apiReturnValues(refSite)

@app.route('/new-site', methods=['POST'])
def newsite():
    try:
        site = Site(request.form['site'].replace(' ','-'), request.form['score'], request.form['valueV'], request.form['cleanliness'], request.form['location'], request.form['service'])
        db.session.add(site)
        db.session.commit()
        return redirect(url_for('index'))
    except exc.IntegrityError as e:
        e = "Site already exists!"
        return render_template('error.html', error=e)
    except:
        e = "Site already exists!"
        return render_template('error.html', error=e)

@app.route('/api/new', methods=['GET','POST'])
def apiNewsite():
    try:
        site = Site(request.json.get('name').replace(' ','-'), request.json.get('score'), request.json.get('value'), request.json.get('cleanliness'), request.json.get('location'), request.json.get('service'))
        db.session.add(site)
        db.session.commit()
        return jsonify("success")
    except exc.IntegrityError as e:
        return jsonify("site exists")

@app.route('/api/update/<sitename>', methods=['PUT'])
def apiUpdateSite(sitename):
    try:
        db.session.query(Site).filter_by(name=sitename).update({'score': request.json.get('score'), 'value': request.json.get('value'), 'cleanliness': request.json.get('cleanliness'), 'location': request.json.get('location'), 'service': request.json.get('service')})
        db.session.commit()
        return jsonify("site updated")
    except (exc.IntegrityError, werkzeug.routing.BuildError) as e:
        e = "unhandled"
        return jsonify("site does not exist or other error")

@app.route('/update/<sitename>', methods=['POST'])
def updateSite(sitename):
    try:
        db.session.query(Site).filter_by(name=sitename).update({'score': request.form['score'], 'value': request.form['valueV'], 'cleanliness': request.form['cleanliness'], 'location': request.form['location'], 'service': request.form['service']})
        db.session.commit()
        return redirect(request.url_root+'site/'+sitename)
    except exc.IntegrityError as e:
        e = "unhandled"
        return render_template('error.html', error=e)

@app.route('/remove/<sitename>', methods=['DELETE'])
def removeSite(sitename):
    try:
        site = Site.query.filter_by(name=sitename).delete()
        db.session.commit()
        return jsonify("removed")
    except exc.IntegrityError as e:
        e = "Site already exists!"
        return jsonify("error")

@app.route('/top', methods=['GET'])
def bestOverall():
    latest = Site.query.order_by(Site.score.desc())
    return render_template('app.html', overall=latest, refSite=latest)

@app.route('/most-clean', methods=['GET'])
def mostClean():
    latest = Site.query.order_by(Site.cleanliness.desc())
    return render_template('app.html', cleanest=latest, refSite=latest)

@app.route('/best-value', methods=['GET'])
def bestValue():
    latest = Site.query.order_by(Site.value.desc())
    return render_template('app.html', value=latest, refSite=latest)

@app.route('/best-location', methods=['GET'])
def bestlocation():
    latest = Site.query.order_by(Site.location.desc())
    return render_template('app.html', location=latest, refSite=latest)

@app.route('/best-service', methods=['GET'])
def bestService():
    latest = Site.query.order_by(Site.service.desc())
    return render_template('app.html', service=latest, refSite=latest)

@app.route('/site/<sitename>', methods=['GET'])
def site(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return render_template('site.html', oneSite=oneSite)

@app.route('/api/site/<sitename>', methods=['GET'])
def sitelookup(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return jsonify(name=oneSite.name, overall=oneSite.score, value=oneSite.value, cleanliness=oneSite.cleanliness, location=oneSite.location, space=oneSite.service)

@app.route('/api/score/<sitename>', methods=['GET'])
def sitescore(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return jsonify(overall=oneSite.score)

@app.route('/api/value/<sitename>', methods=['GET'])
def value(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return jsonify(value=oneSite.value)

@app.route('/api/cleanliness/<sitename>', methods=['GET'])
def cleanliness(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return jsonify(cleanliness=oneSite.cleanliness)

@app.route('/api/location/<sitename>', methods=['GET'])
def location(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return jsonify(location=oneSite.location)

@app.route('/api/space/<sitename>', methods=['GET'])
def space(sitename):
    oneSite = Site.query.filter_by(name=sitename).first()
    return jsonify(space=oneSite.service)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

app.run(host='0.0.0.0', port=8080)
