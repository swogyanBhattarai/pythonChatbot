from flask import Flask, render_template, request, jsonify
from project import *
from chatbot import output

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['message']
    bot_reply = f"{output(user_input)}"
    return jsonify({'user_input': user_input, 'bot_reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
