import cocotb
import random

from env.apb_driver import ApbDriver
from env.apb_monitor import ApbMonitor
from env.scoreboard import ApbScoreboard
from env.regression import build_env
from tb.sequences.apb_sequence import ApbSequence

@cocotb.test()
async def test_random(dut):

    dut._log.info("===== RANDOM BASIC TEST START =====")

    env = await build_env(dut, depth=32)
    drv = env.driver
    sco = env.scoreboard
    cov = env.coverage

    seq = ApbSequence()

    # --------------------
    # Reset
    # --------------------
    await drv.reset()

    # --------------------
    # Random traffic
    # --------------------
    for i in range(500):

        op, addr, data = seq.next_txn()

        dut._log.info(f"[TXN {i}] {op} addr={addr} data={data}")

        if op == "reset":
            await drv.reset()

        elif op == "write":
            await drv.write(addr, data)

        elif op == "read":
            await drv.read(addr)

    # --------------------
    # Final checks
    # --------------------
    summ = sco.summary()

    assert summ["errors"] == 0, f"Random regression failed: {summ}"

    dut._log.info("===== RANDOM TEST PASS =====")
    dut._log.info(f"Scoreboard: {summ}")
    dut._log.info(f"Coverage:   {cov.report()}")
