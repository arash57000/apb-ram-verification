#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def merge_coverage(input_dir: Path):
    input_files = sorted(input_dir.glob("*.json"))

    if not input_files:
        raise SystemExit(
            f"ERROR: No functional coverage files found in {input_dir}"
        )

    merged_bins = {}

    for input_file in input_files:
        report = json.loads(input_file.read_text())
        report_bins = report.get("bins", {})

        for group_name, group_bins in report_bins.items():
            merged_group = merged_bins.setdefault(group_name, {})

            for bin_name, count in group_bins.items():
                merged_group[bin_name] = (
                    merged_group.get(bin_name, 0) + int(count)
                )

    all_bins = [
        (group_name, bin_name, count)
        for group_name, group_bins in merged_bins.items()
        for bin_name, count in group_bins.items()
    ]

    total_bins = len(all_bins)
    covered_bins = sum(
        count > 0 for _, _, count in all_bins
    )
    uncovered_bins_count = total_bins - covered_bins

    coverage_percent = (
        100.0 * covered_bins / total_bins
        if total_bins
        else 100.0
    )

    uncovered_bins = [
        f"{group_name}.{bin_name}"
        for group_name, bin_name, count in all_bins
        if count == 0
    ]

    return {
        "summary": {
            "covered_bins": covered_bins,
            "total_bins": total_bins,
            "uncovered_bins": uncovered_bins_count,
            "coverage_percent": round(coverage_percent, 2),
        },
        "source_files": [
            input_file.name for input_file in input_files
        ],
        "bins": merged_bins,
        "uncovered_bins": uncovered_bins,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Merge APB RAM functional coverage reports."
    )

    parser.add_argument(
        "--input-dir",
        default="functional_coverage/tests",
        help="Directory containing per-test JSON reports.",
    )

    parser.add_argument(
        "--output",
        default="functional_coverage/merged/regression.json",
        help="Merged JSON report path.",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)

    merged_report = merge_coverage(input_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(merged_report, indent=2) + "\n"
    )

    summary = merged_report["summary"]

    print()
    print("=" * 60)
    print("        APB RAM FUNCTIONAL COVERAGE REPORT")
    print("=" * 60)
    print(f"Source files    : {len(merged_report['source_files'])}")
    print(f"Covered bins    : {summary['covered_bins']}")
    print(f"Total bins      : {summary['total_bins']}")
    print(f"Uncovered bins  : {summary['uncovered_bins']}")
    print(f"Coverage        : {summary['coverage_percent']:.2f}%")
    print("=" * 60)

    if merged_report["uncovered_bins"]:
        print("Uncovered functional coverage bins:")

        for bin_name in merged_report["uncovered_bins"]:
            print(f"  - {bin_name}")
    else:
        print("All functional coverage bins are covered.")

    print()
    print(f"Merged report: {output_path}")


if __name__ == "__main__":
    main()