#Production-grade apb_monitor.py (RESET edge only)

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class ApbTxn:
    kind: str                 # "READ" / "WRITE" / "RESET"
    addr: int = 0
    wdata: Optional[int] = None
    rdata: Optional[int] = None
    slverr: int = 0
    time_ns: float = 0.0


class ApbMonitor:
    """
    Samples completed APB transfers at:
        PSEL && PENABLE && PREADY

    Reset is modeled as a single RESET transaction on the falling edge of PRESETn.
    """

    def __init__(self, dut):
        self.dut = dut
        self.log = dut._log.getChild("MON")
        self.subscribers: List[Callable[[ApbTxn], None]] = []
        self._prev_presetn = 1

        self.log.info("APB Monitor initialized")

    def subscribe(self, fn: Callable[[ApbTxn], None]):
        self.subscribers.append(fn)

    def _publish(self, txn: ApbTxn):
        for fn in self.subscribers:
            fn(txn)

    async def run(self):
        self.log.info("APB Monitor run() started")

        while True:
            await RisingEdge(self.dut.pclk)
            await ReadOnly()

            now = cocotb.utils.get_sim_time(units="ns")
            presetn = int(self.dut.presetn.value)

            # RESET edge detect (1 -> 0)
            if self._prev_presetn == 1 and presetn == 0:
                txn = ApbTxn(kind="RESET", time_ns=now)
                self.log.info(f"[{now:.1f} ns] RESET observed (edge)")
                self._publish(txn)

            self._prev_presetn = presetn

            # Only sample transfers when not in reset
            if presetn == 0:
                continue

            # Completed transfer
            if (int(self.dut.psel.value)
                and int(self.dut.penable.value)
                and int(self.dut.pready.value)):

                pwrite = int(self.dut.pwrite.value)
                addr   = int(self.dut.paddr.value)
                slverr = int(self.dut.pslverr.value)

                if pwrite:
                    wdata = int(self.dut.pwdata.value)
                    txn = ApbTxn(kind="WRITE", addr=addr, wdata=wdata, slverr=slverr, time_ns=now)
                    self.log.info(f"[{now:.1f} ns] WRITE  addr={addr} data=0x{wdata:08X} slverr={slverr}")
                else:
                    try:
                        rdata = int(self.dut.prdata.value)
                        rdata_text = f"0x{rdata:08X}"
                    except ValueError:
                        rdata = None
                        rdata_text = "XXXXXXXX"

                    txn = ApbTxn(
                        kind="READ",
                        addr=addr,
                        rdata=rdata,
                        slverr=slverr,
                        time_ns=now,
                    )

                    self.log.info(
                        f"[{now:.1f} ns] READ   "
                        f"addr=0x{addr:08X} data={rdata_text} "
                        f"slverr={slverr}"
                    )

                self._publish(txn)

