import cocotb

from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
    apb_read_expect_error,
)


@cocotb.test()
async def test_illegal_read_address(dut):
    """
    Negative Test

    Verify that illegal read addresses are rejected.

    Expected:
        - PSLVERR is asserted
        - No RAM contents are modified
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    illegal_addresses = [
        32,
        33,
        100,
        255,
    ]

    for addr in illegal_addresses:

        cocotb.log.info(
            f"\n=== Illegal Read Test ===\n"
            f"ADDR : {addr}"
        )

        # Initialize RAM with a known pattern
        await initialize_memory_pattern(dut)

        # Perform illegal read and expect PSLVERR
        await apb_read_expect_error(
            dut,
            addr,
        )

        # Verify that every legal RAM location is unchanged
        for legal_addr in range(32):

            read_data = await apb_read(
                dut,
                legal_addr,
            )

            expected_data = legal_addr + 1

            assert read_data == expected_data, (
                f"Memory corruption detected! "
                f"Address={legal_addr} "
                f"Expected=0x{expected_data:08X} "
                f"Got=0x{read_data:08X}"
            )

    cocotb.log.info(
        "PASS: Illegal read addresses correctly rejected without memory corruption."
    )