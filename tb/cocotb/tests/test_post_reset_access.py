import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_post_reset_access(dut):
    """
    Phase 6 - Corner-Case Test

    Verify the DUT correctly accepts the very first
    APB transaction immediately after reset is released.
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    dut._log.info("============================================================")
    dut._log.info("Starting Post-Reset Access Test")
    dut._log.info("============================================================")

    # ---------------------------------------------------------
    # Apply reset
    # ---------------------------------------------------------
    await reset_dut(dut)

    # ---------------------------------------------------------
    # First transaction after reset
    # ---------------------------------------------------------
    addr = 12
    expected_data = 0xABCDEF01

    dut._log.info(
        "Performing first APB transaction immediately after reset"
    )

    await apb_write(dut, addr, expected_data)

    read_data = await apb_read(dut, addr)

    assert read_data == expected_data, (
        f"Expected 0x{expected_data:08X}, "
        f"got 0x{read_data:08X}"
    )

    dut._log.info(
        f"PASS  ADDR={addr} DATA=0x{read_data:08X}"
    )

    dut._log.info("============================================================")
    dut._log.info("Post-Reset Access Test PASSED")
    dut._log.info("============================================================")