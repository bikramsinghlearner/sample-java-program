# Cisco L2/L3 Service Package

This NSO service package provides Layer 2 and Layer 3 configuration capabilities for Cisco IOS and IOS XR devices.

## Features

### Layer 2 Configuration
- VLAN creation and management
- Interface switchport configuration (access/trunk modes)
- Bridge domain configuration for IOS XR

### Layer 3 Configuration
- Interface IP addressing (IPv4 and IPv6)
- Static routing (IPv4 and IPv6)
- OSPF configuration
- BGP configuration

## Supported Devices
- Cisco IOS devices
- Cisco IOS XR devices

## Installation

1. Copy the package to your NSO packages directory
2. Compile the package:
   ```bash
   cd cisco-l2l3-service/src
   make
   ```
3. Reload packages in NSO:
   ```bash
   ncs_cli -C -u admin
   packages reload
   ```

## Usage Example

```bash
# Create a service instance
configure
services cisco-l2l3-service example-service
device R1
device-type ios

# Configure L2
l2-config
vlan 100
name "Data VLAN"
exit
interface GigabitEthernet0/1
description "Access Port"
switchport-mode access
access-vlan 100
exit
exit

# Configure L3
l3-config
interface GigabitEthernet0/2
description "L3 Interface"
ip-address 192.168.1.1
subnet-mask 255.255.255.0
exit

routing
static-route 10.0.0.0/24
next-hop 192.168.1.254
exit
exit
exit

commit
```

## Package Structure

```
cisco-l2l3-service/
├── src/
│   └── yang/
│       └── cisco-l2l3-service.yang
├── python/
│   └── cisco_l2l3_service/
│       ├── __init__.py
│       └── main.py
├── templates/
│   ├── cisco-l2l3-service-ios-template.xml
│   └── cisco-l2l3-service-iosxr-template.xml
├── package-meta-data.xml
├── Makefile
└── README.md
```

## Dependencies

- cisco-ios-cli-6.77 (or compatible version)
- cisco-iosxr-cli-7.38 (or compatible version)
- NSO 5.7 or higher

## License

This package is provided as-is for educational and development purposes.