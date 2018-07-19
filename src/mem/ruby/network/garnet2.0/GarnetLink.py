# Copyright (c) 2008 Princeton University
# Copyright (c) 2009 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import *
from m5.proxy import *
from m5.objects.ClockedObject import ClockedObject
from m5.objects.BasicLink import BasicIntLink, BasicExtLink

class NetworkLink(ClockedObject):
    type = 'NetworkLink'
    cxx_header = "mem/ruby/network/garnet2.0/NetworkLink.hh"
    link_id = Param.Int(Parent.link_id, "link id")
    link_latency = Param.Cycles(Parent.latency, "link latency")
    vcs_per_vnet = Param.Int(Parent.vcs_per_vnet,
                              "virtual channels per virtual network")
    virt_nets = Param.Int(Parent.number_of_virtual_networks,
                          "number of virtual networks")
    supported_vnets = VectorParam.Int(Parent.supported_vnets,
                                      "Vnets supported")
    width = Param.UInt32(Parent.width, "bit-width of the link")

class CreditLink(NetworkLink):
    type = 'CreditLink'
    cxx_header = "mem/ruby/network/garnet2.0/CreditLink.hh"

class NetworkBridge(CreditLink):
    type = 'NetworkBridge'
    cxx_header = "mem/ruby/network/garnet2.0/NetworkBridge.hh"
    link = Param.NetworkLink("Associated Network Link")
    vtype = Param.Int(2, "Direction of CDC 0:LINK->OBJECT, 1:OBJECT->LINK")
    serdes_latency = Param.Cycles(1, "Latency of SerDes Unit")
    cdc_latency = Param.Cycles(1, "Latency of CDC Unit")

# Interior fixed pipeline links between routers
class GarnetIntLink(BasicIntLink):
    type = 'GarnetIntLink'
    cxx_header = "mem/ruby/network/garnet2.0/GarnetLink.hh"
    # The internal link includes one forward link (for flit)
    # and one backward flow-control link (for credit)
    network_link = Param.NetworkLink(NetworkLink(), "forward link")
    credit_link  = Param.CreditLink(CreditLink(), "backward flow-control link")

    src_cdc = Param.Bool(False, "Enable CDC")
    dst_cdc = Param.Bool(False, "Enable CDC")

    src_net_bridge = Param.NetworkBridge("Network CDC at source")
    dst_net_bridge = Param.NetworkBridge("Network CDC at dest")
    src_cred_bridge = Param.NetworkBridge("Credit CDC at source")
    dst_cred_bridge = Param.NetworkBridge("Credit CDC at dest")

    src_serdes = Param.Bool(False, "Enable CDC")
    dst_serdes = Param.Bool(False, "Enable CDC")

    width = Param.UInt32(Parent.ni_flit_size,
                          "bit width supported by the router")

# Exterior fixed pipeline links between a router and a controller
class GarnetExtLink(BasicExtLink):
    type = 'GarnetExtLink'
    cxx_header = "mem/ruby/network/garnet2.0/GarnetLink.hh"
    # The external link is bi-directional.
    # It includes two forward links (for flits)
    # and two backward flow-control links (for credits),
    # one per direction
    _nls = []
    # In uni-directional link
    _nls.append(NetworkLink());
    # Out uni-directional link
    _nls.append(NetworkLink());
    network_links = VectorParam.NetworkLink(_nls, "forward links")

    _cls = []
    # In uni-directional link
    _cls.append(CreditLink());
    # Out uni-directional link
    _cls.append(CreditLink());
    credit_links = VectorParam.CreditLink(_cls, "backward flow-control links")

    ext_cdc = Param.Bool(False, "Enable CDC")
    int_cdc = Param.Bool(False, "Enable CDC")

    ext_net_bridge = VectorParam.NetworkBridge("CDC to reach the consumers")
    ext_cred_bridge = VectorParam.NetworkBridge("CDC to reach the consumers")
    int_net_bridge = VectorParam.NetworkBridge("CDC to reach the consumers")
    int_cred_bridge = VectorParam.NetworkBridge("CDC to reach the consumers")

    ext_serdes = Param.Bool(False, "Enable CDC")
    int_serdes = Param.Bool(False, "Enable CDC")

    width = Param.UInt32(Parent.ni_flit_size,
                          "bit width supported by the router")
