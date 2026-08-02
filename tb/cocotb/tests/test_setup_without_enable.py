import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_setup_without_enable(dut):
    """
    Negative Test

    Verify that remaining in the APB SETUP phase
    does not perform a transfer.

    Expected:
        - No write occurs
        - Memory remains unchanged
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    await initialize_memory_pattern(dut)

    cocotb.log.info(
        "\n=== APB SETUP Without PENABLE Test ==="
    )

    #
    # Drive SETUP only
    #
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = 10
    dut.pwdata.value = 0xDEADBEEF

    #
    # Stay in SETUP for several cycles
    #
    for _ in range(5):
        await RisingEdge(dut.pclk)

    #
    # Abort transaction
    #
    dut.psel.value = 0
    dut.penable.value = 0

    await RisingEdge(dut.pclk)

    #
    # Verify RAM unchanged
    #
    for addr in range(32):

        read_data = await apb_read(
            dut,
            addr,
        )

        expected_data = addr + 1

        assert read_data == expected_data, (
            f"Unexpected write detected! "
            f"Address={addr} "
            f"Expected=0x{expected_data:08X} "
            f"Got=0x{read_data:08X}"
        )

    cocotb.log.info(
        "PASS: SETUP phase without PENABLE performed no transfer."
    )