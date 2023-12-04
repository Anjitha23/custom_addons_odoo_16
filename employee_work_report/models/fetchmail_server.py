# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from email import message_from_bytes
from email.utils import parseaddr
import logging
_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    @api.model
    def _fetch_mails(self):
        """Override the fetch_mail function."""
        return self.search([('state', '=', 'done'),
                            ('server_type', '!=', 'local')]).fetch_mail()

    def extract_html_body(self, part):
        """
        Recursively extract HTML body from multipart message.
        """
        if part.is_multipart():
            html_body = ""
            for subpart in part.get_payload():
                html_body += self.extract_html_body(subpart)
            return html_body
        elif part.get_content_type() == 'text/html':
            return part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
        else:
            return ""

    def fetch_mail(self):
        additional_context = {
            'fetchmail_cron_running': True
        }
        MailThread = self.env['mail.thread']
        DailyWorkReport = self.env['daily.work.report']

        for server in self:
            _logger.info('Start checking for new emails on %s server %s',
                         server.server_type, server.name)
            additional_context['default_fetchmail_server_id'] = server.id
            count, failed = 0, 0
            imap_server = None
            connection_type = server._get_connection_type()

            if connection_type == 'imap':
                try:
                    imap_server = server.connect()
                    imap_server.select()
                    result, data = imap_server.search(None, '(UNSEEN)')
                    for num in data[0].split():
                        result, data = imap_server.fetch(num, '(RFC822)')
                        imap_server.store(num, '-FLAGS', '\\Seen')

                        try:
                            # Process the fetched email
                            msg = message_from_bytes(data[0][1])

                            sender_name, sender_email = parseaddr(msg.get('From', 'Unknown'))
                            subject = msg.get('Subject', 'No Subject')

                            # Extract HTML body from multipart message
                            email_body = self.extract_html_body(msg)
                            # Find the corresponding employee
                            employee = self.env['hr.employee'].search(
                                [('work_email', '=', sender_email)],
                                limit=1)

                            if employee:
                                # Create a new record in daily.work.report
                                DailyWorkReport.create({
                                    'name': f'Daily Work Report_{fields.Date.today().strftime("%d %b %Y")}_{employee.name}',
                                    'employee': employee.name,
                                    'email_body': email_body,
                                })
                            else:
                                _logger.warning(
                                    "No employee found for sender email: %s",
                                    sender_email)
                                failed += 1

                        except Exception:
                            _logger.exception(
                                'Failed to process mail from %s server %s.',
                                server.server_type, server.name)
                            failed += 1
                        imap_server.store(num, '+FLAGS', '\\Seen')
                        self._cr.commit()
                        count += 1
                    _logger.info(
                        "Fetched %d email(s) on %s server %s; %d succeeded, %d failed.",
                        count, server.server_type, server.name,
                        (count - failed), failed)
                except Exception:
                    _logger.exception(
                        "General failure when trying to fetch mail from %s server %s.",
                        server.server_type, server.name)
                finally:
                    if imap_server:
                        try:
                            imap_server.close()
                            imap_server.logout()
                        except OSError:
                            _logger.warning(
                                'Failed to properly finish imap connection: %s.',
                                server.name, exc_info=True)

        return True

    def _get_connection_type(self):
        """Return which connection must be used for this mail server (IMAP or POP).
        Can be overridden in sub-module to define which connection to use for a specific
        "server_type" (e.g., Gmail server).
        """
        self.ensure_one()
        return self.server_type
