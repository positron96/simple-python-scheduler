
import cmd
import configparser

from . import scheduler
from . import email_sender


class Cli(cmd.Cmd):
    intro = 'Python scheduler. Type help or ? to list commands'
    prompt = 'scheduler: '

    def __init__(self, sched):
        cmd.Cmd.__init__(self)
        self.sched = sched

    def do_add(self, arg):
        """Add new job. Format: add <commandline> <interval in seconds> """
        cmd, secs = arg.rsplit(' ', maxsplit=1)
        secs = int(secs)
        self.sched.add_job(cmd, secs)

    def do_log(self, arg):
        """ Show executed jobs. Format: log <max number of entries> """
        if not arg: arg = '10'
        n = int(arg)
        reports = self.sched.get_recent_jobs(n)
        print('Showing last {} reports'.format(n) )
        for r in reports:
            print( '{0:%a %b %d %H:%M:%S %Y} -- {1:%a %b %d %H:%M:%S %Y}  "{2}"  {3}'.format( 
                r.start, 
                r.end, 
                r.cmd,
                r.ret if r.ex is None else r.ex )  )

    def do_backlog(self, arg):
        """Show jobs to be executed. Format: backlog <max number of entries>"""
        
        if not arg: arg = '10'
        n = int(arg)
        jobs = self.sched.get_future_jobs(n)
        print('Showing upcoming {} jobs'.format(n) )
        for j in jobs:
            print( '{0:%a %b %d %H:%M:%S %Y} "{1}"'.format( j.start, j.cmd ) )

    def do_q(self, arg):
        """Quit"""
        return True

    def emptyline(self):
        pass

def main():
    # jobstores = {
    #     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    # }
    cfg = configparser.ConfigParser()
    cfg.read('config.cfg')

    emailer = email_sender.Emailer(cfg['email'])

    sched = scheduler.Scheduler()
    #sched.add_job('ver', 5)
    sched.add_listener(emailer)
    Cli(sched).cmdloop()

if __name__ == '__main__':
    main()