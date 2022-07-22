import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs(clubs_json):
    """ Return the content of clubs.json containing name, email and points of each user """
    with open(clubs_json) as c:  # 'clubs.json'
        return json.load(c)['clubs']


def load_comps(competitions_json):
    """ Return the content of competitions.json containing name, date and number of places of each competition """
    with open(competitions_json) as comps:
        return json.load(comps)['competitions']


def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    app.secret_key = 'something_special'

    comps = load_comps('tests/dataset.json') if app.config['TESTING'] is True else load_comps('competitions.json')
    clubs = load_clubs('tests/dataset.json') if app.config['TESTING'] is True else load_clubs('clubs.json')

    @app.route('/')
    def index():
        """ Login page """
        return render_template('index.html')

    @app.route('/show-summary', methods=['POST'])
    def show_summary():
        """ Show a summary of club and competitions data """
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except IndexError:
            flash('That email is not registered')
            return redirect(url_for('index'))
        return render_template('welcome.html', club=club, competitions=comps)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        """ Book place of a competition """
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in comps if c['name'] == competition][0]
        if found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=comps)

    @app.route('/purchase-places', methods=['POST'])
    def purchase_places():
        """ Purchase places of competition """
        competition = [c for c in comps if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        competition['number_of_places'] = int(competition['number_of_places']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=comps)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        """ Disconnect session of the current user """
        return redirect(url_for('index'))

    return app
