import logging
from dns import resolver, reversename
from utils.settings import data, collect


def verify(item, dns_config):
    try:
        res = resolver.Resolver()
        ip = str(res.query(item[0])[0].address)
        hostname = str(res.query(
            reversename.from_address(item[1]), 'PTR'
        )[0].target)[:-1]
        if dns_config.get('hostnames').get(hostname) == ip:
            return True
        else:
            return False
    except:
        logging.exception("Ran into error trying to verify DNS addresses and hostnames")
        return False

@collect(data.get('services').get('dns').get('enabled'))
def DNS():
    dns_config = data.get('services').get('dns')

    hostname_ip_pairs = [(key, value) for key, value in
                         dns_config.get("hostnames").items()
                        ]
    result = [verify(pair, dns_config) for pair in hostname_ip_pairs]
    outcome = 1 if all(result) else 0

    return outcome
