import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_reset_during_transaction(dut):
    """
    Phase 6 - Corner-Case Test

    Assert reset during an active APB write transaction.
    Verify the DUT recovers correctly and accepts
    new transactions after reset.
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    dut._log.info("============================================================")
    dut._log.info("Starting Reset-During-Transaction Test")
    dut._log.info("============================================================")

    # ---------------------------------------------------------
    # Initial reset
    # ---------------------------------------------------------
    await reset_dut(dut)

    addr = 5
    data = 0x12345678

    # ---------------------------------------------------------
    # Begin APB WRITE (SETUP phase)
    # ---------------------------------------------------------
    dut._log.info("Starting APB write transaction")

    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = addr
    dut.pwdata.value = data

    await RisingEdge(dut.pclk)

    # ---------------------------------------------------------
    # ACCESS phase
    # ---------------------------------------------------------
    dut._log.info("Entering ACCESS phase")

    dut.penable.value = 1

    # ---------------------------------------------------------
    # Interrupt transaction with reset
    # ---------------------------------------------------------
    dut._log.info("Asserting reset during ACCESS phase")

    dut.presetn.value = 0

    await RisingEdge(dut.pclk)
    await RisingEdge(dut.pclk)

    # ---------------------------------------------------------
    # Release reset
    # ---------------------------------------------------------
    dut._log.info("Releasing reset")

    dut.presetn.value = 1

    await RisingEdge(dut.pclk)

    # ---------------------------------------------------------
    # Cleanup bus signals
    # ---------------------------------------------------------
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0
    dut.paddr.value = 0
    dut.pwdata.value = 0

    await RisingEdge(dut.pclk)

    # ---------------------------------------------------------
    # Verify DUT still operates correctly
    # ---------------------------------------------------------
    verify_addr = 8
    verify_data = 0xCAFEBABE

    dut._log.info("Verifying DUT recovery after reset")

    await apb_write(dut, verify_addr, verify_data)

    read_data = await apb_read(dut, verify_addr)

    assert read_data == verify_data, (
        f"Recovery failed: expected 0x{verify_data:08X}, "
        f"got 0x{read_data:08X}"
    )

    dut._log.info(
        f"PASS  ADDR={verify_addr} DATA=0x{read_data:08X}"
    )

    dut._log.info("============================================================")
    dut._log.info("Reset-During-Transaction Test PASSED")
    dut._log.info("============================================================")