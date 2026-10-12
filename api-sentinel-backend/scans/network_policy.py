from ipaddress import ip_address
from urllib.parse import urlparse
import socket
from django.conf import settings

ALLOWED_SCHEMES={'http','https'}

def validate_target_url(url):
    parsed=urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname:
        raise ValueError('Target URL must use http/https and include a hostname.')
    hostname=parsed.hostname
    # Local development can explicitly opt into loopback/private targets.
    if getattr(settings,'DEBUG',False) and hostname in {'localhost','127.0.0.1','::1'}:
        return parsed
    try:
        infos=socket.getaddrinfo(hostname, parsed.port or (443 if parsed.scheme=='https' else 80), type=socket.SOCK_STREAM)
        ips={info[4][0] for info in infos}
    except OSError as exc:
        raise ValueError(f'Could not resolve target host: {exc}') from exc
    for raw in ips:
        ip=ip_address(raw)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise ValueError('Target resolves to a non-public network address. Use a private scanning agent for internal targets.')
    return parsed
