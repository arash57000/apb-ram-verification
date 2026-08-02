from dataclasses import dataclass

@dataclass
class ApbConfig:
    depth: int = 32
    data_mask: int = 0xFFFFFFFF
    timeout_cycles: int = 100
    reset_cycles: int = 5
    enable_coverage: bool = True
    enable_scoreboard: bool = True

