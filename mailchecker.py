#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import sys
import DNS
import smtplib
import itertools

INVALID_MAILBOX_STATUS = [450, 550, 553]
VALID_MAILBOX_STATUS = [250, 251]

def get_mx_for_domain(domain):
    try:
        mx_list = DNS.mxlookup(domain)
        best_mx_ip = sorted(mx_list)[0][1]
    except:
        best_mx_ip = None

    return best_mx_ip

if __name__ == '__main__':
    DNS.DiscoverNameServers()

    queue = []

    for email in sys.stdin.readlines():
        email = email.rstrip('\n')
        if '@' not in email:
            print('{0} -> invalid'.format(email))
            continue

        user, domain = email.rsplit('@', 1)
        queue.append(
            (email, domain)
        )

    # sort queue by domain
    queue = sorted(queue, key=lambda x: x[1])

    # group the queue by domain
    for domain, email_iter in itertools.groupby(queue, lambda x: x[1]):
        mx = get_mx_for_domain(domain)

        if mx is None:
            for email, _ in email_iter:
                print('{0} -> invalid'.format(email))
            continue

        try:
            for email, _ in email_iter:
                smtp = smtplib.SMTP(mx, timeout=5)
                smtp.helo()
                smtp.docmd('MAIL FROM:<mailchecker@example.com>')
                status, msg = smtp.docmd('RCPT TO:<%s>' % email)
                if status in INVALID_MAILBOX_STATUS:
                    print('{0} -> invalid'.format(email))
                elif status in VALID_MAILBOX_STATUS:
                    print('{0} -> valid'.format(email))
                else:
                    print('{0} -> unknown ({1} {2})'.format(email, status, msg))
                smtp.quit()

        except smtplib.SMTPException as e:
            print('MX {0} error: {1}'.format(mx, str(e)))
            continue

