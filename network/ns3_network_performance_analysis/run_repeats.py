
#!/usr/bin/env python3
"""Run repeatable NS-3 baseline/failure scenarios locally, without Docker."""

import argparse
import hashlib
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT / "repeat_simulations"
RAW_DIR = PROJECT / "results" / "raw" / "repeats"
LOG_DIR = PROJECT / "results" / "processed" / "repeats" / "run_logs"

NS3_DIR = Path.home() / "ns-allinone-3.45" / "ns-3.45"
SCRATCH_DIR = NS3_DIR / "scratch"

SOURCES = {
    "member4-repeat-impl.h": SOURCE_DIR / "member4-repeat-impl.h",
    "member4-repeat-baseline.cc": SOURCE_DIR / "member4-repeat-baseline.cc",
    "member4-repeat-failure.cc": SOURCE_DIR / "member4-repeat-failure.cc",
}


def run_command(command, *, capture=False):
    return subprocess.run(
        command,
        cwd=NS3_DIR,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install_sources():
    """Copy sources only when the destination is absent or identical."""
    for name, source in SOURCES.items():
        if not source.is_file():
            raise FileNotFoundError(f"Project source missing: {source}")

        destination = SCRATCH_DIR / name

        if destination.exists():
            if sha256(destination) != sha256(source):
                raise FileExistsError(
                    f"Refusing to overwrite different local source: {destination}"
                )
            print(f"Verified existing source: {destination}")
        else:
            shutil.copy2(source, destination)
            print(f"Copied source into scratch: {destination}")


def validate_xml(path):
    root = ET.parse(path).getroot()
    flow_stats = root.find("FlowStats")

    if root.tag != "FlowMonitor" or flow_stats is None:
        raise ValueError(f"Not a valid FlowMonitor XML: {path}")

    if not flow_stats.findall("Flow"):
        raise ValueError(f"FlowMonitor XML has no flow records: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--runs", nargs="+", type=int, required=True,
        help="Distinct positive NS-3 run numbers, e.g. --runs 101 102",
    )
    parser.add_argument(
        "--seed", type=int, default=1,
        help="NS-3 seed held constant while run numbers vary",
    )
    args = parser.parse_args()

    if args.seed < 1 or any(run < 1 for run in args.runs):
        parser.error("Seed and run numbers must be positive integers.")

    if len(set(args.runs)) != len(args.runs):
        parser.error("Run numbers must be distinct.")

    if not (NS3_DIR / "ns3").is_file():
        raise FileNotFoundError(f"NS-3 wrapper not found in {NS3_DIR}")

    scenarios = {
        "baseline": "member4-repeat-baseline",
        "failure": "member4-repeat-failure",
    }

    planned = []
    for run_number in args.runs:
        for scenario, target in scenarios.items():
            stem = f"{scenario}-run-{run_number:04d}-seed-{args.seed}"
            xml_path = RAW_DIR / f"{stem}.xml"
            log_path = LOG_DIR / f"{stem}.txt"
            planned.append(
                (scenario, target, run_number, xml_path, log_path)
            )

    # Check every destination before starting any simulation.
    collisions = [
        str(path)
        for _, _, _, xml_path, log_path in planned
        for path in (xml_path, log_path)
        if path.exists()
    ]
    if collisions:
        raise FileExistsError(
            "Refusing to overwrite existing outputs: "
            + ", ".join(collisions)
        )

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    install_sources()

    for target in scenarios.values():
        print(f"Building {target}...")
        run_command(["./ns3", "build", f"scratch/{target}"])

    for scenario, target, run_number, xml_path, log_path in planned:
        print(f"Running {scenario}: seed={args.seed}, run={run_number}")

        command = [
            "./ns3", "run", f"scratch/{target}", "--",
            f"--run={run_number}",
            f"--seed={args.seed}",
        ]

        result = run_command(command, capture=True)
        log_path.write_text(result.stdout, encoding="utf-8")

        expected = (
            f"RUN_METADATA scenario={scenario} "
            f"seed={args.seed} run={run_number}"
        )
        if expected not in result.stdout:
            raise RuntimeError(
                f"Run metadata mismatch; inspect {log_path}"
            )

        # The source must write its XML to the path expected below.
        # Confirm the actual output path in the simulation source before use.
        possible_xml = [
            SCRATCH_DIR / f"member4-{scenario}-run-{run_number}-seed-{args.seed}.xml",
            NS3_DIR / f"member4-{scenario}-run-{run_number}-seed-{args.seed}.xml",
        ]
        generated = next((path for path in possible_xml if path.is_file()), None)

        if generated is None:
            raise FileNotFoundError(
                "Could not locate generated FlowMonitor XML. "
                f"Inspect log: {log_path}"
            )

        shutil.copy2(generated, xml_path)
        validate_xml(xml_path)
        print(f"Verified FlowMonitor XML: {xml_path}")

    print("Repeat runs completed.")
    print(
        "Analyze with: python3 performance_analysis.py "
        "--repeat-xml-dir results/raw/repeats"
    )


if __name__ == "__main__":
    try:
        main()
    except (
        subprocess.CalledProcessError,
        FileExistsError,
        FileNotFoundError,
        RuntimeError,
        ValueError,
        ET.ParseError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stdout:
            print(error.stdout, file=sys.stderr)
        sys.exit(1)
