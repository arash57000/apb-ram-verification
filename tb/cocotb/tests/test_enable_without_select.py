import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_enable_without_select(dut):
    """
    Negative Test

    Verify that asserting PENABLE without PSEL
    does not perform an APB transfer.

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
        "\n=== APB PENABLE Without PSEL Test ==="
    )

    #
    # Illegal APB bus state
    #
    dut.psel.value = 0
    dut.penable.value = 1
    dut.pwrite.value = 1
    dut.paddr.value = 10
    dut.pwdata.value = 0xDEADBEEF

    #
    # Hold this state for several clocks
    #
    for _ in range(5):
        await RisingEdge(dut.pclk)

    #
    # Return bus to IDLE
    #
    dut.penable.value = 0

    await RisingEdge(dut.pclk)

    #
    # Verify RAM contents
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
        "PASS: PENABLE without PSEL performed no transfer."
    )