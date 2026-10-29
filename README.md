Priority-Based Dynamic Routing in Multi-Client Multi-Server Networks
A network-routing simulation project developed using NS-3.45 to
study priority-aware path selection and routing behavior in a
multi-client, multi-server network, including link-failure and recovery
scenarios.
Overview
This project simulates a network containing clients, servers, and relay
nodes. It uses an A*-based path-search implementation with a cost
function that accounts for link distance, congestion, and client
priority. The simulation also evaluates network performance under normal
conditions and when a link failure is introduced.

The project is intended for academic demonstration and performance
analysis. Results are generated from NS-3 simulation runs rather than
from a live physical network.
Objectives
- Model a multi-client, multi-server network with relay nodes.
- Explore priority-aware path selection using A* search.
- Simulate a link failure and subsequent recovery.
- Measure throughput, packet loss, packet delivery ratio (PDR),
  end-to-end delay, route changes, and recovery detection time.
- Compare baseline and failure-scenario results using CSV summaries
  and graphs.
Technology Stack
- NS-3.45 --- network simulation
- C++ --- simulation and routing logic
- Python 3 --- result processing and performance analysis
- Pandas / NumPy / Matplotlib --- data analysis and visualization
  (depending on the analysis script)
- HTML, CSS, JavaScript --- standalone browser-based topology/demo
  visualization
Network Model
The simulation uses four clients, four servers, and eight relay nodes.
The relay nodes provide primary and alternate paths through the modeled
topology.

Client traffic priorities are configured in the C++ source. The
A*-based route search evaluates candidate paths using a cost that
includes link distance and congestion adjusted by priority. The
simulated Wi-Fi network uses the IEEE 802.11g standard, an ad-hoc MAC
configuration, and IPv4 addressing.
The browser demo is a standalone visualization. It does not execute or
control the NS-3 simulation itself.

Repository Structure
The project directory may contain the following main components:
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
The main NS-3 simulation source used during development is
scratch/astar-multiclient.cc in the NS-3 workspace. If this repository
is intended to be self-contained, keep a project copy of that source
file in the repository and update the run instructions to match its
actual location.
Requirements
- Linux or WSL with Ubuntu
- NS-3.45
- Python 3
- Python packages required by the analysis scripts
Check the imports in the analysis scripts for the exact Python
dependencies. If a requirements.txt is included, install from that
file.
Running the NS-3 Simulation
1. Install and build NS-3.45 following the official NS-3 installation
   instructions.
2. Place the simulation source file in the NS-3 scratch/ directory,
   for example:
   ns-3.45/scratch/astar-multiclient.cc
3. From the NS-3.45 root directory, run:
   ./ns3 run scratch/astar-multiclient
   If the project source uses a different target name or requires
   command-line arguments, use the command defined by that source file.
4. Check the simulation console output and generated result files. The
   simulation uses FlowMonitor to export flow statistics and reports
   route-change information.
Running Performance Analysis
The analysis scripts are located in:
priority_aware_routing/network/ns3_network_performance_analysis/
From that directory, run the repeat-analysis command used to process the
saved A* repeat XML and log files:
python3 performance_analysis.py \
  --repeat-xml-dir results/raw/astar_repeats \
  --repeat-log-dir results/processed/astar_repeats/run_logs \
  --repeat-output-dir results/processed/astar_repeats_verified \
  --repeat-graphs results/graphs/astar_repeats_verified
This command processes the existing repeat-run results and creates
per-run, per-flow, and summary CSV files along with performance graphs.
It does not launch new NS-3 simulations by itself; run the
simulation/repeat-run script first when fresh results are required.

Generated outputs include:
- per_run_metrics.csv --- metrics for each run and scenario
- per_flow_metrics.csv --- flow-level metrics
- repeat_summary.csv --- aggregated baseline/failure comparison
- priority_summary.csv --- results grouped by priority
- Graphs comparing network performance
Use the actual output paths printed by the scripts if they differ from
the paths above.
Failure and Recovery Scenario
The configured experiment introduces a link failure affecting the
Client1-RelayA link at simulation time 5 seconds, followed by a
recovery event at 7 seconds. Failure and recovery behavior is
recorded in the simulation logs.

The recovery-time checker polls at 10 ms intervals and records the first
subsequent packet reception. Therefore, a reported recovery time of
0.01 s represents the detection resolution of this polling mechanism;
it should not be interpreted as a precise measurement of the routing
protocol's full convergence time.
Metrics
  Metric                              Meaning
  Throughput                          Rate of successfully received
                                      application data

  Packet loss                         Number or percentage of transmitted
                                      packets not received

  Packet delivery ratio (PDR)         Percentage of transmitted packets
                                      successfully received

  End-to-end delay                    Average time taken for received
                                      packets to reach their destination

  Route changes                       Number of route changes recorded by
                                      the simulation

  Recovery detection time             Time until the configured checker
                                      detects a subsequent packet
                                  reception
Recorded Experimental Summary
The following values are the mean results from six paired repeat runs
(run IDs 0104--0109) available during the project analysis. Treat them
as results for this specific configuration, not as universal performance
guarantees.

  Metric                                 Baseline   Link-failure scenario
  Throughput                         5.80860 Mbps            5.80635 Mbps
  Packet loss                           0.105233%               0.143950%
  Packet delivery ratio                99.894767%              99.856050%
  Average end-to-end delay            0.399388 ms             0.409073 ms
  Mean route changes                            0                       2
  Mean recovery detection time     Not applicable                  0.01 s

In these runs, the failure scenario showed a small reduction in average
throughput and PDR, a small increase in average delay and packet loss,
and two recorded route changes. The 0.01-second recovery value is
limited by the 10 ms polling method described above.
Browser Demo
Open browser_demo/index.html in a web browser to view the standalone
topology/demo, if that file is present in the repository. The demo is
for visualization and should not be treated as a live simulation
dashboard unless it has explicitly been connected to simulation outputs.
Reproducibility Notes
- Keep the simulation source, configuration, analysis scripts, input
  logs, and XML files together when sharing a reproducible experiment.
- Record the NS-3 version, run IDs, seed, and scenario configuration
  when collecting new results.
- The available repeat runs use seed 1 and run IDs 104 through
  109.
- Rerun the analysis after generating new simulation outputs so the
  CSV summaries and graphs correspond to the latest data.
- Do not commit virtual environments, build directories, compiled
  binaries, cache folders, credentials, or .env files.
Limitations
- Results apply to the configured simulation topology, traffic,
  propagation model, and selected run parameters.
- The recovery time reported by the current checker is
  reception-detection time, not an exact measurement of routing
  convergence.
- A standalone browser visualization does not replace the NS-3
  simulation.
- Performance may vary when topology, traffic rates, radio settings,
  run number, or other simulation parameters change.
Authors
- Aarusha GP --- 1BM23CS005
- Abhinav C --- 1BM23CS008
- Abhinav Sanjay --- 1BM23CS009
- Anushree VK --- 1BM23CS046
Academic Context
Alternate Assessment Tool (AAT) project, Bachelor of Engineering in
Computer Science and Engineering, Visvesvaraya Technological University,
Belagavi, academic year 2026--2027.
License
No license has been specified. Add a license file if you intend to
publish or permit reuse of this project.
