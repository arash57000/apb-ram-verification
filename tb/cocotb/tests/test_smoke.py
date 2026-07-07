import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_smoke(dut):

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== SMOKE TEST ==========")

    await reset_dut(dut)

    addr = 0
    data = 0xA5

    cocotb.log.info(
        f"WRITE ADDR={addr} DATA=0x{data:02X}"
    )

    await apb_write(dut, addr, data)

    rdata = await apb_read(dut, addr)

    assert rdata == data, (
        f"Expected 0x{data:02X}, "
        f"Got 0x{rdata:02X}"
    )

    cocotb.log.info("Smoke test PASSED.")
