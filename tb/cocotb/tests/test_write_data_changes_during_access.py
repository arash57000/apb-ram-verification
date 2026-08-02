import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_write_data_changes_during_access(dut):
    """
    Negative Test

    Intentionally violate the APB requirement that PWDATA remain
    stable from SETUP through ACCESS.

    This test characterizes the DUT behavior when write data
    changes during the transaction.
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    await initialize_memory_pattern(dut)

    test_addr = 5
    setup_data = 0xAAAAAAAA
    access_data = 0xDEADBEEF

    cocotb.log.info(
        "\n=== Write Data Change During ACCESS Test ===\n"
        f"ADDR        : {test_addr}\n"
        f"SETUP DATA  : 0x{setup_data:08X}\n"
        f"ACCESS DATA : 0x{access_data:08X}"
    )

    # SETUP phase
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = test_addr
    dut.pwdata.value = setup_data

    await RisingEdge(dut.pclk)

    # ACCESS phase
    dut.penable.value = 1

    # Intentional APB protocol violation:
    # change PWDATA after SETUP
    dut.pwdata.value = access_data

    await RisingEdge(dut.pclk)

    while not dut.pready.value:
        await RisingEdge(dut.pclk)

    # Return bus to IDLE
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0

    await RisingEdge(dut.pclk)

    # Read back the target location
    read_data = await apb_read(
        dut,
        test_addr,
    )

    assert read_data == access_data, (
        f"Unexpected write data captured. "
        f"Address={test_addr} "
        f"Expected=0x{access_data:08X} "
        f"Got=0x{read_data:08X}"
    )

    cocotb.log.info(
        "PASS: DUT behavior under an ACCESS-phase "
        "PWDATA change was characterized successfully."
    )