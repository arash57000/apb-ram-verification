import json
from pathlib import Path


class ApbCoverage:
    DATA_PATTERNS = {
        0x00000000: "all_zeros",
        0xFFFFFFFF: "all_ones",
        0xAAAAAAAA: "alternating_A",
        0x55555555: "alternating_5",
        0x80000000: "msb_only",
        0x00000001: "lsb_only",
        0x7FFFFFFF: "all_except_msb",
        0xFFFFFFFE: "all_except_lsb",
    }

    def __init__(self, depth=32):
        self.depth = depth
        self._last = None

        self.bins = {
            "operation": {
                "read": 0,
                "write": 0,
            },
            "legal_address": {
                str(addr): 0 for addr in range(depth)
            },
            "address_type": {
                "legal": 0,
                "illegal": 0,
            },
            "boundary": {
                "address_0": 0,
                f"address_{depth - 1}": 0,
            },
            "error": {
                "slverr_0": 0,
                "slverr_1": 0,
            },
            "data_pattern": {
                name: 0 for name in self.DATA_PATTERNS.values()
            },
            "sequence": {
                "back_to_back": 0,
                "write_read_same_address": 0,
            },
            "operation_address_type_cross": {
                "read_legal": 0,
                "read_illegal": 0,
                "write_legal": 0,
                "write_illegal": 0,
            },
            "operation_legal_address_cross": {
                f"read_address_{addr}": 0
                for addr in range(depth)
            } | {
                f"write_address_{addr}": 0
                for addr in range(depth)
            },
            "reset": {
                "observed": 0,
            },
        }

    def on_txn(self, txn):
        if txn.kind == "RESET":
            self.bins["reset"]["observed"] += 1
            self._last = txn
            return

        if txn.kind not in ("READ", "WRITE"):
            return

        operation = txn.kind.lower()
        legal = 0 <= txn.addr < self.depth
        address_type = "legal" if legal else "illegal"

        self.bins["operation"][operation] += 1
        self.bins["address_type"][address_type] += 1

        cross_name = f"{operation}_{address_type}"
        self.bins["operation_address_type_cross"][cross_name] += 1

        if legal:
            self.bins["legal_address"][str(txn.addr)] += 1

            legal_cross = f"{operation}_address_{txn.addr}"
            self.bins["operation_legal_address_cross"][legal_cross] += 1

            if txn.addr == 0:
                self.bins["boundary"]["address_0"] += 1

            if txn.addr == self.depth - 1:
                boundary_name = f"address_{self.depth - 1}"
                self.bins["boundary"][boundary_name] += 1

        if txn.slverr == 0:
            self.bins["error"]["slverr_0"] += 1
        else:
            self.bins["error"]["slverr_1"] += 1

        if txn.kind == "WRITE" and txn.wdata is not None:
            pattern_name = self.DATA_PATTERNS.get(txn.wdata)

            if pattern_name is not None:
                self.bins["data_pattern"][pattern_name] += 1

        if self._last is not None:
            if (
                self._last.kind in ("READ", "WRITE")
                and txn.kind in ("READ", "WRITE")
            ):
                self.bins["sequence"]["back_to_back"] += 1

            if (
                self._last.kind == "WRITE"
                and txn.kind == "READ"
                and self._last.addr == txn.addr
            ):
                self.bins["sequence"]["write_read_same_address"] += 1

        self._last = txn

    def _all_bin_values(self):
        for group in self.bins.values():
            yield from group.values()

    def coverage_summary(self):
        values = list(self._all_bin_values())

        total_bins = len(values)
        covered_bins = sum(value > 0 for value in values)
        uncovered_bins = total_bins - covered_bins

        percentage = (
            100.0 * covered_bins / total_bins
            if total_bins
            else 100.0
        )

        return {
            "covered_bins": covered_bins,
            "total_bins": total_bins,
            "uncovered_bins": uncovered_bins,
            "coverage_percent": round(percentage, 2),
        }

    def uncovered_bins(self):
        uncovered = []

        for group_name, group in self.bins.items():
            for bin_name, count in group.items():
                if count == 0:
                    uncovered.append(f"{group_name}.{bin_name}")

        return uncovered

    def report(self):
        return {
            "summary": self.coverage_summary(),
            "bins": self.bins,
            "uncovered_bins": self.uncovered_bins(),
        }

    def export_json(self, path: str):
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(
            json.dumps(self.report(), indent=2) + "\n"
        )

        return str(output_path)