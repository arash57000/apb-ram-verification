from dataclasses import dataclass
from typing import Optional

@dataclass
class ApbTxn:
    kind: str               # "READ" | "WRITE" | "RESET"
    addr: int = 0
    wdata: int = 0
    rdata: int = 0
    slverr: int = 0
    time_ns: float = 0.0

    def is_legal(self, depth: int) -> bool:
        return 0 <= self.addr < depth

