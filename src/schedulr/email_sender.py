
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
            'Start time: {1:%x %X}\n'
            'Finish time: {2:%x %X}\n'
            '{3}\n'
            '{4}' ).format( rep.cmd, rep.start, rep.end, 
                '' if rep.ex is None else str(rep.ex),
                rep.ret ) )

        msg['Subject'] = 'Execution result of "{}"'.format(rep.cmd)
        msg['From'] = self._cfg.get('from', 'sender@example.com')
        msg['To'] = self._cfg.get('to', 'target@example.com')

        s = smtplib.SMTP(self._cfg.get('server', 'localhost'), 
                port=self._cfg.getint('server_port', 1025) )
        user,psw = self._cfg.get('server_username',''), self._cfg.get('server_password', '')
        if user:
            s.login(user, psw)
        s.send_message(msg)
        s.quit()