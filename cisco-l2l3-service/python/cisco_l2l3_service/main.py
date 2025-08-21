"""
Cisco L2/L3 Service Implementation for NSO
Supports Cisco IOS and IOS XR devices
"""

import ncs
from ncs.application import Service
from ncs.dp import Action
import ncs.maapi as maapi
import ncs.maagic as maagic


class CiscoL2L3Service(Service):
    """
    Main service class for Cisco L2/L3 configuration
    """
    
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        """
        Service create callback
        """
        self.log.info(f'Service create(service={service._path})')
        
        # Get service parameters
        device_name = service.device
        device_type = service.device_type
        
        # Get device object
        device = root.devices.device[device_name]
        
        # Apply L2 configuration if present
        if service.l2_config:
            self._configure_l2(device, device_type, service.l2_config)
            
        # Apply L3 configuration if present
        if service.l3_config:
            self._configure_l3(device, device_type, service.l3_config)
    
    def _configure_l2(self, device, device_type, l2_config):
        """
        Configure Layer 2 settings
        """
        self.log.info(f'Configuring L2 for device: {device.name}')
        
        if device_type == 'ios':
            self._configure_l2_ios(device, l2_config)
        elif device_type == 'iosxr':
            self._configure_l2_iosxr(device, l2_config)
    
    def _configure_l3(self, device, device_type, l3_config):
        """
        Configure Layer 3 settings
        """
        self.log.info(f'Configuring L3 for device: {device.name}')
        
        if device_type == 'ios':
            self._configure_l3_ios(device, l3_config)
        elif device_type == 'iosxr':
            self._configure_l3_iosxr(device, l3_config)
    
    def _configure_l2_ios(self, device, l2_config):
        """
        Configure L2 for Cisco IOS devices
        """
        config = device.config.ios__vlan
        
        # Configure VLANs
        if l2_config.vlan:
            for vlan in l2_config.vlan:
                vlan_config = config.vlan_list.create(vlan.vlan_id)
                if vlan.name:
                    vlan_config.name = vlan.name
        
        # Configure interfaces
        if l2_config.interface:
            for intf in l2_config.interface:
                interface_config = device.config.ios__interface.GigabitEthernet.create(intf.name)
                
                if intf.description:
                    interface_config.description = intf.description
                
                if intf.switchport_mode:
                    interface_config.switchport.mode = intf.switchport_mode
                    
                    if intf.switchport_mode == 'access' and intf.access_vlan:
                        interface_config.switchport.access.vlan = intf.access_vlan
                    elif intf.switchport_mode == 'trunk' and intf.trunk_vlans:
                        interface_config.switchport.trunk.allowed.vlan = ','.join(map(str, intf.trunk_vlans))
    
    def _configure_l2_iosxr(self, device, l2_config):
        """
        Configure L2 for Cisco IOS XR devices
        """
        # IOS XR L2 configuration (bridge-domain, etc.)
        if l2_config.vlan:
            for vlan in l2_config.vlan:
                # Configure bridge-domain for IOS XR
                bd_config = device.config.cisco_ios_xr__l2vpn.bridge.group.create("default").bridge_domain.create(str(vlan.vlan_id))
                if vlan.name:
                    bd_config.description = vlan.name
        
        # Configure interfaces for IOS XR
        if l2_config.interface:
            for intf in l2_config.interface:
                interface_config = device.config.cisco_ios_xr__interface.GigabitEthernet.create(intf.name)
                
                if intf.description:
                    interface_config.description = intf.description
    
    def _configure_l3_ios(self, device, l3_config):
        """
        Configure L3 for Cisco IOS devices
        """
        # Configure L3 interfaces
        if l3_config.interface:
            for intf in l3_config.interface:
                interface_config = device.config.ios__interface.GigabitEthernet.create(intf.name)
                
                if intf.description:
                    interface_config.description = intf.description
                
                if intf.ip_address and intf.subnet_mask:
                    interface_config.ip.address.primary.address = intf.ip_address
                    interface_config.ip.address.primary.mask = intf.subnet_mask
                
                if intf.ipv6_address and intf.ipv6_prefix_length:
                    ipv6_addr = f"{intf.ipv6_address}/{intf.ipv6_prefix_length}"
                    interface_config.ipv6.address.prefix_list.create(ipv6_addr)
                
                if intf.shutdown:
                    interface_config.shutdown = None
                else:
                    if hasattr(interface_config, 'shutdown'):
                        del interface_config.shutdown
        
        # Configure routing
        if l3_config.routing:
            self._configure_routing_ios(device, l3_config.routing)
    
    def _configure_l3_iosxr(self, device, l3_config):
        """
        Configure L3 for Cisco IOS XR devices
        """
        # Configure L3 interfaces
        if l3_config.interface:
            for intf in l3_config.interface:
                interface_config = device.config.cisco_ios_xr__interface.GigabitEthernet.create(intf.name)
                
                if intf.description:
                    interface_config.description = intf.description
                
                if intf.ip_address and intf.subnet_mask:
                    # Convert subnet mask to prefix length for IOS XR
                    prefix_len = self._mask_to_prefix(intf.subnet_mask)
                    ipv4_addr = f"{intf.ip_address}/{prefix_len}"
                    interface_config.ipv4.address.create(ipv4_addr)
                
                if intf.ipv6_address and intf.ipv6_prefix_length:
                    ipv6_addr = f"{intf.ipv6_address}/{intf.ipv6_prefix_length}"
                    interface_config.ipv6.address.create(ipv6_addr)
                
                if intf.shutdown:
                    interface_config.shutdown = None
                else:
                    if hasattr(interface_config, 'shutdown'):
                        del interface_config.shutdown
        
        # Configure routing
        if l3_config.routing:
            self._configure_routing_iosxr(device, l3_config.routing)
    
    def _configure_routing_ios(self, device, routing):
        """
        Configure routing for Cisco IOS
        """
        # Static routes
        if routing.static_route:
            for route in routing.static_route:
                route_config = device.config.ios__ip.route.ip_route_forwarding_list.create(
                    route.destination, route.next_hop
                )
                if route.administrative_distance != 1:
                    route_config.distance = route.administrative_distance
        
        # IPv6 static routes
        if routing.static_ipv6_route:
            for route in routing.static_ipv6_route:
                route_config = device.config.ios__ipv6.route.ipv6_route_list.create(
                    route.destination, route.next_hop
                )
                if route.administrative_distance != 1:
                    route_config.distance = route.administrative_distance
        
        # OSPF configuration
        if routing.ospf:
            ospf_config = device.config.ios__router.ospf.create(routing.ospf.process_id)
            
            if routing.ospf.router_id:
                ospf_config.router_id = routing.ospf.router_id
            
            if routing.ospf.network:
                for network in routing.ospf.network:
                    net_config = ospf_config.network.create(network.network)
                    net_config.area = network.area
        
        # BGP configuration
        if routing.bgp:
            bgp_config = device.config.ios__router.bgp.create(routing.bgp.as_number)
            
            if routing.bgp.router_id:
                bgp_config.bgp.router_id = routing.bgp.router_id
            
            if routing.bgp.neighbor:
                for neighbor in routing.bgp.neighbor:
                    neighbor_config = bgp_config.neighbor.create(neighbor.ip_address)
                    neighbor_config.remote_as = neighbor.remote_as
                    if neighbor.description:
                        neighbor_config.description = neighbor.description
    
    def _configure_routing_iosxr(self, device, routing):
        """
        Configure routing for Cisco IOS XR
        """
        router_config = device.config.cisco_ios_xr__router
        
        # Static routes
        if routing.static_route:
            static_config = router_config.static
            for route in routing.static_route:
                route_config = static_config.address_family.ipv4.unicast.create(
                    route.destination
                ).next_hop.next_hop_address.create(route.next_hop)
                if route.administrative_distance != 1:
                    route_config.metric = route.administrative_distance
        
        # IPv6 static routes
        if routing.static_ipv6_route:
            static_config = router_config.static
            for route in routing.static_ipv6_route:
                route_config = static_config.address_family.ipv6.unicast.create(
                    route.destination
                ).next_hop.next_hop_address.create(route.next_hop)
                if route.administrative_distance != 1:
                    route_config.metric = route.administrative_distance
        
        # OSPF configuration
        if routing.ospf:
            ospf_config = router_config.ospf.create(routing.ospf.process_id)
            
            if routing.ospf.router_id:
                ospf_config.router_id = routing.ospf.router_id
            
            if routing.ospf.network:
                for network in routing.ospf.network:
                    area_config = ospf_config.area.create(network.area)
                    area_config.interface.create(network.network)
        
        # BGP configuration
        if routing.bgp:
            bgp_config = router_config.bgp.create(routing.bgp.as_number)
            
            if routing.bgp.router_id:
                bgp_config.bgp.router_id = routing.bgp.router_id
            
            if routing.bgp.neighbor:
                for neighbor in routing.bgp.neighbor:
                    neighbor_config = bgp_config.neighbor.create(neighbor.ip_address)
                    neighbor_config.remote_as = neighbor.remote_as
                    if neighbor.description:
                        neighbor_config.description = neighbor.description
    
    def _mask_to_prefix(self, mask):
        """
        Convert subnet mask to prefix length
        """
        mask_parts = mask.split('.')
        binary_str = ''
        for part in mask_parts:
            binary_str += bin(int(part))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))


class CiscoL2L3ServiceApplication(ncs.application.Application):
    """
    Application class for the Cisco L2/L3 Service
    """
    
    def setup(self):
        """
        Setup the application
        """
        self.log.info('CiscoL2L3ServiceApplication RUNNING')
        self.register_service('cisco-l2l3-servicepoint', CiscoL2L3Service)
    
    def teardown(self):
        """
        Teardown the application
        """
        self.log.info('CiscoL2L3ServiceApplication FINISHED')