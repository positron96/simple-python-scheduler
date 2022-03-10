
import smtplib
from email.message import EmailMessage
from configparser import ConfigParser

from .report import Report


class Emailer:

    def __init__(self, config: ConfigParser):
        self._cfg = config

    def send(self, rep: Report):

        msg = EmailMessage()
        msg.set_content( ('Command: "{0}"\n'
            'Start time: {1:%a %b %d %H:%M:%S %Y}\n'
            'Finish time: {2:%a %b %d %H:%M:%S %Y}\n'
            'Output: {3}\n'
            '{4}').format( rep.cmd, rep.start, rep.end, rep.ret, '' if rep.ex is None else str(rep.ex) ) )

        msg['Subject'] = 'Execution result of "{}"'.format(rep.cmd)
        msg['From'] = self._cfg.get('from', 'sender@example.com')
        msg['To'] = self._cfg.get('to', 'target@example.com')

        s = smtplib.SMTP(self._cfg.get('server', 'localhost'), 
                port=self._cfg.getint('server_port',1025) )
        s.send_message(msg)
        s.quit()