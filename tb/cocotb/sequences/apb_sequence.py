import random

class ApbSequence:
    def __init__(self):
        self.last_written = {}

    def next_txn(self):

        # 10% reset
        if random.random() < 0.10:
            return ("reset", None, None)

        # 20% chance → force read of previously written addr
        if self.last_written and random.random() < 0.2:
            addr = random.choice(list(self.last_written.keys()))
            return ("read", addr, None)

        # normal address selection
        if random.random() < 0.85:
            addr = random.randint(0, 31)
        else:
            addr = random.randint(32, 63)

        # boundary bias
        if random.random() < 0.1:
            addr = random.choice([0, 31])

        # operation
        if random.random() < 0.6:
            data = random.getrandbits(32)
            self.last_written[addr] = data   # ✅ TRACK WRITE
            return ("write", addr, data)

        else:
            return ("read", addr, None)
            
            
            '''
            
            Sequence → creates dependency
            Scoreboard → verifies correctness
            
            '''
