# MLD

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-mld)](https://pypi.org/project/py-mld/)
[![PyPI](https://img.shields.io/pypi/v/py-mld)](https://pypi.org/project/py-mld/)
[![PyPI - License](https://img.shields.io/pypi/l/py-mld)](https://github.com/pedrofran12/py-mld/blob/master/LICENSE)

This repository stores the implementation of MLDv1 router-side state machines. This can be used to detect multicast interest of directly connected hosts.

The goal of this repository/module is to facilitate maintainability of this MLD implementation since its code is used by other Python projects/modules:

- [HPIM-DM](https://github.com/pedrofran12/hpim_dm)
- [PIM-DM](https://github.com/pedrofran12/pim_dm)


# Requirements

 - Linux machine
 - Python3 (we have written all code to be compatible with at least Python v3.3)
 - pip (to install all dependencies)


# Installation

  ```
  pip3 install py-mld
  ```

# How to use it?

```python
# import module
from mld import InterfaceMLD

intf = InterfaceMLD(interface_name="eth0")
intf.enable()  # start receiving MLD packets

# get information from a given multicast group
multicast_group_obj = intf.interface_state.get_group_state(group_ip="ff05::10:11:12")

interest = multicast_group_obj.has_members()  # boolean that informs if there is
                                              # multicast interest in this group
group_state = multicast_group_obj.state.print_state()  # get string identifying
                                                       # the state in which this
                                                       # group is at

# get notified of interest changes on this group
class MulticastGroupNotifier:
    def notify_membership(self, has_members):
        print(has_members)

notifier = MulticastGroupNotifier()
multicast_group_obj.add_multicast_routing_entry(notifier)

# when there is a change of multicast interest (for example group ff05::10:11:12
# gets interested receivers), the object associated to this object is notified
# through "notify_membership" method with has_members=True

# if you no longer want to monitor the interest of ff05::10:11:12, remove the
# notifier from the group
multicast_group_obj.remove_multicast_routing_entry(notifier)

intf.remove()  # stop receiving MLD packets
```
