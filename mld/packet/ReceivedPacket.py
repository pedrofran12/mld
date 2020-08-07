import socket
from .Packet import Packet
from .PacketMLDHeader import PacketMLDHeader
from .PacketIpHeader import PacketIpv6Header
from mld.utils import TYPE_CHECKING

if TYPE_CHECKING:
    from mld.Interface import Interface


class ReceivedPacket(Packet):
    # choose payload protocol class based on ip protocol number
    payload_protocol_v6 = {58: PacketMLDHeader}

    def __init__(self, raw_packet: bytes, ancdata: list, src_addr: str, next_header: int, interface: 'Interface'):
        self.interface = interface

        # Parse packet and fill Packet super class
        dst_addr = "::"
        for cmsg_level, cmsg_type, cmsg_data in ancdata:
            if cmsg_level == socket.IPPROTO_IPV6 and cmsg_type == socket.IPV6_PKTINFO:
                dst_addr = socket.inet_ntop(socket.AF_INET6, cmsg_data[:16])
                break

        src_addr = src_addr[0].split("%")[0]
        ipv6_packet = PacketIpv6Header(ver=6, hop_limit=1, next_header=next_header, ip_src=src_addr, ip_dst=dst_addr)
        payload = ReceivedPacket.payload_protocol_v6[next_header].parse_bytes(raw_packet)
        super().__init__(ip_header=ipv6_packet, payload=payload)
