import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write_expect_error,
    apb_read_expect_error,
)


@cocotb.test()
async def test_illegal_addr(dut):
    """
    Directed Test

    Verification Objective:
        Verify that the DUT asserts PSLVERR for
        illegal APB read and write accesses.
    """

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info(
        "========== DIRECTED TEST: ILLEGAL ADDRESS =========="
    )

    await reset_dut(dut)

    illegal_addr = 45

    cocotb.log.info(
        f"WRITE ADDR={illegal_addr} (illegal)"
    )

    err = await apb_write_expect_error(
        dut,
        illegal_addr,
        0x12345678
    )

    assert err == 1, (
        "Expected PSLVERR during illegal write."
    )

    cocotb.log.info(
        f"READ ADDR={illegal_addr} (illegal)"
    )

    _, err = await apb_read_expect_error(
        dut,
        illegal_addr
    )

    assert err == 1, (
        "Expected PSLVERR during illegal read."
    )

    cocotb.log.info(
        "PASS: Illegal address verification completed successfully."
    )