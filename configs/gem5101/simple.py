// In this file, we create system consists of a CPU and a Memory
// Memory are managed by Memory controller, which is mainly responsible for CPU Mem access
// CPU and Memory connect through a membus, all ports of CPU and Memory are connected to the membus.
import m5
//import all the existing m5 objects
from m5.objects import *

// First, create the my own system object use m5-System object
system = System()

// System property: config the system clock domain including clock-frequency and voltage-domain
system.clock_domain = SrcClockDomain()
system.clock_domain.clock = '1GHz'
system.clock_domain.voltage_domain = VoltageDomain()

// Next, set the memory property before adding memory object to the system
system.mem_mode = 'Timing'
// Address Ranges
system.mem_ranges = [AddrRange('512MB')]

// Create CPU
system.cpu = 'TimingSimpleCPU'

// Create Membus
system.membus = SystemXBar()

// Connect CPU port to membus
system.cpu.icache_port = system.membus.slave()
system.cpu.dcache_port = system.membus.slave()

// Some extra InterruptController ports needed to connect for X86-ISA
system.cpu.createInterruptController()
system.cpu.interrupt[0].pio = system.membus.master
system.cpu.interrupt[0].int_master = system.membus.slave
system.cpu.interrupt[0].int_slave = system.membus.master

system.system_port = system.membus.slave

// Create Memory Controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

// Finally, after constructing the whole system, we can assign a binary for the system to process

// Create Proccess
process = Process()
process.cmd = ['test/test-progs/hello/bin/x86/linux/hello']

// load the process to the system
system.load = process
system.cpu.createThreads()

// every system should pass to the root object
root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}' .format(m5.curTick(), exit_event.getCause()))
