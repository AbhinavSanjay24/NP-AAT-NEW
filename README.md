# Priority-Based Dynamic Routing in Multi-Client Multi-Server Networks

## Overview

This project implements a priority-based dynamic routing system for multi-client, multi-server wireless networks using **NS-3.45**. It explores how routing decisions can be influenced by client priorities, link distance, and congestion, while evaluating network performance under normal and link-failure conditions.

The system uses an A*-based path-selection algorithm to identify suitable routes between clients and servers through relay nodes. Network performance is evaluated using simulation results, statistical analysis, and graphical visualizations.

## Objectives

- Design a multi-client, multi-server wireless network topology.
- Implement priority-aware routing using the A* search algorithm.
- Consider link distance and congestion when evaluating routes.
- Simulate link failures and recovery events.
- Measure throughput, packet loss, packet delivery ratio, and end-to-end delay.
- Compare baseline and failure scenarios using repeated simulation runs.
- Visualize performance metrics using graphs and summary reports.

## Technology Stack

- **NS-3.45:** Wireless network simulation
- **C++:** Network simulation and routing implementation
- **Python 3:** Performance analysis and data processing
- **Pandas and NumPy:** Data processing and statistical analysis
- **Matplotlib:** Graph generation
- **HTML, CSS, JavaScript:** Browser-based network visualization

## Network Topology

The simulated network consists of:

- **4 clients**
- **4 servers**
- **8 relay nodes**
- Primary and backup relay paths

Different priorities are assigned to client traffic. The A*-based routing model evaluates candidate paths using a cost function that incorporates link distance and congestion adjusted by priority.

The wireless network is configured using IEEE 802.11g ad hoc Wi-Fi, IPv4 addressing, and packet-based communication.

## Project Structure

```text
priority_aware_routing/
├── browser_demo/
│   └── index.html
├── network/
│   └── ns3_network_performance_analysis/
│       ├── performance_analysis.py
│       ├── run_astar_repeats.py
│       └── results/
│           ├── raw/
│           │   └── astar_repeats/
│           ├── processed/
│           │   └── astar_repeats/
│           └── graphs/
└── README.md
```

The main NS-3 simulation source file used during development is `astar-multiclient.cc`, located in the NS-3 `scratch/` directory. Ensure the source file is included or its location is documented when sharing the complete project.

## Requirements

- Ubuntu Linux or Windows Subsystem for Linux (WSL)
- NS-3.45
- Python 3
- Required Python libraries for the analysis scripts

Install the Python dependencies listed in the project's `requirements.txt`, if available.

## Running the Simulation

1. Install and configure NS-3.45.
2. Place `astar-multiclient.cc` in the NS-3.45 `scratch/` directory.
3. Open a terminal and navigate to the NS-3.45 root directory.
4. Run the simulation:

```bash
./ns3 run scratch/astar-multiclient
```

5. Review the console output and generated simulation result files.

The simulation uses FlowMonitor to collect network statistics and records routing changes and failure-recovery events.

## Performance Analysis

Navigate to the performance analysis directory:

```bash
cd priority_aware_routing/network/ns3_network_performance_analysis
```

Run the analysis script:

```bash
python3 performance_analysis.py \
  --repeat-xml-dir results/raw/astar_repeats \
  --repeat-log-dir results/processed/astar_repeats/run_logs \
  --repeat-output-dir results/processed/astar_repeats_verified \
  --repeat-graphs results/graphs/astar_repeats_verified
```

This command processes the existing simulation results and generates performance summaries and graphs. It does not execute new NS-3 simulations.

### Generated Outputs

- `per_run_metrics.csv` — Performance metrics for individual simulation runs.
- `per_flow_metrics.csv` — Performance measurements for individual traffic flows.
- `repeat_summary.csv` — Aggregated comparison of baseline and failure scenarios.
- `priority_summary.csv` — Performance analysis grouped by traffic priority.
- Graph files — Visual comparisons of network performance.

To obtain updated results, run the NS-3 simulation or repeat-run script first, then execute the analysis script.

## Link Failure and Recovery

The simulation introduces a link failure affecting the `Client1-RelayA` link at **5 seconds**, followed by a configured recovery event at **7 seconds**.

The experiment evaluates how the routing system responds to the link failure and records changes in network performance and routing behavior.

The recovery-time checker polls at 10-millisecond intervals and records the first subsequent packet reception. Therefore, a reported recovery time of `0.01 seconds` represents the detection resolution of the checker and should not be interpreted as an exact measurement of routing convergence.

## Performance Metrics

| Metric | Description |
|---|---|
| Throughput | Rate of successfully received application data |
| Packet Loss | Number or percentage of packets that fail to reach their destination |
| Packet Delivery Ratio (PDR) | Percentage of transmitted packets successfully received |
| End-to-End Delay | Average time taken for packets to reach their destination |
| Route Changes | Number of routing changes recorded during the simulation |
| Recovery Detection Time | Time until the checker detects a subsequent packet reception |

## Experimental Results

The project analyses six paired baseline and link-failure runs, using run IDs 0104–0109.

| Metric | Baseline | Link-Failure Scenario |
|---|---:|---:|
| Mean Throughput | 5.80860 Mbps | 5.80635 Mbps |
| Mean Packet Loss | 0.105233% | 0.143950% |
| Mean Packet Delivery Ratio | 99.894767% | 99.856050% |
| Mean End-to-End Delay | 0.399388 ms | 0.409073 ms |
| Mean Route Changes | 0 | 2 |
| Mean Recovery Detection Time | Not applicable | 0.01 seconds |

The results show that the simulated link failure causes a small change in aggregate network performance. The analysis also demonstrates the importance of examining route changes, packet delivery, and delay when evaluating routing behavior under changing network conditions.

These values apply to the tested simulation configuration and should not be treated as universal performance guarantees.

## Browser Demo

The `browser_demo/index.html` file provides a standalone browser-based visualization of the network topology, if included in the repository.

Open the HTML file in a web browser to view the demonstration. The browser demo is a visualization and does not execute or control the NS-3 simulation.

## Reproducibility

- The analysed repeat runs use seed `1` and run IDs `104` through `109`.
- Keep the simulation source, configuration, analysis scripts, input logs, and XML files together when sharing reproducible experiments.
- Regenerate the analysis outputs whenever new simulation results are produced.
- Record changes to topology, traffic configuration, routing parameters, and simulation settings.
- Exclude virtual environments, compiled binaries, build directories, cache files, and credentials from version control.

## Limitations

- Results depend on the selected topology, traffic patterns, wireless configuration, and simulation parameters.
- The reported recovery time reflects packet-reception detection at 10-millisecond polling intervals.
- The standalone browser visualization is separate from the actual NS-3 simulation.
- Additional topologies, traffic conditions, and repeated experiments would be required to establish broader conclusions about routing performance.

## Team Members

1. **Aarusha GP** — 1BM23CS005
2. **Abhinav C** — 1BM23CS008
3. **Abhinav Sanjay** — 1BM23CS009
4. **Anushree VK** — 1BM23CS046

## Academic Context

Alternate Assessment Tool (AAT) project for the Bachelor of Engineering degree in Computer Science and Engineering, Visvesvaraya Technological University, Belagavi, academic year 2026–2027.

## License

No license has been specified for this project. Add an appropriate license file if you intend to permit public reuse or redistribution.
