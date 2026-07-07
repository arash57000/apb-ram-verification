daily DV industry style” this into a production-grade cocotb verification environment (UVM-like structure, clean layering, regression-friendly, CI-friendly).

Below is a drop-in blueprint you can implement in your repo. I’ll give you:

✅ recommended folder structure

✅ clean architecture (Agent/Env/Sequences/Scoreboard/Coverage)

✅ regression runner (multi-test, seed control, reproducible)

✅ outputs: junit XML, coverage JSON/summary, logs

✅ code skeletons you can paste

1) Target repo structure (industry-style)
apb-ram-verification/
├─ rtl/
├─ tb/
│  ├─ cocotb/
│  │  ├─ tests/
│  │  │  ├─ test_smoke.py
│  │  │  ├─ test_error.py
│  │  │  ├─ test_random.py
│  │  │  └─ test_full_regression.py
│  │  ├─ env/
│  │  │  ├─ config.py
│  │  │  ├─ txn.py
│  │  │  ├─ agent.py
│  │  │  ├─ driver.py
│  │  │  ├─ monitor.py
│  │  │  ├─ scoreboard.py
│  │  │  ├─ coverage.py
│  │  │  ├─ sequences.py
│  │  │  ├─ env.py
│  │  │  └─ regression.py
│  │  ├─ utils/
│  │  │  ├─ log.py
│  │  │  └─ seed.py
│  │  └─ __init__.py
├─ sim_build/
├─ Makefile
└─ README.md


Key idea: tests are small and readable, and they all reuse the same Env.

2) Architecture (the “UVM mapping”)
UVM concept                      cocotb equivalent
sequence item	                ApbTxn dataclass
sequencer	          sequence generator / async sequence
driver	                       ApbDriver (drives APB)
monitor            	ApbMonitor (samples bus + publishes txns)
scoreboard	         ApbScoreboard (golden model + checks)
coverage	          ApbCoverage (functional bins + export)
env      	                   ApbEnv(wires everything)
regression	       RegressionRunner (runs multiple tests / seeds)


3) Core rules for production-grade DV
✅ Rule A — Driver drives only (but returns observed response)

Driver must return what the DUT responded with (slverr, rdata), because tests/sequences need it.

✅ Rule B — Monitor is source of truth for scoreboard/coverage

Scoreboard + coverage consume monitor transactions, not driver calls.

✅ Rule C — Tests should not contain protocol timing

Tests should read like: “write addr X, then read back, expect …”
Protocol details live in driver/monitor.

✅ Rule D — Regression is seed-controlled + reproducible

Every run logs:

seed

test name

pass/fail

coverage summary

exported coverage JSON

4) Production-grade code skeletons (pasteable)
4.1 env/txn.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class ApbTxn:
    kind: str               # "READ" | "WRITE" | "RESET"
    addr: int = 0
    wdata: int = 0
    rdata: int = 0
    slverr: int = 0
    time_ns: float = 0.0

    def is_legal(self, depth: int) -> bool:
        return 0 <= self.addr < depth

4.2 env/config.py
from dataclasses import dataclass

@dataclass
class ApbConfig:
    depth: int = 32
    data_mask: int = 0xFFFFFFFF
    timeout_cycles: int = 100
    reset_cycles: int = 5
    enable_coverage: bool = True
    enable_scoreboard: bool = True

4.3 env/driver.py (production-grade behavior)

This version:

drives APB SETUP -> ACCESS

waits for PREADY

samples response in ReadOnly() on the cycle PREADY is high

returns observed response

optional check (keep it, but normally scoreboard handles checking)

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly

class ApbDriver:
    def __init__(self, dut, cfg):
        self.dut = dut
        self.cfg = cfg
        self.log = dut._log.getChild("DRV")

    def _t(self) -> float:
        return cocotb.utils.get_sim_time(units="ns")

    async def reset(self):
        # Idle
        self.dut.psel.value = 0
        self.dut.penable.value = 0
        self.dut.pwrite.value = 0
        self.dut.paddr.value = 0
        self.dut.pwdata.value = 0

        self.dut.presetn.value = 0
        self.log.info(f"[{self._t():.1f} ns] RESET assert")

        for _ in range(self.cfg.reset_cycles):
            await RisingEdge(self.dut.pclk)

        self.dut.presetn.value = 1
        await RisingEdge(self.dut.pclk)
        self.log.info(f"[{self._t():.1f} ns] RESET deassert")

    async def write(self, addr: int, data: int, expect_slverr: int | None = None):
        # SETUP
        self.dut.psel.value = 1
        self.dut.penable.value = 0
        self.dut.pwrite.value = 1
        self.dut.paddr.value = addr
        self.dut.pwdata.value = data & self.cfg.data_mask
        await RisingEdge(self.dut.pclk)

        # ACCESS
        self.dut.penable.value = 1
        self.log.info(f"[{self._t():.1f} ns] WRITE addr={addr} data=0x{data & self.cfg.data_mask:08X}")

        # Wait for ready
        for _ in range(self.cfg.timeout_cycles):
            await RisingEdge(self.dut.pclk)
            if int(self.dut.pready.value):
                break
        else:
            raise TimeoutError(f"WRITE timeout waiting for PREADY (addr={addr})")

        # SAMPLE (same cycle as PREADY==1)
        await ReadOnly()
        slverr = int(self.dut.pslverr.value)

        # COMPLETE (drop next cycle)
        await RisingEdge(self.dut.pclk)
        self.dut.psel.value = 0
        self.dut.penable.value = 0

        if expect_slverr is not None:
            assert slverr == int(expect_slverr), f"WRITE addr={addr}: expected PSLVERR={expect_slverr}, got {slverr}"

        return slverr

    async def read(self, addr: int, expect_slverr: int | None = None):
        # SETUP
        self.dut.psel.value = 1
        self.dut.penable.value = 0
        self.dut.pwrite.value = 0
        self.dut.paddr.value = addr
        await RisingEdge(self.dut.pclk)

        # ACCESS
        self.dut.penable.value = 1
        self.log.info(f"[{self._t():.1f} ns] READ  addr={addr}")

        for _ in range(self.cfg.timeout_cycles):
            await RisingEdge(self.dut.pclk)
            if int(self.dut.pready.value):
                break
        else:
            raise TimeoutError(f"READ timeout waiting for PREADY (addr={addr})")

        await ReadOnly()
        rdata = int(self.dut.prdata.value) & self.cfg.data_mask
        slverr = int(self.dut.pslverr.value)

        await RisingEdge(self.dut.pclk)
        self.dut.psel.value = 0
        self.dut.penable.value = 0

        if expect_slverr is not None:
            assert slverr == int(expect_slverr), f"READ addr={addr}: expected PSLVERR={expect_slverr}, got {slverr}"

        return rdata, slverr

4.4 env/monitor.py (single source of truth)

Monitor reconstructs transactions and pushes them to subscribers.

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from .txn import ApbTxn

class ApbMonitor:
    def __init__(self, dut):
        self.dut = dut
        self.log = dut._log.getChild("MON")
        self.subscribers = []  # callbacks(txn)

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def _publish(self, txn: ApbTxn):
        for fn in self.subscribers:
            fn(txn)

    async def run(self):
        self.log.info("APB Monitor run() started")
        prev_reset = 1

        while True:
            await RisingEdge(self.dut.pclk)
            await ReadOnly()

            # reset detect
            rst = int(self.dut.presetn.value)
            if prev_reset == 1 and rst == 0:
                self._publish(ApbTxn(kind="RESET", time_ns=cocotb.utils.get_sim_time("ns")))
            prev_reset = rst

            # handshake sample
            if int(self.dut.psel.value) and int(self.dut.penable.value) and int(self.dut.pready.value):
                is_write = int(self.dut.pwrite.value)
                addr = int(self.dut.paddr.value)
                slverr = int(self.dut.pslverr.value)
                t = cocotb.utils.get_sim_time("ns")

                if is_write:
                    wdata = int(self.dut.pwdata.value)
                    txn = ApbTxn(kind="WRITE", addr=addr, wdata=wdata, slverr=slverr, time_ns=t)
                    self.log.info(f"[{t:.1f} ns] WRITE  addr={addr} data=0x{wdata:08X} slverr={slverr}")
                else:
                    rdata = int(self.dut.prdata.value)
                    txn = ApbTxn(kind="READ", addr=addr, rdata=rdata, slverr=slverr, time_ns=t)
                    self.log.info(f"[{t:.1f} ns] READ   addr={addr} data=0x{rdata:08X} slverr={slverr}")

                self._publish(txn)

4.5 env/scoreboard.py (cleaner + stricter)

This version:

checks legal/illegal slverr behavior

checks read data vs model

tracks counts

provides a hard assert_no_errors() at end

class ApbScoreboard:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = [0] * cfg.depth
        self.errors = 0
        self.checks = 0
        self.illegal_checks = 0

    def on_txn(self, txn):
        if txn.kind == "RESET":
            self.model = [0] * self.cfg.depth
            return

        legal = txn.is_legal(self.cfg.depth)

        # rule: illegal accesses must assert slverr==1
        if not legal:
            self.illegal_checks += 1
            if txn.slverr != 1:
                self.errors += 1
            return

        # legal: slverr must be 0
        if legal and txn.slverr != 0:
            self.errors += 1
            return

        if txn.kind == "WRITE":
            self.model[txn.addr] = txn.wdata & self.cfg.data_mask

        elif txn.kind == "READ":
            exp = self.model[txn.addr] & self.cfg.data_mask
            got = txn.rdata & self.cfg.data_mask
            self.checks += 1
            if got != exp:
                self.errors += 1

    def summary(self):
        return {
            "checks": self.checks,
            "illegal_checks": self.illegal_checks,
            "errors": self.errors,
        }

    def assert_no_errors(self):
        s = self.summary()
        assert s["errors"] == 0, f"Scoreboard errors={s['errors']} checks={s['checks']} illegal={s['illegal_checks']}"

4.6 env/coverage.py (functional coverage with export)
import json
from pathlib import Path

class ApbCoverage:
    def __init__(self, cfg):
        self.cfg = cfg
        self.bins = {
            "read": 0,
            "write": 0,
            "reset": 0,
            "legal_addr": 0,
            "illegal_addr": 0,
            "slverr_0": 0,
            "slverr_1": 0,
            "boundary_0": 0,
            "boundary_last": 0,
            "back_to_back": 0,
        }
        self._prev_kind = None

    def on_txn(self, txn):
        if txn.kind == "RESET":
            self.bins["reset"] += 1
            self._prev_kind = "RESET"
            return

        if txn.kind == "READ":
            self.bins["read"] += 1
        elif txn.kind == "WRITE":
            self.bins["write"] += 1

        legal = txn.is_legal(self.cfg.depth)
        self.bins["legal_addr" if legal else "illegal_addr"] += 1

        self.bins["slverr_0" if txn.slverr == 0 else "slverr_1"] += 1

        if txn.addr == 0:
            self.bins["boundary_0"] += 1
        if txn.addr == self.cfg.depth - 1:
            self.bins["boundary_last"] += 1

        if self._prev_kind in ("READ", "WRITE") and txn.kind in ("READ", "WRITE"):
            self.bins["back_to_back"] += 1

        self._prev_kind = txn.kind

    def report(self):
        return dict(self.bins)

    def export_json(self, out_dir="out", name="func_coverage.json"):
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        p = Path(out_dir) / name
        p.write_text(json.dumps(self.bins, indent=2))
        return str(p)

4.7 env/env.py (wires everything)
import cocotb
from .agent import ApbAgent
from .scoreboard import ApbScoreboard
from .coverage import ApbCoverage
from .monitor import ApbMonitor

class ApbEnv:
    def __init__(self, dut, cfg):
        self.dut = dut
        self.cfg = cfg
        self.log = dut._log.getChild("ENV")

        self.agent = ApbAgent(dut, cfg)     # driver inside
        self.monitor = ApbMonitor(dut)

        self.scoreboard = ApbScoreboard(cfg) if cfg.enable_scoreboard else None
        self.coverage = ApbCoverage(cfg) if cfg.enable_coverage else None

        if self.scoreboard:
            self.monitor.subscribe(self.scoreboard.on_txn)
        if self.coverage:
            self.monitor.subscribe(self.coverage.on_txn)

    async def start(self):
        cocotb.start_soon(self.monitor.run())

    async def reset(self):
        await self.agent.drv.reset()


env/agent.py

from .driver import ApbDriver

class ApbAgent:
    def __init__(self, dut, cfg):
        self.drv = ApbDriver(dut, cfg)

5) Tests become small + clean (real regression style)
tests/test_smoke.py
import cocotb
from tb.cocotb.env.config import ApbConfig
from tb.cocotb.env.env import ApbEnv

@cocotb.test()
async def test_smoke(dut):
    cfg = ApbConfig()
    env = ApbEnv(dut, cfg)
    await env.start()

    await env.reset()
    await env.agent.drv.write(12, 0x23, expect_slverr=0)
    rdata, slv = await env.agent.drv.read(12, expect_slverr=0)
    assert rdata == 0x23

    if env.scoreboard:
        env.scoreboard.assert_no_errors()
    if env.coverage:
        dut._log.info(f"Coverage report: {env.coverage.report()}")

tests/test_error.py
import cocotb
from tb.cocotb.env.config import ApbConfig
from tb.cocotb.env.env import ApbEnv

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

tests/test_full_regression.py

This is your “apb_ram_full_regression” but now it’s composed cleanly.

6) Regression runner (CI-friendly, seed control)

In cocotb, regression is usually “multiple cocotb tests” + pytest or make TESTCASE=....
But you can also add a higher-level “scenario runner” inside a single test if you want.

Production pattern:

multiple tests: smoke/error/random/reset

run them in CI with different seeds

We can add env/regression.py later to organize scenarios inside one test if you want.

7) Outputs (what production teams expect)

Create an out/ folder containing:

func_coverage.json

coverage_summary.txt (optional)

results.xml (cocotb already creates this)

logs (if you add file handlers)

Add this at end of each test:

if env.coverage:
    path = env.coverage.export_json(out_dir="out")
    dut._log.info(f"Functional coverage JSON exported to: {path}")

8) What you should do next (no waiting, immediate steps)

Create folders exactly like section 1

Move your current driver/monitor/scoreboard into those modules

Convert your current full regression test into:

test_smoke.py

test_error.py

test_random.py

test_reset.py

test_full_regression.py (optional orchestration)
