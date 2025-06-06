
import numpy as np
from matplotlib import pyplot as plt

import json
import os
from datetime import datetime

def simulate_lcfs1(lu, ld, mu, md, max_steps):
    packets = {}
    packets_index = 0
    packets_generated_controller = {}
    packets_arrived_controller = {}

    latest_packet = 0
    controller_packet = 0
    controller_sent_packet = 0
    actuator_packet = 0

    aol = []
    joint = []
    for t in range(max_steps):
        if np.random.rand() <= lu:
            packets_index += 1
            packets[packets_index] = t
            latest_packet = packets_index

        decision = np.random.choice([0,1,2], p = [mu, md, 1 - mu - md])
        if decision == 0:
            if latest_packet > 0:
                controller_packet = latest_packet

        if np.random.rand() <= ld:
            controller_sent_packet = controller_packet
            packets_generated_controller[controller_packet] = t

        if decision == 1:
            if controller_sent_packet > 0:
                actuator_packet = controller_sent_packet

        _aol = 0
        _ad = 0
        _au = 0
        if actuator_packet > 0:
            _aol = t - packets[actuator_packet]
            #if _aol == 0:
            #  print(t,actuator_packet,packets[actuator_packet],packets_generated_controller[actuator_packet])
            _ad = t - packets_generated_controller[actuator_packet]
            _au = _aol - _ad

            aol.append(_aol)
            joint.append((_au, _ad))

    return np.mean(aol), aol, joint

def analytical_lcfs1(lu, ld, mu, md):
    t1 = ld * (1/mu + 1/lu - 1)
    t2 = (1 - ld) * (1/mu - 1 + 1/lu - 1 + 1/ld)
    return 1/md - 1 + t1 + t2

def simulate_fcfs(lu, ld, mu, md, max_steps):
    packets = {}
    packets_index = 0
    packets_generated_controller = {}
    packets_arrived_controller = {}

    uplink_packets = []
    downlink_packets = []

    latest_packet = 0
    controller_packet = 0
    controller_sent_packet = 0
    actuator_packet = 0

    aol = []
    joint = []
    for t in range(max_steps):
        if np.random.rand() <= lu:
            packets_index += 1
            packets[packets_index] = t
            latest_packet = packets_index
            uplink_packets.append(latest_packet)

        decision = np.random.choice([0,1,2], p = [mu, md, 1 - mu - md])
        if decision == 0:
            if latest_packet > 0 and len(uplink_packets)!=0:
                controller_packet = uplink_packets[0]
                uplink_packets = uplink_packets[1:]

        if np.random.rand() <= ld:
            controller_sent_packet = controller_packet
            packets_generated_controller[controller_packet] = t
            downlink_packets.append(controller_packet)

        if decision == 1:
            if controller_sent_packet > 0 and len(downlink_packets)!=0:
                actuator_packet = downlink_packets[0]
                downlink_packets = downlink_packets[1:]

        _aol = 0
        _ad = 0
        _au = 0
        if actuator_packet > 0:
            _aol = t - packets[actuator_packet]
            #if _aol == 0:
            #  print(t,actuator_packet,packets[actuator_packet],packets_generated_controller[actuator_packet])
            _ad = t - packets_generated_controller[actuator_packet]
            _au = _aol - _ad

            aol.append(_aol)
            joint.append((_au, _ad))

    return np.mean(aol), aol, joint

def analytical_fcfs(lu, ld, mu, md):
    lub = 1 - lu
    ldb = 1 - ld
    mub = 1 - mu
    mdb = 1 - md
    tu = lub/(mu-lu)-lu*mub/(mu**2)+1/lu
    td = ldb/(md-ld)-ld*mdb/(md**2)+1/ld
    return tu + td - 4

def generate_data():
    lus = np.round(np.arange(0.05,1,0.05), 2)
    mus = [0.3,0.45]
    ld = 0.4
    md = 0.55
    aaol_data = {}

    max_steps = 100000
    aaol_data['lcfs1_sim'] = {}
    for mu in mus:
      aaol_data['lcfs1_sim'][mu] = {}
      for lu in lus:
        if lu >= mu:
          break
        s, a, j = simulate_lcfs1(lu, ld, mu, md, max_steps)
        print(mu,lu,s)
        aaol_data['lcfs1_sim'][mu][lu] = s

    aaol_data['lcfs1_ana'] = {}
    for mu in mus:
      aaol_data['lcfs1_ana'][mu] = {}
      for lu in lus:
        if lu >= mu:
          break
        aaol_data['lcfs1_ana'][mu][lu] = analytical_lcfs1(lu, ld, mu, md)
        print(mu,lu,aaol_data['lcfs1_ana'][mu][lu])

    aaol_data['fcfs_sim'] = {}
    for mu in mus:
      aaol_data['fcfs_sim'][mu] = {}
      for lu in lus:
        if lu >= mu:
          break
        s, a, j = simulate_fcfs(lu, ld, mu, md, max_steps)
        print(mu,lu,s)
        aaol_data['fcfs_sim'][mu][lu] = s

    aaol_data['fcfs_ana'] = {}
    for mu in mus:
      aaol_data['fcfs_ana'][mu] = {}
      for lu in lus:
        if lu >= mu:
          break
        aaol_data['fcfs_ana'][mu][lu] = analytical_fcfs(lu, ld, mu, md)
        print(mu,lu,aaol_data['fcfs_ana'][mu][lu])

    aaol_data['mu_d'] = md
    aaol_data['lambda_d'] = ld
    aaol_data['mu_u'] = 'lambda_u'

    file_name = 'sim/sim12_aaoi_data_sim_ana_lcfs_fcfs.json'
    with open(file_name, 'w') as file:
      json.dump(aaol_data, file, ensure_ascii=False)


generate_data()
