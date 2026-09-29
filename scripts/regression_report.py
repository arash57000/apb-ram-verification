from pathlib import Path
import sys
import xml.etree.ElementTree as ET

results_dir = Path("results/tests")
report_file = Path("results/regression_report.txt")

xml_files = sorted(results_dir.glob("*.xml"))
if not xml_files:
    sys.exit(f"No test results found in {results_dir}")

rows = []
for xml_file in xml_files:
    root = ET.parse(xml_file).getroot()
    for case in root.iter("testcase"):
        if case.find("failure") is not None:
            status = "FAIL"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        else:
            status = "PASS"

        rows.append((xml_file.stem, case.get("name", "unknown"), status))

if not rows:
    sys.exit("No testcases found in the XML files")

lines = ["APB RAM REGRESSION REPORT", "=" * 65]
for target, name, status in rows:
    lines.append(f"{target:<28} {status:<6} {name}")

passed = sum(status == "PASS" for _, _, status in rows)
failed = sum(status in ("FAIL", "ERROR") for _, _, status in rows)
skipped = sum(status == "SKIP" for _, _, status in rows)
lines.append("=" * 65)
lines.append(
    f"Total: {len(rows)}  Passed: {passed}  "
    f"Failed: {failed}  Skipped: {skipped}"
)

report = "\n".join(lines) + "\n"
report_file.parent.mkdir(parents=True, exist_ok=True)
report_file.write_text(report, encoding="utf-8")
print(report, end="")

sys.exit(0 if failed == 0 and skipped == 0 else 1)
