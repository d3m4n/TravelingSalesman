from flask import render_template, jsonify, request
from . import main
from anneal import simulated_annealing, get_params

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/anneal', methods=['POST', 'GET', 'PUT'])
def anneal():
    data = request.json
    if not data:
        abort(400)
    params = get_params(data.pop('params', {}))
    return jsonify(simulated_annealing(data, **params))
    

@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
