from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, from heroku!.your code is working fine"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    session_id=request.form.get('From')
    reply=fetch_reply(msg,session_id)

    # Create reply
    response = MessagingResponse()
    # -response.message(reply)

    response.message(reply).media("https://cdn.pixabay.com/photo/2019/03/21/15/51/chatbot-4071274__340.jpg")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
