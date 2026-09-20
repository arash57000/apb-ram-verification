import cocotb

from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
    apb_write_expect_error,
)


@cocotb.test()
async def test_illegal_write_address(dut):
    """
    Negative Test

    Verify that illegal write addresses are rejected.

    Expected:
        - PSLVERR is asserted
        - No RAM contents are modified
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    illegal_addresses = [
        (32, 0xDEADBEEF),
        (33, 0xCAFEBABE),
        (100, 0x12345678),
        (255, 0xFFFFFFFF),
    ]

    illegal_addresses += [
        (0xFFFFFFFF, 0xA5A5A5A5)
    ] * 10

    for addr, data in illegal_addresses:

        cocotb.log.info(
            f"\n=== Illegal Write Test ===\n"
            f"ADDR : 0x{addr:08X}\n"
            f"DATA : 0x{data:08X}"
        )

        # Initialize RAM with a known pattern
        await initialize_memory_pattern(dut)

        # Perform illegal write and expect PSLVERR
        await apb_write_expect_error(
            dut,
            addr,
            data
        )

        # Verify that every legal RAM location is unchanged
        for legal_addr in range(32):

            read_data = await apb_read(
                dut,
                legal_addr
            )

            expected_data = legal_addr + 1

            assert read_data == expected_data, (
                f"Memory corruption detected! "
                f"Address={legal_addr} "
                f"Expected=0x{expected_data:08X} "
                f"Got=0x{read_data:08X}"
            )

    cocotb.log.info(
        "PASS: Illegal write addresses correctly rejected without memory corruption."
    )
