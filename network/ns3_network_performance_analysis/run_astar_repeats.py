
#!/usr/bin/env python3
"""Run paired multi-client A* simulations using local NS-3.45."""

import argparse
import hashlib
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
SOURCE = PROJECT / "repeat_simulations" / "astar-multiclient.cc"

NS3_DIR = Path.home() / "ns-allinone-3.45" / "ns-3.45"
SCRATCH_SOURCE = NS3_DIR / "scratch" / "astar-multiclient.cc"

RAW_DIR = PROJECT / "results" / "raw" / "astar_repeats"
OUTPUT_DIR = PROJECT / "results" / "processed" / "astar_repeats"
LOG_DIR = OUTPUT_DIR / "run_logs"


def run_command(command, capture=False):
    return subprocess.run(
        command,
        cwd=NS3_DIR,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


def validate_xml(path):
    root = ET.parse(path).getroot()
    flow_stats = root.find("FlowStats")
    if root.tag != "FlowMonitor" or flow_stats is None:
        raise ValueError(f"Invalid FlowMonitor XML: {path}")
    if not flow_stats.findall("Flow"):
        raise ValueError(f"No flows found in FlowMonitor XML: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", nargs="+", type=int, required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument(
        "--failure-type", choices=("link", "node"), default="link"
    )
    args = parser.parse_args()

    if args.seed < 1 or any(run < 1 for run in args.runs):
        parser.error("Seed and run numbers must be positive.")
    if len(set(args.runs)) != len(args.runs):
        parser.error("Run numbers must be distinct.")

    if not SOURCE.is_file():
        raise FileNotFoundError(f"Simulation source missing: {SOURCE}")
    if not (NS3_DIR / "ns3").is_file():
        raise FileNotFoundError(f"NS-3 wrapper missing: {NS3_DIR / 'ns3'}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    planned = []
    for run in args.runs:
        for scenario, failure in (("baseline", False), ("failure", True)):
            stem = f"{scenario}-run-{run:04d}-seed-{args.seed}"
            planned.append((
                scenario,
                failure,
                run,
                RAW_DIR / f"{stem}.xml",
                LOG_DIR / f"{stem}.txt",
            ))

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

    if SCRATCH_SOURCE.exists():
        existing_hash = hashlib.sha256(
            SCRATCH_SOURCE.read_bytes()
        ).hexdigest()
        source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        if existing_hash != source_hash:
            raise FileExistsError(
                f"Refusing to overwrite different source: {SCRATCH_SOURCE}"
            )
    else:
        SCRATCH_SOURCE.parent.mkdir(parents=True, exist_ok=True)
        SCRATCH_SOURCE.write_bytes(SOURCE.read_bytes())

    print("Building local NS-3 simulation...")
    run_command(["./ns3", "build", "scratch/astar-multiclient"])

    for scenario, failure, run, xml_path, log_path in planned:
        print(f"Running {scenario}: seed={args.seed}, run={run}")

        command = [
            "./ns3",
            "run",
            "scratch/astar-multiclient",
            "--",
            f"--run={run}",
            f"--seed={args.seed}",
            f"--failure={'true' if failure else 'false'}",
            f"--failureType={args.failure_type}",
            f"--output={xml_path}",
        ]

        result = run_command(command, capture=True)
        log_path.write_text(result.stdout, encoding="utf-8")

        expected = f"RUN_METADATA scenario={scenario} seed={args.seed} run={run}"
        if expected not in result.stdout:
            raise RuntimeError(
                f"Expected metadata not found; inspect {log_path}"
            )

        if not xml_path.is_file():
            raise FileNotFoundError(
                f"Simulation did not create XML: {xml_path}"
            )

        validate_xml(xml_path)
        print(f"Verified FlowMonitor XML: {xml_path}")

    print("Paired A* runs completed successfully.")
    print("Analyze results with performance_analysis.py.")


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
