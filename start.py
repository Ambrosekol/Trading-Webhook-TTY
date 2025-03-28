from flask import Flask, request, jsonify
from models.Notifier import StatusNotifier
from sys import argv


app = Flask(__name__)
notifier = StatusNotifier(timeframes=argv[1:4]) # Insert any preset settings in future if needed

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


@app.route('/v2/l', methods=['POST']) # webhook_1 for lower timeframe 
def wh1():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(webhook_name="webhook_one", status=value['status'])
        notifier.execute_process()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v2/m', methods=['POST']) # webhook_2 for medium timeframe 
def wh2():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(webhook_name="webhook_two", status=value['status'])
        notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v2/h', methods=['POST']) # webhook_3 for higher timeframe 
def wh3():
    try:
        value = request.get_json()
        # Check if 'status' exists in the received JSON
        if not value or 'status' not in value:
            return jsonify({"error": "No valid key found"}), 400
        notifier.save_webhook_data(webhook_name="webhook_three", status=value['status'])
        notifier.check_validity()
        #audiohandler.speak(value['status'])
        return jsonify({"status": "success", "code": 200}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
    