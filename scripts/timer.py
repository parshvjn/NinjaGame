import time

class Timer:
    def __init__(self, timeAmount):
        self.start_time = time.time()
        self.amount = timeAmount

    def count(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time>=self.amount

    def redo(self):
        self.start_time = time.time()
    