from tb.cocotb.agents.apb_driver import ApbDriver
from tb.cocotb.agents.apb_monitor import ApbMonitor

class ApbAgent:
    def __init__(self, dut, cfg):
        self.drv = ApbDriver(dut, cfg)

