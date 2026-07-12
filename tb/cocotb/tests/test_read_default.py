import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_read,
)


@cocotb.test()
async def test_read_default(dut):

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== DIRECTED TEST: DEFAULT MEMORY ==========")

    # Reset DUT
    await reset_dut(dut)

    # Verify every memory location is cleared
    for addr in range(32):

        rdata = await apb_read(dut, addr)

        cocotb.log.info(
            f"ADDR={addr:02d} DATA=0x{rdata:08X}"
        )

        assert rdata == 0, (
            f"Address {addr} not reset. "
            f"Expected 0x00000000, "
            f"Got 0x{rdata:08X}"
        )

    cocotb.log.info(
        "PASS: All memory locations correctly reset to zero."
    )