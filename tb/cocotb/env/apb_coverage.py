import json
from pathlib import Path

class ApbCoverage:
    def __init__(self, depth=32):
        self.depth = depth
        self.count = {
            "read": 0,
            "write": 0,
            "reset": 0,
            "legal_addr": 0,
            "illegal_addr": 0,
            "slverr_0": 0,
            "slverr_1": 0,
            "seq_write_read_same": 0,
            "back_to_back": 0,
            "boundary_0": 0,
            "boundary_31": 0,
        }
        self._last = None

    def on_txn(self, txn):
        if txn.kind == "RESET":
            self.count["reset"] += 1
            self._last = txn
            return

        if txn.kind == "READ":
            self.count["read"] += 1
        elif txn.kind == "WRITE":
            self.count["write"] += 1

        if 0 <= txn.addr < self.depth:
            self.count["legal_addr"] += 1
            if txn.addr == 0:
                self.count["boundary_0"] += 1
            if txn.addr == 31:
                self.count["boundary_31"] += 1
        else:
            self.count["illegal_addr"] += 1

        if txn.slverr == 0:
            self.count["slverr_0"] += 1
        else:
            self.count["slverr_1"] += 1

        if self._last is not None:
            if self._last.kind in ("READ", "WRITE") and txn.kind in ("READ", "WRITE"):
                self.count["back_to_back"] += 1
            if self._last.kind == "WRITE" and txn.kind == "READ" and self._last.addr == txn.addr:
                self.count["seq_write_read_same"] += 1

        self._last = txn

    def report(self):
        return dict(self.count)

    def export_json(self, path: str):
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.count, indent=2))
        return str(p)

