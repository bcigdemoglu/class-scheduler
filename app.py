# app.py
import argparse
from flask import Flask, request, jsonify, render_template
import CS_IA_revised2 as scheduler
app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/load_excel/', methods=['GET'])
def load_excel():
    excel_data = request.args.get("excel_data", "", type=str)
    slot_count = request.args.get("slot_count", 0, type=int)
    scheduler.load_classes(excel_data, slot_count)
    response = {}
    response["RESULT"] = True
    return jsonify(response)

@app.route('/get_classes/', methods=['GET'])
def get_classes():
    picked_slot = request.args.get("picked_slot", None, type=int)
    response = {}
    classes = scheduler.get_potential_classes_for_slot(picked_slot)
    response["CLASSES"] = classes
    return jsonify(response)

@app.route('/select_class/', methods=['GET'])
def select_class():
    picked_slot = request.args.get("picked_slot", None, type=int)
    class_name = request.args.get("class_name", None, type=str)
    scheduler.select_class_for_slot(class_name, picked_slot)
    response = {}
    response["RESULT"] = True
    return jsonify(response)

@app.route('/reset_schedule/', methods=['GET'])
def reset_schedule():
    scheduler.reset_selections()
    response = {}
    response["RESULT"] = True
    return jsonify(response)

if __name__ == '__main__':
    debug = False

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Turns debugging on", action='store_true')
    args = parser.parse_args()
    if args.debug:
        print("Debugging on")
        debug = True
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=debug, threaded=True, port=5000)
