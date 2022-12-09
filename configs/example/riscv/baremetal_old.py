#Author : Anuj J

from __future__ import print_function
from __future__ import absolute_import

import optparse
import sys

import m5
# from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath#, fatal, warn
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
# from common.Caches import *
from common import Options 

system = BareMetalRiscvSystem()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('2GB')]
system.membus = SystemXBar()

system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master
system.system_port = system.membus.slave

system.cpu = ProtoCPU()

system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

system.cpu.createInterruptController()

system.bootloader = '/home/ajx/gem5/Test_components/a.out'
# system.kernel = '/home/ajx/gem5/Test_components/a.out'

system.cpu.createThreads()

root = Root(full_system = True, system = system)


m5.instantiate()
print ('Begining to execute on what ?')
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
