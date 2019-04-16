import string

import boto.route53
from django.conf import settings

from .models import Subdomain


R53 = boto.route53.connect_to_region(
    'universal', aws_access_key_id=settings.AWS['access_key'],
    aws_secret_access_key=settings.AWS['secret_key'])
ZONE = None
TTL = 90
NAME_FORMAT = '{0}.zzzz.io'
VALID_CHARS = string.ascii_letters + '_-' + string.digits


def get_zone():
    global ZONE
    if ZONE is None:
        ZONE = R53.get_zone("zzzz.io.")
    return ZONE


def valid_ip(ip, rec_type):
    return True if settings.RECORD_TYPES[rec_type]['regex'].match(ip) else False


def update_dns_record(subdomain, ip, rec_type):
    ZONE = get_zone()
    name = NAME_FORMAT.format(subdomain)
    old_record = ZONE.find_records(name, rec_type)
    if old_record:
        ZONE.update_record(old_record, ip, new_ttl=TTL)
    else:
        ZONE.add_record(rec_type, name, ip, ttl=TTL)


def update_if_necessary(subdomain_obj, ip, rec_type, force=False):
    if not force and ip == getattr(subdomain_obj, settings.RECORD_TYPES[rec_type]['field']):
        return {'msg': 'No change', 'status': 200}
    if not valid_ip(ip, rec_type):
        return {'msg': 'Invalid IP address. Have you specified the right type?',
                'status': 400}
    update_dns_record(subdomain_obj.name, ip, rec_type)
    setattr(subdomain_obj, settings.RECORD_TYPES[rec_type]['field'], ip)
    subdomain_obj.save()
    return {'msg': 'Updated', 'status': 200}


def delete_dns_records(subdomain):
    ZONE = get_zone()
    name = NAME_FORMAT.format(subdomain.lower())
    for rec_type in settings.RECORD_TYPES:
        record = ZONE.find_records(name, rec_type)
        if record:
            ZONE.delete_record(record)


def create_subdomain(user, subdomain, ip):
    if not subdomain:
        raise ValueError('Subdomain cannot be empty.')
    if subdomain.startswith('xn--'):
        raise ValueError('Unicode subdomains are blacklisted. Sorry!')
    if len(subdomain) >= 63:
        raise ValueError('Subdomain is too long.')
    for char in subdomain:
        if char not in VALID_CHARS:
            msg = 'The subdomain can only consist of the following characters: {0}'
            raise ValueError(msg.format(VALID_CHARS))
    if subdomain.startswith('-') or subdomain.endswith('-'):
        msg = 'The subdomain may not begin or end with a hyphen ("-")'
        raise ValueError(msg)

    subdomain_objs = Subdomain.objects.filter(name=subdomain)
    if (subdomain.lower() in settings.RESERVED_SUBDOMAINS
            or '_domainkey' in subdomain
            or subdomain_objs
            or subdomain.lower().startswith('www')):
        raise ValueError('This subdomain is unfortunately already in use.')

    domain_limit = settings.USER_CLASSES[user.user_class]['domain_limit']
    if domain_limit and len(Subdomain.objects.filter(user=user)) >= domain_limit:
        msg = ('You may not create another subdomain.'
               ' To prevent abuse of the service, your user class entitles you'
               ' to {0} subdomain{1}. To increase your user class, please consider donating.')
        raise ValueError(msg.format(domain_limit, 's' if domain_limit > 1 else ''))
    subdomain_obj = Subdomain(user=user, name=subdomain, ip=ip)
    subdomain_obj.save()
    if ip is not None:
        update_dns_record(subdomain, ip, 'A')
    return subdomain_obj
