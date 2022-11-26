#!/usr/bin/python3
"""
Module for starting a Flask web application
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
from uuid import uuid4

# Flask Configration
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


# Flask Page Rendering Functions:
@app.teardown_appcontext
def teardown_db(exception):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/0-hbnb/')
def hbnb_filters(the_id=None):
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
    return render_template('100-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           users=users,
                           cache_id=uuid4())


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)
