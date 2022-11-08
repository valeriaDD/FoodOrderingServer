import itertools

class OrderProcessor:
    id_iter = itertools.count()

    def process_order(self, order):
        order['order_id'] = next(OrderProcessor.id_iter) + 1
        order['max_wait'] = 20
        order['priority'] = 1
        return order
