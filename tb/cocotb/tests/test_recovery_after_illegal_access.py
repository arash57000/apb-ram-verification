import cocotb

from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
    apb_write_expect_error,
    apb_read_expect_error,
)


@cocotb.test()
async def test_recovery_after_illegal_access(dut):
    """
    Negative Test

    Verify that the DUT recovers correctly after illegal APB accesses.

    Expected:
        - Illegal accesses assert PSLVERR
        - DUT does not remain stuck after an error
        - Legal accesses immediately following an error succeed
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    # -------------------------------------------------
    # Recovery after illegal WRITE
    # -------------------------------------------------

    cocotb.log.info(
        "\n=== Recovery After Illegal Write ==="
    )

    await apb_write_expect_error(
        dut,
        32,
        0xDEADBEEF,
    )

    legal_write_addr = 5
    legal_write_data = 0x12345678

    await apb_write(
        dut,
        legal_write_addr,
        legal_write_data,
    )

    read_data = await apb_read(
        dut,
        legal_write_addr,
    )

    assert read_data == legal_write_data, (
        f"Recovery after illegal write failed! "
        f"Address={legal_write_addr} "
        f"Expected=0x{legal_write_data:08X} "
        f"Got=0x{read_data:08X}"
    )

    cocotb.log.info(
        "PASS: DUT recovered after illegal write."
    )

    # -------------------------------------------------
    # Recovery after illegal READ
    # -------------------------------------------------

    cocotb.log.info(
        "\n=== Recovery After Illegal Read ==="
    )

    await apb_read_expect_error(
        dut,
        100,
    )

    legal_read_addr = 20
    legal_read_data = 0xCAFEBABE

    await apb_write(
        dut,
        legal_read_addr,
        legal_read_data,
    )

    read_data = await apb_read(
        dut,
        legal_read_addr,
    )

    assert read_data == legal_read_data, (
        f"Recovery after illegal read failed! "
        f"Address={legal_read_addr} "
        f"Expected=0x{legal_read_data:08X} "
        f"Got=0x{read_data:08X}"
    )

    cocotb.log.info(
        "PASS: DUT recovered after illegal read."
    )

    cocotb.log.info(
        "PASS: DUT successfully recovered after all illegal accesses."
    )