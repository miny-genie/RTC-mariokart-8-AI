import logging


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
        
    def emit(self, record):
        self.log_queue.put(record)
        

def register_queue_handler(queue_handler, log_level=logging.INFO):
    root_logger = logging.getLogger()
    
    for handler in root_logger.handlers:
        if isinstance(handler, QueueHandler):
            return
        
    formatter = logging.Formatter("%(asctime)s: %(message)s")
    queue_handler.setFormatter(formatter)
    
    root_logger.addHandler(queue_handler)
    root_logger.setLevel(log_level)