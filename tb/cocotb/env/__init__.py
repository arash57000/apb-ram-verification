"""
APB RAM Verification Environment
================================

Cocotb-based DV infrastructure with UVM-style architecture:

Components:
- driver      : stimulus
- monitor     : protocol sampling
- scoreboard  : functional checking
- coverage    : functional coverage
- sequences   : stimulus generation
- regression  : environment orchestration
- log         : unified logging
- seed        : reproducible randomness
"""

from .log import dv_log
from .seed import init_seed
from tb.cocotb.sequences.sequences import (
    BaseSequence,
    RandomSequence,
    DirectedSequence,
    ResetStressSequence,
)

