import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_boundary_toggle(dut):
    """
    Phase 6 - Corner Case Test

    Rapidly alternate accesses between the lowest and highest
    valid RAM addresses to verify correct address decoding and
    memory integrity.
    """

    # -------------------------------------------------
    # Start Clock
    # -------------------------------------------------
    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    cocotb.log.info("=" * 60)
    cocotb.log.info("Starting Boundary Toggle Test")
    cocotb.log.info("=" * 60)

    # -------------------------------------------------
    # Reset DUT
    # -------------------------------------------------
    await reset_dut(dut)

    # -------------------------------------------------
    # Repeat Boundary Accesses
    # -------------------------------------------------
    for iteration in range(1, 21):

        cocotb.log.info(f"\nIteration {iteration}")

        addr0_data = iteration
        addr31_data = 0xFFFFFFFF - iteration

        # ---------------------------------------------
        # Address 0
        # ---------------------------------------------
        await apb_write(dut, 0, addr0_data)

        read_data = await apb_read(dut, 0)

        assert read_data == addr0_data, (
            f"Iteration {iteration}: "
            f"Address 0 mismatch. "
            f"Expected 0x{addr0_data:08X}, "
            f"Got 0x{read_data:08X}"
        )

        cocotb.log.info(
            f"PASS  ADDR=00 DATA=0x{addr0_data:08X}"
        )

        # ---------------------------------------------
        # Address 31
        # ---------------------------------------------
        await apb_write(dut, 31, addr31_data)

        read_data = await apb_read(dut, 31)

        assert read_data == addr31_data, (
            f"Iteration {iteration}: "
            f"Address 31 mismatch. "
            f"Expected 0x{addr31_data:08X}, "
            f"Got 0x{read_data:08X}"
        )

        cocotb.log.info(
            f"PASS  ADDR=31 DATA=0x{addr31_data:08X}"
        )

    cocotb.log.info("=" * 60)
    cocotb.log.info("Boundary Toggle Test PASSED")
    cocotb.log.info("=" * 60)