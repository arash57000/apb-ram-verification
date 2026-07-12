import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_addr31(dut):

    # Start APB clock
    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== DIRECTED TEST: ADDRESS 31 ==========")

    # Reset DUT
    await reset_dut(dut)

    # Highest valid address for 32-location RAM
    addr = 31
    data = 0x5A

    cocotb.log.info(
        f"WRITE ADDR={addr} DATA=0x{data:02X}"
    )

    # Write
    await apb_write(dut, addr, data)

    # Read
    rdata = await apb_read(dut, addr)

    # Verify
    assert rdata == data, (
        f"Expected 0x{data:02X}, "
        f"Got 0x{rdata:02X}"
    )

    cocotb.log.info("Address 31 test PASSED.")