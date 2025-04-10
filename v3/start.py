from flask import Flask, request, jsonify
from models.Notifier import StatusNotifier
from sys import argv
from datetime import datetime
import logging
import os


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

os.environ['FLASK_ENV'] = 'production'



notifier = StatusNotifier(timeframes=argv[1:7]) # Insert any preset values in future if needed

@app.route('/', methods=['POST'])
def speak_notification():
    try:
        value = request.get_json()
        # Check if 'key' exists in the received JSON
        if not value or 'key' not in value:
            return jsonify({"error": "No valid key found"}), 400

        notifier.talk(value['key'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/v3/1', methods=['POST']) # webhook_1 for lower timeframe 
def wh1():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(db=argv[1], status=value['status'], received_when = datetime.now())
        notifier.execute_process(caller = 1)
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v3/2', methods=['POST']) # webhook_2 for medium timeframe 
def wh2():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(db=argv[2], status=value['status'], received_when = datetime.now())
        #notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v3/3', methods=['POST']) # webhook_3 for higher timeframe 
def wh3():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(db=argv[3], status=value['status'], received_when = datetime.now())
        #notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)