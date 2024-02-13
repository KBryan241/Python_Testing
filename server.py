import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        for club in listOfClubs:
            club['total_reserved'] = 0  # Initialiser 'total_reserved' pour chaque club
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    return listOfCompetitions
    
app = Flask(__name__)
app.secret_key = 'something_special'
competitions = loadCompetitions()
clubs = loadClubs()
today = datetime.now()
@app.route('/')
def index():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    return render_template('index.html', clubs=clubs, competitions=comp)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    comp = [competition for competition in competitions if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") >= today]
    email = request.form['email']
    # password = request.form['password']
    if not email :
        flash("Enter a valid email please")
        return render_template('index.html', clubs=clubs, competitions=comp)
    
    club = next((club for club in clubs if club['email'] == email), None) #next permet d'obtenir le premier element d'une liste genere
    if not club:
        flash("No clubs exist for this email")
        return render_template('index.html', clubs = clubs, competitions = comp)
    return render_template('welcome.html', club = club, competitions = comp)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    flash("Something went wrong-please try again")
    return render_template('welcome.html', club = club, competitions = competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    placesRequired = int(request.form['places'])
    
    if not competition or not club:
        flash("Invalid competition or club")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    
    if int(club['points']) < placesRequired:
        flash("Your points is not enough")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    
    total_reserved = club['total_reserved'] + placesRequired
    if total_reserved > 12 and competition['name'] == club['last_competition']:
        flash("Your club has already purchased 12 places for this competition")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    
    if placesRequired > int(competition['numberOfPlaces']):
        flash("No place available for this competition")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points']=int(club['points'])- placesRequired
    club['total_reserved'] = total_reserved
    club['last_competition'] = competition['name']
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))