from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from collision_check import check_for_ship_in_sol
from mapping import *

app = Flask(__name__)
app.debug = False
map_url = '/'
no_map_url = '/nomap'

@app.route(no_map_url, methods = ['GET'])
def landing_page():
    return render_template('index.htm', p_ship = "jumper", p_id = 336, p_sol = 1)

@app.route(no_map_url, methods = ['POST'])
def check():
    ship_name = request.form['name']
    ship_id = request.form['id']
    sol = request.form['sol']
    return render_template('index.htm', result = check_for_ship_in_sol(ship_name, int(ship_id), int(sol))
    , p_ship = ship_name, p_id = ship_id, p_sol = sol)

#########

@app.route(map_url, methods = ['GET'])
def clown_page():
    return render_template('map_index.htm', p_ship = "jumper", p_id = 336, p_sol = 1)

@app.route(map_url, methods = ['POST'])
def clown_check():
    ship_name = request.form['name']
    ship_id = request.form['id']
    sol = request.form['sol']
    return render_template('map_index.htm', result = check_for_ship_in_sol(ship_name, int(ship_id), int(sol))
    , p_ship = ship_name, p_id = ship_id, p_sol = sol)



@app.route('/<ship>/<int:ship_nb>/<int:sol_id>')
def checker(ship, ship_nb, sol_id):
    return check_for_ship_in_sol(ship, ship_nb, sol_id)

@app.route('/ships')
def ship_json():
    return render_template('ships.json')

@app.route('/script_js')
def script_js():
    return render_template("script.js")

@app.route('/map_js')
def map_js():
    return render_template("map.js")

@app.route('/map_collections_js')
def map_collections_js():
    return render_template("map_collections.js")

@app.route('/map_form_js')
def map_form_js():
    return render_template("map_form.js")

@app.route('/map_script_js')
def map_script_js():
    return render_template("map_script.js")

@app.route('/carac')
def ship_carac():
    return render_template('carac.json')

@app.route('/ships_img/<name>')
def ships_img(name):
    return send_from_directory('static/ships_img', name)

### Maping

@app.route('/<ship>/<int:ship_nb>/<int:sol_id>/red')
def red_map(ship, ship_nb, sol_id):
    return mappy(sol_id - 1)

@app.route('/<ship>/<int:ship_nb>/<int:sol_id>/blue')
def blue_map(ship, ship_nb, sol_id):
    return get_all_miners_in_sol_as_xyt(sol_id - 1)

@app.route('/<ship>/<int:ship_nb>/<int:sol_id>/green')
def green_map(ship, ship_nb, sol_id):
    return owner_ship(ship, ship_nb, sol_id - 1)


if __name__ == '__main__':
    app.run()