import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)

DATA_PATTERNS = [
    0x00000000,
    0xFFFFFFFF,
    0xAAAAAAAA,
    0x55555555,
    0x80000000,
    0x00000001,
    0x7FFFFFFF,
    0xFFFFFFFE,
]

TEST_ADDRESSES = [
    0,
    15,
    31,
]


@cocotb.test()
async def test_data_patterns(dut):

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    cocotb.log.info("=" * 60)
    cocotb.log.info("Starting Data Pattern Test")
    cocotb.log.info("=" * 60)

    await reset_dut(dut)

    for addr in TEST_ADDRESSES:

        cocotb.log.info(f"\nTesting Address {addr}")

        for pattern in DATA_PATTERNS:

            await apb_write(dut, addr, pattern)

            data = await apb_read(dut, addr)

            assert data == pattern, (
                f"Mismatch at address {addr}: "
                f"expected 0x{pattern:08X}, "
                f"got 0x{data:08X}"
            )

            cocotb.log.info(
                f"PASS  ADDR={addr:02d} "
                f"DATA=0x{pattern:08X}"
            )

    cocotb.log.info("=" * 60)
    cocotb.log.info("Data Pattern Test PASSED")
    cocotb.log.info("=" * 60)