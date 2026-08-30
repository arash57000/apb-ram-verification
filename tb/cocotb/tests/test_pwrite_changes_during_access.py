import cocotb

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_pwrite_changes_during_access(dut):
    """
    Protocol Behavior Characterization Test

    Intentionally violate the APB requirement that PWRITE remain
    stable from SETUP through ACCESS.

    This is not a protocol-compliance test. It documents the
    current RTL behavior: the DUT samples PWRITE when the
    transfer completes during ACCESS.
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)
    await initialize_memory_pattern(dut)

    addr = 10
    write_data = 0xDEADBEEF
    expected_data = addr + 1

    cocotb.log.info(
        "\n=== PWRITE Change During ACCESS Test ===\n"
        f"Changing PWRITE from WRITE to READ during ACCESS "
        f"at address {addr}"
    )

    # SETUP phase
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = addr
    dut.pwdata.value = write_data

    await RisingEdge(dut.pclk)

    # ACCESS phase with an intentional APB violation
    dut.penable.value = 1
    dut.pwrite.value = 0

    await RisingEdge(dut.pclk)

    while not dut.pready.value:
        await RisingEdge(dut.pclk)

    # Return bus to IDLE
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0

    await RisingEdge(dut.pclk)

    # Verify that the original memory value was preserved
    read_data = await apb_read(
        dut,
        addr,
    )

    cocotb.log.info(
        f"CHECK ADDR={addr:02d} "
        f"EXPECTED=0x{expected_data:08X} "
        f"READ=0x{read_data:08X}"
    )

    assert read_data == expected_data, (
        f"DUT did not exhibit the expected behavior after "
        f"a PWRITE change during ACCESS. "
        f"Address={addr} "
        f"Expected=0x{expected_data:08X} "
        f"Got=0x{read_data:08X}"
    )

    cocotb.log.info(
        "PASS: DUT behavior under a PWRITE change "
        "during ACCESS was characterized successfully."
    )
