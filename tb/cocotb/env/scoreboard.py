class ApbScoreboard:
    """
    APB Scoreboard (UVM-style)

    - Uses monitor transactions as source of truth
    - Reference memory model
    - Checks PSLVERR rules
    - Reports mismatches with detailed debug    
    """

    def __init__(self, cfg, name="SCO", max_error_logs=20):
        # Configuration
        self.cfg = cfg
        self.depth = cfg.depth
        self.name = name

        # Memory model
        self.model = [0] * self.depth

        # Counters
        self.errors = 0
        self.checks = 0
        self.read_compares = 0
        self.write_updates = 0

        self.legal_ops = 0
        self.illegal_ops = 0
        self.slverr_expected_1 = 0
        self.slverr_expected_0 = 0

        # Logging control
        self.max_error_logs = max_error_logs
        self._error_logs = 0

        # Safety check
        assert isinstance(self.depth, int), "cfg.depth must be int"

    # ------------------------------------------
    # Helpers
    # ------------------------------------------
    def _is_legal(self, addr: int) -> bool:
        return 0 <= addr < self.depth

    def _err(self, msg: str):
        self.errors += 1
        if self._error_logs < self.max_error_logs:
            print(f"[{self.name} ERROR] {msg}")
            self._error_logs += 1

    # ------------------------------------------
    # Main entry from monitor
    # ------------------------------------------
    def on_txn(self, txn):
        # RESET: clear model
        if txn.kind == "RESET":
            self.model = [0] * self.depth
            return

        # Validate transaction type
        if txn.kind not in ("READ", "WRITE"):
            self._err(f"Unknown txn.kind={txn.kind} t={txn.time_ns}")
            return

        is_legal = self._is_legal(txn.addr)

        # ------------------------------------------
        # PSLVERR checking
        # ------------------------------------------
        if is_legal:
            self.legal_ops += 1
            self.slverr_expected_0 += 1

            if txn.slverr != 0:
                self._err(
                    f"Unexpected PSLVERR on {txn.kind} "
                    f"addr={txn.addr} slverr={txn.slverr} t={txn.time_ns}"
                )
                return
        else:
            self.illegal_ops += 1
            self.slverr_expected_1 += 1

            if txn.slverr != 1:
                self._err(
                    f"Missing PSLVERR on illegal {txn.kind} "
                    f"addr={txn.addr} slverr={txn.slverr} t={txn.time_ns}"
                )
            return  # Do not update model

        # ------------------------------------------
        # Functional checking
        # ------------------------------------------
        if txn.kind == "WRITE":
            if txn.wdata is None:
                self._err(f"WRITE missing wdata addr={txn.addr} t={txn.time_ns}")
                return

            self.model[txn.addr] = txn.wdata & 0xFFFFFFFF
            self.write_updates += 1
            self.checks += 1

        elif txn.kind == "READ":
            if txn.rdata is None:
                self._err(f"READ missing rdata addr={txn.addr} t={txn.time_ns}")
                return

            exp = self.model[txn.addr] & 0xFFFFFFFF
            got = txn.rdata & 0xFFFFFFFF

            self.read_compares += 1
            self.checks += 1

            if got != exp:
                self._err(
                    f"READ mismatch addr={txn.addr} "
                    f"exp=0x{exp:08X} got=0x{got:08X} t={txn.time_ns}"
                )

    # ------------------------------------------
    # Summary
    # ------------------------------------------
    def summary(self):
        return {
            "checks": self.checks,
            "errors": self.errors,
            "read_compares": self.read_compares,
            "write_updates": self.write_updates,
            "legal_ops": self.legal_ops,
            "illegal_ops": self.illegal_ops,
            "slverr_expected_0": self.slverr_expected_0,
            "slverr_expected_1": self.slverr_expected_1,
        }
        
    # ------------------------------------------
    # assert_no_errors
    # ------------------------------------------       
        
        
    def assert_no_errors(self):
        if self.errors > 0:
            raise AssertionError(
                  f"[{self.name}] Scoreboard detected {self.errors} errors"
            )
        else:
            print(f"[{self.name}] Scoreboard PASS — no errors")
