import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_address_changes_during_access(dut):
    """
    Negative Test

    Intentionally violate the APB requirement that PADDR remain
    stable from SETUP through ACCESS.

    This test characterizes the DUT behavior. The current DUT
    samples PADDR when the transfer completes in ACCESS.
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)
    await initialize_memory_pattern(dut)

    original_addr = 5
    changed_addr = 20
    write_data = 0xDEADBEEF

    cocotb.log.info(
        "\n=== Address Change During ACCESS Test ==="
    )

    # SETUP phase
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = original_addr
    dut.pwdata.value = write_data

    await RisingEdge(dut.pclk)

    # ACCESS phase with an intentional APB violation
    dut.penable.value = 1
    dut.paddr.value = changed_addr

    await RisingEdge(dut.pclk)

    while not dut.pready.value:
        await RisingEdge(dut.pclk)

    # Return bus to IDLE
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0

    await RisingEdge(dut.pclk)

    original_data = await apb_read(
        dut,
        original_addr,
    )

    changed_data = await apb_read(
        dut,
        changed_addr,
    )

    original_expected = original_addr + 1

    assert original_data == original_expected, (
        f"Original address changed unexpectedly. "
        f"Address={original_addr} "
        f"Expected=0x{original_expected:08X} "
        f"Got=0x{original_data:08X}"
    )

    assert changed_data == write_data, (
        f"ACCESS-phase address was not used. "
        f"Address={changed_addr} "
        f"Expected=0x{write_data:08X} "
        f"Got=0x{changed_data:08X}"
    )

    cocotb.log.info(
        "PASS: DUT behavior under an ACCESS-phase address "
        "change was characterized successfully."
    )