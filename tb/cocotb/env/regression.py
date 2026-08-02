import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from tb.cocotb.agents.apb_driver import ApbDriver
from tb.cocotb.agents.apb_monitor import ApbMonitor
from env.scoreboard import ApbScoreboard
from env.apb_coverage import ApbCoverage


class RegressionEnv:
    """
    Regression environment container
    (UVM-style env abstraction)
    """

    def __init__(self, dut, depth=32):
        self.dut = dut
        self.depth = depth

        # Clock
        self.clk = dut.pclk

        # Components
        self.driver = ApbDriver(dut)
        self.monitor = ApbMonitor(dut, self.clk)
        self.scoreboard = ApbScoreboard(depth=depth)
        self.coverage = ApbCoverage(depth=depth)

        # Connections (UVM analysis ports style)
        self.monitor.subscribe(self.scoreboard.on_txn)
        self.monitor.subscribe(self.coverage.on_txn)

    async def start(self):
        # Start clock
        cocotb.start_soon(Clock(self.clk, 10, units="ns").start())
        await Timer(1, units="ns")

        # Start monitor
        cocotb.start_soon(self.monitor.run())

    def summary(self):
        return {
            "scoreboard": self.scoreboard.summary(),
            "coverage": self.coverage.report(),
        }


async def build_env(dut, depth=32):
    """
    Factory for regression environment
    """
    env = RegressionEnv(dut, depth=depth)
    await env.start()
    return env

