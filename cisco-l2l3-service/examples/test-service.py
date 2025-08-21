#!/usr/bin/env python3
"""
Test script for Cisco L2/L3 Service Package
This script demonstrates how to create service instances programmatically
"""

import ncs
from ncs.maapi import Maapi
from ncs.maagic import get_root


def create_test_service():
    """
    Create a test service instance
    """
    with Maapi() as m:
        with ncs.maapi.single_write_trans(m, 'admin', 'system') as t:
            root = get_root(t)
            
            # Create service instance
            service = root.services.cisco_l2l3_service.create('test-service-1')
            service.device = 'R1'
            service.device_type = 'ios'
            
            # Configure L2
            l2_config = service.l2_config.create()
            
            # Add VLAN
            vlan = l2_config.vlan.create(100)
            vlan.name = 'Data VLAN'
            
            # Add L2 interface
            intf = l2_config.interface.create('GigabitEthernet0/1')
            intf.description = 'Access Port'
            intf.switchport_mode = 'access'
            intf.access_vlan = 100
            
            # Configure L3
            l3_config = service.l3_config.create()
            
            # Add L3 interface
            l3_intf = l3_config.interface.create('GigabitEthernet0/2')
            l3_intf.description = 'L3 Interface'
            l3_intf.ip_address = '192.168.1.1'
            l3_intf.subnet_mask = '255.255.255.0'
            
            # Add static route
            routing = l3_config.routing
            static_route = routing.static_route.create('10.0.0.0/24')
            static_route.next_hop = '192.168.1.254'
            
            # Add OSPF
            ospf = routing.ospf.create()
            ospf.process_id = 1
            ospf.router_id = '1.1.1.1'
            
            network = ospf.network.create('192.168.1.0/24')
            network.area = '0'
            
            print("Service instance 'test-service-1' created successfully")
            t.apply()


def create_iosxr_test_service():
    """
    Create a test service instance for IOS XR
    """
    with Maapi() as m:
        with ncs.maapi.single_write_trans(m, 'admin', 'system') as t:
            root = get_root(t)
            
            # Create service instance
            service = root.services.cisco_l2l3_service.create('test-service-xr')
            service.device = 'XR1'
            service.device_type = 'iosxr'
            
            # Configure L2
            l2_config = service.l2_config.create()
            
            # Add VLAN (Bridge Domain for XR)
            vlan = l2_config.vlan.create(200)
            vlan.name = 'XR Data VLAN'
            
            # Configure L3
            l3_config = service.l3_config.create()
            
            # Add L3 interface
            l3_intf = l3_config.interface.create('GigabitEthernet0/0/0/1')
            l3_intf.description = 'XR L3 Interface'
            l3_intf.ip_address = '10.1.1.1'
            l3_intf.subnet_mask = '255.255.255.0'
            l3_intf.ipv6_address = '2001:db8::1'
            l3_intf.ipv6_prefix_length = 64
            
            # Add static routes
            routing = l3_config.routing
            static_route = routing.static_route.create('172.16.0.0/16')
            static_route.next_hop = '10.1.1.254'
            
            ipv6_route = routing.static_ipv6_route.create('2001:db8:1::/48')
            ipv6_route.next_hop = '2001:db8::254'
            
            # Add BGP
            bgp = routing.bgp.create()
            bgp.as_number = 65001
            bgp.router_id = '10.1.1.1'
            
            neighbor = bgp.neighbor.create('10.1.1.2')
            neighbor.remote_as = 65002
            neighbor.description = 'Peer Router'
            
            print("Service instance 'test-service-xr' created successfully")
            t.apply()


if __name__ == '__main__':
    print("Creating test service instances...")
    
    try:
        create_test_service()
        create_iosxr_test_service()
        print("All test services created successfully!")
    except Exception as e:
        print(f"Error creating test services: {e}")