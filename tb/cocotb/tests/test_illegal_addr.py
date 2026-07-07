import cocotb
from tb.cocotb.env.config import ApbConfig
from env.env import ApbEnv
from env.apb_driver import ApbDriver
from env.apb_monitor import ApbMonitor
from env.scoreboard import ApbScoreboard
from env.regression import build_env

@cocotb.test()
async def test_illegal_addr(dut):
    cfg = ApbConfig(depth=32)
    env = ApbEnv(dut, cfg)
    await env.start()

    await env.reset()
    await env.agent.drv.write(45, 0x3333, expect_slverr=1)
    await env.agent.drv.read(45, expect_slverr=1)

    if env.scoreboard:
        env.scoreboard.assert_no_errors()

