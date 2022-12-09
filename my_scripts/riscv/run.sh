#!/bin/bash
build/RISCV/gem5.opt -r --stdout=cool --debug-flags=ProtoFetchStage,ProtoDecodeStage,ProtoExecuteStage,ProtoMemaccStage,ProtoWritebackStage ./configs/example/riscv/baremetal_l2_uart.py --exe=../benchmarks/output/hello.riscv

