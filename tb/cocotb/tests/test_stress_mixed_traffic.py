import random

import cocotb

from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_stress_mixed_traffic(dut):
    """
    Stress Test

    Verify reliable RAM operation during a long sequence
    of randomly mixed APB reads and writes.

    Expected:
        - Every write updates the expected memory model
        - Every read matches the expected stored value
        - No corruption occurs during mixed traffic
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    transaction_count = 1000
    random_seed = 12345

    rng = random.Random(random_seed)

    expected_memory = {
        addr: 0
        for addr in range(32)
    }

    write_count = 0
    read_count = 0

    cocotb.log.info(
        f"Starting mixed-traffic stress test: "
        f"transactions={transaction_count}, "
        f"seed={random_seed}"
    )

    for transaction in range(transaction_count):

        addr = rng.randrange(32)
        do_write = rng.choice([True, False])

        if do_write:

            data = rng.getrandbits(32)

            await apb_write(
                dut,
                addr,
                data
            )

            expected_memory[addr] = data
            write_count += 1

        else:

            actual = await apb_read(
                dut,
                addr
            )

            expected = expected_memory[addr]

            cocotb.log.info(
                f"CHECK ADDR={addr:02d} "
                f"EXPECTED=0x{expected:08X} "
                f"READ=0x{actual:08X}"
            )

            assert actual == expected, (
                f"Transaction {transaction}: "
                f"Address {addr}: "
                f"Expected 0x{expected:08X}, "
                f"Got 0x{actual:08X}"
            )

            read_count += 1

        if (transaction + 1) % 200 == 0:
            cocotb.log.info(
                f"Completed {transaction + 1} mixed transactions"
            )

    cocotb.log.info(
        f"Mixed traffic summary: "
        f"Writes={write_count}, "
        f"Reads={read_count}"
    )

    cocotb.log.info(
        "PASS: Stress mixed-traffic test completed successfully."
    )
