# Production-grade apb_driver.py
import cocotb
from cocotb.triggers import RisingEdge, ReadOnly


class ApbDriver:
    """
    APB Driver (UVM-style)
    - Drives APB stimulus only
    - Does NOT check PRDATA/PSLVERR (scoreboard/monitor do that)
    - Optionally returns sampled (slverr, rdata) for debug, sampled correctly in ReadOnly
    
    Why this is “daily DV” driver-quality

    Always returns to idle between transfers (prevents accidental protocol overlap)

    Samples in ReadOnly() on the completion cycle (same rule your monitor uses)

    No checking/asserts (scoreboard owns correctness)

    Timeout cleans up bus before throwing (so failures don’t cascade)
    
    In industry:

   A driver usually drives (no checking).

   A monitor samples (source of truth).

   But it is totally normal for a driver to do debug sampling (return rdata/slverr) as long as:

   it samples correctly (ReadOnly on completion)

   it does not assert/check

   That’s exactly what the upgraded driver does.
    
    
    """

    def __init__(self, dut, cfg=None):
        self.dut = dut
        self.cfg = cfg   # store config
        self.log = dut._log.getChild("DRV")

        # Default bus idle
        self.dut.psel.value = 0
        self.dut.penable.value = 0
        self.dut.pwrite.value = 0
        self.dut.paddr.value = 0
        self.dut.pwdata.value = 0

    def _t(self) -> float:
        return cocotb.utils.get_sim_time(units="ns")

    async def _drive_idle(self):
        """Return bus to idle state (APB idle)."""
        self.dut.psel.value = 0
        self.dut.penable.value = 0
        self.dut.pwrite.value = 0
        self.dut.paddr.value = 0
        self.dut.pwdata.value = 0

    async def reset(self, cycles: int = 5):
        # Drive bus idle before reset
        await self._drive_idle()

        self.dut.presetn.value = 0
        self.log.info(f"[{self._t():.1f} ns] RESET assert")

        for _ in range(cycles):
            await RisingEdge(self.dut.pclk)

        self.dut.presetn.value = 1
        await RisingEdge(self.dut.pclk)
        self.log.info(f"[{self._t():.1f} ns] RESET deassert")

        # Leave bus idle after reset
        await self._drive_idle()

    async def write(self, addr: int, data: int, timeout_cycles: int = 100, return_slverr: bool = False):
        """
        APB write:
          SETUP:  PSEL=1, PENABLE=0, PWRITE=1, PADDR, PWDATA
          ACCESS: PENABLE=1 until PREADY
          SAMPLE: In ReadOnly on the completion cycle (PREADY=1)
          COMPLETE: Drop PSEL/PENABLE next cycle

        Returns:
          - None by default
          - slverr (int) if return_slverr=True (sampled correctly)
        """

        # ---- SETUP ----
        self.dut.psel.value = 1
        self.dut.penable.value = 0
        self.dut.pwrite.value = 1
        self.dut.paddr.value = addr
        self.dut.pwdata.value = data

        await RisingEdge(self.dut.pclk)

        # ---- ACCESS ----
        self.dut.penable.value = 1
        self.log.info(f"[{self._t():.1f} ns] WRITE addr={addr} data=0x{data:08X}")

        # Wait for completion (PREADY high on a rising edge)
        for _ in range(timeout_cycles):
            await RisingEdge(self.dut.pclk)
            if int(self.dut.pready.value):
                break
        else:
            # Clean up bus before raising
            await self._drive_idle()
            raise TimeoutError(f"WRITE timeout waiting for PREADY (addr={addr})")

        # ---- SAMPLE (completion cycle) ----
        await ReadOnly()
        slverr = int(self.dut.pslverr.value)

        # ---- COMPLETE ----
        await RisingEdge(self.dut.pclk)
        await self._drive_idle()

        self.log.info(f"[{self._t():.1f} ns] WRITE-DONE addr={addr} slverr={slverr}")

        if return_slverr:
            return slverr
        return None

    async def read(self, addr: int, timeout_cycles: int = 100, return_slverr: bool = True):
        """
        APB read:
          SETUP -> ACCESS -> SAMPLE (ReadOnly on completion cycle) -> COMPLETE

        Returns:
          - (rdata, slverr) by default (sampled correctly)
          - rdata only if return_slverr=False
        """

        # ---- SETUP ----
        self.dut.psel.value = 1
        self.dut.penable.value = 0
        self.dut.pwrite.value = 0
        self.dut.paddr.value = addr

        await RisingEdge(self.dut.pclk)

        # ---- ACCESS ----
        self.dut.penable.value = 1
        self.log.info(f"[{self._t():.1f} ns] READ  addr={addr}")

        for _ in range(timeout_cycles):
            await RisingEdge(self.dut.pclk)
            if int(self.dut.pready.value):
                break
        else:
            await self._drive_idle()
            raise TimeoutError(f"READ timeout waiting for PREADY (addr={addr})")

        # ---- SAMPLE (completion cycle) ----
        await ReadOnly()
        rdata = int(self.dut.prdata.value)
        slverr = int(self.dut.pslverr.value)

        # ---- COMPLETE ----
        await RisingEdge(self.dut.pclk)
        await self._drive_idle()

        self.log.info(
            f"[{self._t():.1f} ns] READ-DONE addr={addr} data=0x{rdata:08X} slverr={slverr}"
        )

        if return_slverr:
            return rdata, slverr
        return rdata

