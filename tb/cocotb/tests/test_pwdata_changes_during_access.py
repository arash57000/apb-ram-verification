import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_pwdata_changes_during_access(dut):
    """
    Protocol Behavior Characterization Test

    Intentionally violate the APB requirement that PWDATA remain
    stable from SETUP through ACCESS.

    This is not a protocol-compliance test. It documents the
    current RTL behavior: the DUT samples PWDATA when the
    transfer completes during ACCESS.
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)
    await initialize_memory_pattern(dut)

    addr = 10
    setup_data = 0x11111111
    access_data = 0xDEADBEEF

    cocotb.log.info(
        "\n=== PWDATA Change During ACCESS Test ==="
    )

    # SETUP phase
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = addr
    dut.pwdata.value = setup_data

    await RisingEdge(dut.pclk)

    # ACCESS phase with an intentional APB protocol violation
    cocotb.log.info(
        f"Changing PWDATA from "
        f"0x{setup_data:08X} to "
        f"0x{access_data:08X} "
        f"during ACCESS."
    )

    dut.penable.value = 1
    dut.pwdata.value = access_data

    await RisingEdge(dut.pclk)

    while not dut.pready.value:
        await RisingEdge(dut.pclk)

    # Return bus to IDLE
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0

    await RisingEdge(dut.pclk)

    # Verify which PWDATA value was captured
    read_data = await apb_read(
        dut,
        addr,
    )

    cocotb.log.info(
        f"CHECK ADDR={addr:02d} "
        f"EXPECTED=0x{access_data:08X} "
        f"READ=0x{read_data:08X}"
    )

    assert read_data == access_data, (
        f"DUT did not exhibit the expected behavior after "
        f"a PWDATA change during ACCESS. "
        f"Address={addr} "
        f"Expected=0x{access_data:08X} "
        f"Got=0x{read_data:08X}"
    )

    cocotb.log.info(
        "PASS: DUT behavior under a PWDATA change "
        "during ACCESS was characterized successfully."
    )
