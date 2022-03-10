
import cmd
import configparser
import pathlib
import argparse

from . import scheduler
from . import email_sender


class Cli(cmd.Cmd):
    intro = 'Python task scheduler. Type help or ? to list commands'
    prompt = 'schedulr: '

    def __init__(self, sched):
        cmd.Cmd.__init__(self)
        self.sched = sched

    def do_add(self, arg):
        """Add new job. Format: add <interval in seconds> <commandline>"""
        secs, cmd = arg.split(' ', maxsplit=1)
        secs = int(secs)
        try:
            self.sched.add_job(cmd, secs)
            print(f'Added job with command "{cmd}"')
        except ValueError as e:
            print('Could not create job: ', e)


    def do_cron(self, arg):
        """Add new cron job. Format: cron <crontab format: * * * * *> <commandline> """
        *r, cmd = arg.split(' ', maxsplit=5)
        crontab = ' '.join(r)
        try:
            self.sched.add_cron_job(cmd, crontab)
            print(f'Added job with command "{cmd}" and crontab {crontab}')
        except ValueError as e:
            print('Could not create job: ', e)
        

    def do_log(self, arg):
        """ Show executed jobs. Format: log <max number of entries> """
        if not arg: arg = '10'
        n = int(arg)
        reports = self.sched.get_recent_jobs(n)
        print(f'Showing last {len(reports)} reports' )
        for r in reports:
            ret = r.ret
            #if(ret[-1]=='\n'): ret = ret[:-1]
            print( f'{r.start:%x %X} -- {r.end:%x %X}  "{r.cmd}"  {"" if r.ex is None else r.ex}\n{ret}')

    def do_backlog(self, arg):
        """Show jobs to be executed. Format: backlog <max number of entries>"""
        
        if not arg: arg = '10'
        n = int(arg)
        jobs = self.sched.get_future_jobs(n)
        print(f'Showing upcoming {n} jobs' )
        for j in jobs:
            print( f'{ j.start:%x %X} "{j.cmd}"' )

    def do_q(self, arg):
        """Quit"""
        return True

    def do_EOF(self, arg):
        return True

    def emptyline(self):
        pass

def main():
    parser = argparse.ArgumentParser(description='Python task scheduler')
    parser.add_argument('--cfg', type=str, help='config file location')
    args = vars( parser.parse_args() )

    cfg = configparser.ConfigParser()
    cfg['email'] = {}
    if args['cfg'] is not None:
        print(f'Using config file {args["cfg"]}')
        with open(args['cfg'], 'r') as f:
            cfg.read(f)
    else:
        cfg.read('config.cfg')

    emailer = email_sender.Emailer(cfg['email'])

    sched = scheduler.Scheduler()
    #sched.add_job('ver', 5)
    sched.add_listener(emailer)
    Cli(sched).cmdloop()
    sched.stop()

if __name__ == '__main__':
    main()