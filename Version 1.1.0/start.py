from flask import Flask, request, jsonify
from models.Notifier import StatusNotifier
from datetime import datetime
import logging
import os


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

os.environ['FLASK_ENV'] = 'production'

notifier = StatusNotifier() # Insert any preset settings in future if needed

@app.route('/', methods=['POST'])
def dosomething():
    try:
        value = request.get_json()
        # Check if 'key' exists in the received JSON
        if not value or 'key' not in value:
            return jsonify({"error": "No valid key found"}), 400

        notifier.talk(value['key'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/v1/l', methods=['POST'])
def wh1():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(webhook_name="low timeframe", status=value['status'], received_when = datetime.now())
        notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/m', methods=['POST'])
def wh2():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(webhook_name="midimum timeframe", status=value['status'], received_when = datetime.now())
        notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/h', methods=['POST'])
def wh3():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(webhook_name="higher timeframe", status=value['status'], received_when = datetime.now())
        notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
