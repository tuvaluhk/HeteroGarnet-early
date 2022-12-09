// This file create Specific Cache for our two-cache.py
from m5.objects import Cache

class L1Cache(Cache):
    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def connectCPU(self, cpu):
        raise NotImplementedError
    def connectBus(self, bus):
        self.mem_side = bus.slave

class L1ICache(L1Cache):
    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

    size = '16kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size
    size = '64kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

class L2Cache(Cache):
    def __init__(self, options=None):
        super(L2Cache, self).__init__(options)
        if not options or not options.l2_size:
            return
        self.size = options.l2_size
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave
