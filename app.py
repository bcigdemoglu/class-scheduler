# app.py
from flask import Flask, request, jsonify, render_template
import CS_IA_revised as scheduler
app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/load_excel/', methods=['GET'])
def load_excel():
    excel_data = request.args.get("excel_data", "")
    slot_count = request.args.get("slot_count", 0)
    scheduler.load_classes(excel_data, slot_count)
    response = {}
    response["RESULT"] = True
    return jsonify(response)

@app.route('/get_classes/', methods=['GET'])
def get_classes():
    picked_slot = request.args.get("picked_slot", None)
    response = {}
    classes = scheduler.get_potential_classes_for_slot(picked_slot)
    response["CLASSES"] = classes
    return jsonify(response)

@app.route('/select_class/', methods=['GET'])
def select_class():
    picked_slot = request.args.get("picked_slot", None)
    class_name = request.args.get("class_name", None)
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

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/receiveexcel/', methods=['POST'])
def get_csv():
    print(request)
    class_data = request.args.get('excel_data')
    print(class_data)

    return "Data sent for processing"

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {param} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
