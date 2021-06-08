from flask import Flask, request, render_template
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://ucu-test.servicebus.windows.net/;SharedAccessKeyName=send-receive;" \
                 "SharedAccessKey=zQqz7qjj1F/m8mM6XtCrt9bqB9VkFSFZb8q9FPxSN/c=;EntityPath=msg-q"
QUEUE_NAME = "msg-q"
MAX_WAIT_TIME = 5
msg_list = []

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=['post', 'get'])
def result():
    sb = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    with sb:
        receiver = sb.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=MAX_WAIT_TIME)
        with receiver:
            for msg in receiver:
                receiver.complete_message(msg)
                msg_list.append(str(msg))
    return render_template("index.html", value=msg_list)


if __name__ == '__main__':
      app.run(port=5001)
