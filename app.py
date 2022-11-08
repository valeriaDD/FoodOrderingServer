import json
import queue
import threading
import time

import requests
from flask import Flask, request

from src.OrderProcesser import OrderProcessor

app = Flask(__name__)

KITCHEN_URL = "http://kitchen:5000"
CLIENT_URL = "http://client:5002"

clients_orders_q = queue.Queue()
client_orders_writer_lock = threading.Lock()

orders_from_kitchen_q = queue.Queue()
kitchen_orders_writer_lock = threading.Lock()


class ClientOrderProcessor(threading.Thread):
    def __init__(self, order_q, lock):
        super(ClientOrderProcessor, self).__init__()
        self.order_q = order_q
        self.lock = lock

    def run(self):
        while True:
            while not self.order_q.empty():
                with self.lock:
                    requests.post(f'{KITCHEN_URL}/order', json=json.dumps(self.order_q.get()))
                    app.logger.info("Order sent to kitchen")
            else:
                time.sleep(2)


class KitchenOrderProcessor(threading.Thread):
    def __init__(self, order_q, lock):
        super(KitchenOrderProcessor, self).__init__()
        self.order_q = order_q
        self.lock = lock

    def run(self):
        while True:
            while not self.order_q.empty():
                with self.lock:
                    order = self.order_q.get()
                    requests.post(f'{CLIENT_URL}/serve/{order["client_id"]}', json=json.dumps(order))
                    app.logger.info("Order sent to client from Food Ordering")
            else:
                time.sleep(2)


@app.route("/")
def miaw():
    return "Hello from food-ordering server"


@app.route("/order", methods=['POST'])
def client_order_processing():
    with client_orders_writer_lock:
        data = request.json
        data = json.loads(data)
        app.logger.info("Food ordering got a order from Client!")

        order = OrderProcessor().process_order(data)
        clients_orders_q.put(order)
    return "Sent!"


@app.route("/distribution", methods=['POST'])
def process_data_from_kitchen():
    kitchen_orders_writer_lock.acquire()

    data = request.json
    data = json.loads(data)
    app.logger.info("Order back from kitchen to Food Ordering!")

    orders_from_kitchen_q.put(data)

    kitchen_orders_writer_lock.release()


    return "Sent!"


if __name__ == '__main__':
    orderProcessors = 2

    for _ in range(orderProcessors):
        client_thread = ClientOrderProcessor(clients_orders_q, client_orders_writer_lock)
        client_thread.daemon = True
        client_thread.start()

        for _ in range(orderProcessors):
            client_thread = KitchenOrderProcessor(orders_from_kitchen_q, kitchen_orders_writer_lock)
            client_thread.daemon = True
            client_thread.start()

        app.run(debug=True, port=5003, host="0.0.0.0")
