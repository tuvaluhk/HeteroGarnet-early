#Author : Anuj J

from __future__ import print_function
from __future__ import absolute_import

import optparse
import sys

import m5
# from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath  #, fatal, warn
# from m5.util.fdthelper import *

addToPath('../../')

from ruby import Ruby

from common.FSConfig import *
# from common.SysPaths import *
# from common.Benchmarks import *
from common import Simulation
from common import CacheConfig
# from common import CpuConfig
# from common import MemConfig
# from common import ObjectList

from m5.objects import Cache

# from common.learning_gem5.part1.caches import *
from common import Options
from common import SimpleOpts

mem_range = [AddrRange(start='0x80000000',size='2GB')]

class L1Cache(Cache):
    """Simple L1 Cache with default values"""

    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    addr_ranges = mem_range

    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.slave

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
           This must be defined in a subclass"""
        raise NotImplementedError

class L1ICache(L1Cache):
    """Simple L1 instruction cache with default values"""

    # Set the default size
    size = '16kB'

    SimpleOpts.add_option('--l1i_size',
                          help="L1 instruction cache size. Default: %s" % size)

    def __init__(self, opts=None):
        super(L1ICache, self).__init__(opts)
        if not opts or not opts.l1i_size:
            return
        self.size = opts.l1i_size

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""

    # Set the default size
    size = '64kB'

    SimpleOpts.add_option('--l1d_size',
                          help="L1 data cache size. Default: %s" % size)

    def __init__(self, opts=None):
        super(L1DCache, self).__init__(opts)
        if not opts or not opts.l1d_size:
            return
        self.size = opts.l1d_size

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port

class L2Cache(Cache):
    """Simple L2 Cache with default values"""

    # Default parameters
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    addr_ranges = mem_range

    SimpleOpts.add_option('--l2_size',
                          help="L2 cache size. Default: %s" % size)

    def __init__(self, opts=None):
        super(L2Cache, self).__init__()
        if not opts or not opts.l2_size:
            return
        self.size = opts.l2_size

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave


mulSgs = 2
divSgs = 32
SimpleOpts.add_option('--mul_stages',
                      help="Number of multiplier stages. Default: %s" % mulSgs)
SimpleOpts.add_option('--div_stages',
                      help="Number of divider stages. Default: %s" % divSgs)
SimpleOpts.add_option('--exe',
                      help="Provide the elf to run on baremetal [--exe=?]")

(opts, args) = SimpleOpts.parse_args()

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = mem_range
system.membus = SystemXBar()

system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master
system.system_port = system.membus.slave

system.uart = ProtoUART(pio_addr=0x11300,pio_latency='200ns')
system.uart.pio = system.membus.master

process = Process()

if opts and opts.mul_stages:
    mulSgs = opts.mul_stages
if opts and opts.div_stages:
    divSgs = opts.div_stages

if opts and opts.exe:
    process.cmd = opts.exe
else:
    print("Please provide the executable binary path")
    exit(1)

# system.cpu = TimingSimpleCPU()
system.cpu = ProtoCPU(divStages = divSgs, mulStages = mulSgs)

# # To include L1 and L2 chaching support
# system.cpu.icache = L1ICache(opts)
# system.cpu.dcache = L1DCache(opts)
# system.cpu.icache.connectCPU(system.cpu)
# system.cpu.dcache.connectCPU(system.cpu)

# system.l2bus = L2XBar()
# # Hook the CPU ports up to the l2bus
# system.cpu.icache.connectBus(system.l2bus)
# system.cpu.dcache.connectBus(system.l2bus)

# # Create an L2 cache and connect it to the l2bus
# system.l2cache = L2Cache(opts)
# system.l2cache.connectCPUSideBus(system.l2bus)
# # Connect the L2 cache to the membus
# system.l2cache.connectMemSideBus(system.membus)

# Uncomment if wanna remove caching
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

system.cpu.createInterruptController()

system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system = False, system = system)

m5.instantiate()
print ('Begining to execute')
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
