# APB (Advanced Peripheral Bus) Protocol

## Overview

The **Advanced Peripheral Bus (APB)** is part of the ARM AMBA (Advanced Microcontroller Bus Architecture) specification. It is a simple, low-power, memory-mapped bus designed for connecting low-bandwidth peripherals to a system-on-chip (SoC).

Unlike AXI or AHB, APB is optimized for simplicity rather than throughput, making it one of the easiest protocols to verify and one of the most common buses used for peripheral devices.

---

# Why APB Exists

Modern SoCs contain two categories of hardware:

- High-performance components
- Low-speed peripherals

High-performance components include:

- CPUs
- DMA engines
- GPUs
- Memory controllers

These typically communicate using AXI or AHB.

Low-speed peripherals include:

- UART
- SPI
- I²C
- GPIO
- Timers
- Watchdog timers
- Small RAM blocks

Using AXI for every peripheral would unnecessarily increase hardware complexity and power consumption.

Instead, an AXI-to-APB bridge converts high-speed AXI transactions into simple APB accesses.

---

# Typical APB System

```text
                CPU
                 │
          AXI / AHB Bus
                 │
        AXI-to-APB Bridge
                 │
        ------------------
        |    APB Bus     |
        ------------------
        │   │   │    │
      UART GPIO TIMER RAM
```

---

# APB Characteristics

- Non-pipelined
- Single outstanding transaction
- Memory mapped
- Low power
- Simple timing
- Easy verification

---

# APB Signals

| Signal | Direction | Description |
|---------|-----------|-------------|
| PCLK | Input | APB Clock |
| PRESETn | Input | Active-low reset |
| PSEL | Input | Slave select |
| PENABLE | Input | Access phase indicator |
| PWRITE | Input | Read/Write control |
| PADDR | Input | Address |
| PWDATA | Input | Write data |
| PRDATA | Output | Read data |
| PREADY | Output | Transfer complete |
| PSLVERR | Output | Error indication |

---

# APB Transfer

Every APB transfer consists of two phases.

## 1. SETUP Phase

The master drives:

- Address
- Read/Write
- Write data (if writing)
- PSEL = 1

PENABLE remains LOW.

---

## 2. ACCESS Phase

The master asserts:

```
PENABLE = 1
```

The slave completes the transfer by asserting:

```
PREADY = 1
```

The transaction finishes on that clock edge.

---

# APB State Diagram

```text
IDLE
 │
 ▼
SETUP
 │
 ▼
ACCESS
 │
 ├── PREADY = 0
 │      │
 │      ▼
 │   ACCESS
 │
 └── PREADY = 1
        │
        ▼
      IDLE
```

---

# Write Transaction

1. Master asserts PSEL
2. Address is valid
3. PWRITE = 1
4. PWDATA contains write data
5. PENABLE asserted
6. Slave writes memory
7. PREADY asserted
8. Transaction completes

---

# Read Transaction

1. Master asserts PSEL
2. Address valid
3. PWRITE = 0
4. PENABLE asserted
5. Slave places data on PRDATA
6. PREADY asserted
7. Master samples PRDATA

---

# Error Handling

APB slaves may report errors using PSLVERR.

Typical causes include:

- Illegal address
- Unsupported register
- Invalid operation

Important:

Even when PSLVERR is HIGH, the transaction still completes normally.

Software must explicitly check PSLVERR.

---

# Reset Behavior

PRESETn is asynchronous to APB transfers.

Reset immediately initializes:

- FSM state
- Output signals
- Internal memory (implementation dependent)

Reset may occur during:

- IDLE
- SETUP
- ACCESS

A correct APB slave must recover cleanly.

---

# APB RAM Used in This Project

This project verifies a simple APB RAM featuring:

- 32 × 32-bit memory
- APB slave interface
- FSM implementation
- Illegal address detection
- PSLVERR generation
- Directed verification
- Functional coverage

---

# References

- ARM AMBA APB Specification
- ARM AMBA Architecture