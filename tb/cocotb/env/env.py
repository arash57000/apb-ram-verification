# APB verification environment integration.
import cocotb
from .agent import ApbAgent
from .scoreboard import ApbScoreboard
from .apb_coverage import ApbCoverage
from tb.cocotb.agents.apb_monitor import ApbMonitor



class ApbEnv:
    def __init__(self, dut, cfg):
        self.dut = dut
        self.cfg = cfg
        self.log = dut._log.getChild("ENV")

        self.agent = ApbAgent(dut, cfg)     # driver inside
        self.monitor = ApbMonitor(dut)

        self.scoreboard = ApbScoreboard(cfg) if cfg.enable_scoreboard else None
        self.coverage = ApbCoverage(cfg.depth) if cfg.enable_coverage else None

        if self.scoreboard:
            self.monitor.subscribe(self.scoreboard.on_txn)
        if self.coverage:
            self.monitor.subscribe(self.coverage.on_txn)

    async def start(self):
        cocotb.start_soon(self.monitor.run())

    async def reset(self):
        await self.agent.drv.reset()

