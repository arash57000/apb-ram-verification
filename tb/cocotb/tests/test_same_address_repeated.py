import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


TEST_ADDRESS = 10

WRITE_PATTERNS = [
    0x00000000,
    0x11111111,
    0x22222222,
    0xAAAAAAAA,
    0x55555555,
    0x12345678,
    0xDEADBEEF,
    0xFFFFFFFF,
]


@cocotb.test()
async def test_same_address_repeated(dut):
    """
    Phase 6 - Corner-Case Test

    Repeatedly overwrite the same valid RAM address with different
    data values. Verify that each read returns the most recently
    written value.
    """

    # -------------------------------------------------
    # Start clock
    # -------------------------------------------------
    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    cocotb.log.info("=" * 60)
    cocotb.log.info("Starting Same-Address Repeated-Write Test")
    cocotb.log.info("=" * 60)

    # -------------------------------------------------
    # Reset DUT
    # -------------------------------------------------
    await reset_dut(dut)

    # -------------------------------------------------
    # Repeatedly overwrite the same address
    # -------------------------------------------------
    for iteration, expected_data in enumerate(
        WRITE_PATTERNS,
        start=1,
    ):
        cocotb.log.info(
            f"Iteration {iteration}: "
            f"writing 0x{expected_data:08X} "
            f"to address {TEST_ADDRESS}"
        )

        await apb_write(
            dut,
            TEST_ADDRESS,
            expected_data,
        )

        actual_data = await apb_read(
            dut,
            TEST_ADDRESS,
        )

        assert actual_data == expected_data, (
            f"Iteration {iteration}: repeated-write mismatch at "
            f"address {TEST_ADDRESS}. "
            f"Expected 0x{expected_data:08X}, "
            f"got 0x{actual_data:08X}"
        )

        cocotb.log.info(
            f"PASS  ITER={iteration:02d} "
            f"ADDR={TEST_ADDRESS:02d} "
            f"DATA=0x{actual_data:08X}"
        )

    # -------------------------------------------------
    # Final-value check
    # -------------------------------------------------
    expected_final_data = WRITE_PATTERNS[-1]

    actual_final_data = await apb_read(
        dut,
        TEST_ADDRESS,
    )

    assert actual_final_data == expected_final_data, (
        f"Final-value mismatch at address {TEST_ADDRESS}. "
        f"Expected 0x{expected_final_data:08X}, "
        f"got 0x{actual_final_data:08X}"
    )

    cocotb.log.info(
        f"FINAL PASS  ADDR={TEST_ADDRESS:02d} "
        f"DATA=0x{actual_final_data:08X}"
    )

    cocotb.log.info("=" * 60)
    cocotb.log.info("Same-Address Repeated-Write Test PASSED")
    cocotb.log.info("=" * 60)