#!/usr/bin/env python
# coding: utf-8

import sys
import DNS
import smtplib
import itertools

INVALID_MAILBOX_STATUS = [450, 550, 553]
VALID_MAILBOX_STATUS = [250, 251]

def get_mx_for_domain(domain):
	mx_list = DNS.mxlookup(domain)
	return sorted(mx_list)[0][1]

if __name__ == '__main__':
	DNS.DiscoverNameServers()

	queue = []

	for email in sys.stdin.readlines():
		email = email.rstrip('\n')

		user, domain = email.rsplit('@', 1)

		mx = get_mx_for_domain(domain)
		queue.append(
			(email, domain)
		)

	# sort queue by domain
	queue = sorted(queue, key=lambda x: x[1])

	# group the queue by domain
	for domain, email_iter in itertools.groupby(queue, lambda x: x[1]):
		mx = get_mx_for_domain(domain)

		smtp = smtplib.SMTP(mx)
		smtp.ehlo_or_helo_if_needed()
		smtp.docmd('MAIL FROM:<mailchecker@example.com>')
		for email, _ in email_iter:
			status, msg = smtp.docmd('RCPT TO:<%s>' % email)
			if status in INVALID_MAILBOX_STATUS:
				print '%s -> invalid' % email
			elif status in VALID_MAILBOX_STATUS:
				print '%s -> valid' % email
			else:
				print '%s -> unknown (%s %s)' % (email, status, msg)

		smtp.quit()

