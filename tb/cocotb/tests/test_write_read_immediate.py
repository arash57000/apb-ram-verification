import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_write_read_immediate(dut):
    """
    Directed Test

    Verification Objective:
        Verify that data written to a valid RAM address can be
        read back immediately in the next APB transaction.
    """

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info(
        "========== DIRECTED TEST: IMMEDIATE WRITE/READ =========="
    )

    await reset_dut(dut)

    addr = 20
    write_data = 0xDEADBEEF

    cocotb.log.info(
        f"WRITE ADDR={addr} DATA=0x{write_data:08X}"
    )

    await apb_write(dut, addr, write_data)

    read_data = await apb_read(dut, addr)

    assert read_data == write_data, (
        f"Immediate write/read failed at address {addr}. "
        f"Expected 0x{write_data:08X}, "
        f"Got 0x{read_data:08X}"
    )

    cocotb.log.info(
        "PASS: Immediate write/read verification completed successfully."
    )