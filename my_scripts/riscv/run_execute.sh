#!/bin/bash
build/RISCV/gem5.opt -r --stdout=cool --debug-flags=ProtoExecuteStage ./configs/example/riscv/baremetal_l2_uart.py --exe=../benchmarks/output/dhry.riscv

