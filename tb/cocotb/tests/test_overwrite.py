import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_overwrite(dut):

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== DIRECTED TEST: OVERWRITE ==========")

    # Reset DUT
    await reset_dut(dut)

    addr = 10

    first_data = 0x11111111
    second_data = 0xAAAAAAAA

    # First write
    cocotb.log.info(
        f"WRITE1 ADDR={addr} DATA=0x{first_data:08X}"
    )
    await apb_write(dut, addr, first_data)

    # Second write (overwrite)
    cocotb.log.info(
        f"WRITE2 ADDR={addr} DATA=0x{second_data:08X}"
    )
    await apb_write(dut, addr, second_data)

    # Read back
    rdata = await apb_read(dut, addr)

    # Verify latest value
    assert rdata == second_data, (
        f"Overwrite failed at address {addr}. "
        f"Expected 0x{second_data:08X}, "
        f"Got 0x{rdata:08X}"
    )

    cocotb.log.info("PASS: Overwrite verification completed successfully.")