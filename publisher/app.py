from flask import Flask, request, render_template
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://ucu-test.servicebus.windows.net/;SharedAccessKeyName=send-receive;" \
                 "SharedAccessKey=zQqz7qjj1F/m8mM6XtCrt9bqB9VkFSFZb8q9FPxSN/c=;EntityPath=msg-q"
QUEUE_NAME = "msg-q"
MESSAGE = "Azure Service Bus is a messaging service on cloud used to connect any applications," \
          " devices, and services running in the cloud to any other applications or services."
MAX_WAIT_TIME = 5


app = Flask(__name__, template_folder="templates")


def send_one(sender, msg):
    message = ServiceBusMessage(msg)
    sender.send_messages(message)


@app.route("/", methods=['post', 'get'])
def home():
    sb = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    with sb:
        sender = sb.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            if request.method == 'POST':
                msg = request.form.get('message')
                send_one(sender, msg)
    return render_template("index.html")


if __name__ == '__main__':
      app.run()

