APB RAM Verification Project

SoC Bus Verification | APB | Verilator | Coverage | tmux

📌 Project Overview

This project implements and verifies an APB-based RAM peripheral using an open-source verification flow on Ubuntu (VMware).
The objective is to validate protocol correctness, data integrity, address boundary behavior, error handling, and reset behavior of an APB slave, while demonstrating a realistic SoC DV workflow with coverage, automation, and debugging.

The design under test (DUT) is a 32-entry APB RAM supporting read, write, reset, and slave error signaling (PSLVERR) for illegal accesses.

📘 Introduction to APB (Advanced Peripheral Bus)
What is APB?

APB (Advanced Peripheral Bus) is a low-complexity, low-power, memory-mapped bus protocol defined by ARM AMBA.
It is designed to connect low-bandwidth peripherals (such as UARTs, GPIOs, timers, and small RAMs) to high-performance system buses like AXI or AHB through a bridge.

APB emphasizes:

Simplicity

Deterministic timing

Ease of verification

Low power consumption

Why APB Is Important in SoC Design

Modern SoCs contain:

High-speed cores communicating over AXI/AHB

Large numbers of peripherals that only require simple register access

APB is critical because it:

Reduces peripheral design complexity

Minimizes verification effort

Provides predictable behavior

Scales well to hundreds of peripherals

As a result, APB is one of the most widely used buses in real SoCs.

Typical Usage of APB

APB is commonly used for:

UART, SPI, and I²C controllers

GPIO blocks

Timers and watchdogs

Interrupt controllers

Configuration and status registers

Small embedded RAMs (as implemented in this project)

APB is not intended for:

High-throughput data movement

Bursty or pipelined transfers

APB System Structure

APB is typically part of a hierarchical bus architecture:

CPU / DMA
    |
AXI / AHB (High-speed bus)
    |
AXI-to-APB Bridge
    |
-------------------------
|   APB Peripheral Bus  |
-------------------------
 |     |      |      |
UART  GPIO   TIMER   RAM


The bridge translates high-performance bus transactions into simple APB accesses.

APB Protocol Structure

APB is a non-pipelined, single-transaction bus using a two-phase handshake.

Phase	Description
IDLE	No active transfer
SETUP	Address and control signals asserted
ACCESS	Transfer completes when PREADY is asserted

Only one transaction is active at a time, simplifying verification.

Key APB Signals
Signal	Direction	Description
PCLK	Input	APB clock
PRESETn	Input	Active-low reset (out-of-band)
PSEL	Input	Peripheral select
PENABLE	Input	Indicates ACCESS phase
PADDR	Input	Address
PWRITE	Input	Read (0) / Write (1)
PWDATA	Input	Write data
PRDATA	Output	Read data
PREADY	Output	Transfer completion
PSLVERR	Output	Slave error indication
Error Handling (PSLVERR)

PSLVERR is asserted by the slave to indicate an error such as:

Illegal address access

Unsupported operation

Important behavior:

The transfer still completes (PREADY = 1)

The master must explicitly check PSLVERR

Reset Behavior (Out-of-Band Reset)

APB reset (PRESETn) is out-of-band, meaning:

It does not follow APB SETUP / ACCESS phases

It does not use PSEL, PENABLE, or PREADY

It immediately forces the peripheral into a known state

Reset can occur:

While the bus is idle

During SETUP

During ACCESS

This guarantees reliable recovery and clean initialization.

🎯 Verification Objectives

Verify correct APB handshake timing

Validate read/write data integrity

Detect and flag illegal address accesses

Confirm proper PSLVERR behavior

Ensure reset correctly initializes FSM and memory

Improve coverage through targeted test refinement

🏗️ Project Architecture
Design Under Test (DUT)

apb_ram.sv

32 × 32-bit memory

Valid address range: 0–31

Illegal address → PSLVERR = 1

FSM-based APB implementation

Active-low reset (presetn)

Verification Environment (UVM-Style)
Component	             Responsibility
Sequence	    Generates APB read/write/reset traffic
Driver	             Drives APB signals
Monitor	                Observes completed APB transfers
Scoreboard	      Reference memory model
Agent / Env / Test	Structural integration

The environment follows UVM methodology principles, adapted for an open-source simulation flow.

🧪 Test Scenarios
Directed Tests

Reset initialization

Single read/write

Boundary address access (0 and 31)

Illegal address detection

Random Tests

Random legal reads/writes

Back-to-back transfers

Bulk write followed by bulk read

Random illegal address injection

Reset Stress Tests

Reset during idle

Reset during active transfer

Post-reset recovery validation

📊 Coverage Strategy
Functional Coverage

Read vs write operations

Legal vs illegal address bins

PSLVERR asserted/deasserted

Reset occurrence

Sequential access patterns

Code Coverage

FSM state transitions

Error and non-error paths

Collected using Verilator coverage

Targeted testing improved functional coverage by ~30% compared to baseline random testing.

🖥️ Tools & Environment

OS: Ubuntu (VMware)

Simulator: Verilator

Waveform Viewer: GTKWave

Automation: Makefile + shell scripts

Terminal Workflow: tmux

Language: SystemVerilog

🪟 tmux Workflow

Typical tmux session layout:

Pane 1: Simulation run

Pane 2: Live log monitoring

Pane 3: Waveform debugging

Pane 4: Coverage generation

This mirrors real DV debugging workflows used in industry.

▶️ How to Run
git clone <repo-url>
cd apb-ram-verification

make run
gtkwave dump.vcd
make coverage


Artifacts:

dump.vcd – waveform

results/ – logs and coverage reports

🧩 What This Project Demonstrates

Strong understanding of APB protocol

Practical SoC peripheral verification

Debugging via waveforms and logs

Coverage-driven verification mindset

Open-source DV toolchain proficiency

👤 Author

Andrew Abdi
SoC / ASIC Design Verification
SystemVerilog • UVM • APB / AXI • Verilator • Cocotb
