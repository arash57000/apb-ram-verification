import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_reset(dut):

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())
    dut._log.info("========== RESET TEST ==========")

    # Perform reset
    await reset_dut(dut)

    # Give the DUT one extra clock after reset
    await RisingEdge(dut.pclk)

    # Write after reset
    addr = 5
    data = 0x12345678

    await apb_write(dut, addr, data)

    # Read back
    rdata = await apb_read(dut, addr)

    dut._log.info(f"Read back = 0x{int(rdata):08X}")

    assert int(rdata) == data, \
        f"Reset test failed: expected 0x{data:08X}, got 0x{int(rdata):08X}"

    dut._log.info("PASS: Reset verification completed successfully.")
