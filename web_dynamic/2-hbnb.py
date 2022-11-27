#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

# Flask Configration
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


@app.teardown_appcontext
def close_db(error):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/2-hbnb', strict_slashes=False)
def hbnb():
    """
    Handels request from states, cites and amenitites
    with templates
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    return render_template('2-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           users=users,
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)
