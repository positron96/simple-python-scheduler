import subprocess as sp
import queue
import traceback as tb
import typing
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from attrs import define

from .report import Report

@define
class BacklogEntry:
    cmd: str
    start: datetime

class Scheduler:

    def __init__(self):
        self._reports = []
        self._backend = BackgroundScheduler()#jobstores=jobstores)
        self._backend.start()
        self._listeners = []

    def stop(self):
        self._backend.shutdown()

    def add_listener(self, listr):
        self._listeners.append(listr)

    def run_job(self, cmd):
        ret = ''
        ex = None
        start = datetime.now()
        try:
            proc = sp.run(cmd, shell=True, check=True, stdout=sp.PIPE, stderr=sp.PIPE)
            ret = proc.stdout.decode('utf-8')
        except sp.CalledProcessError as e:
            ret = e.stderr.decode('utf-8')
            ex = e
        end = datetime.now()
        r = Report(cmd, ret, start, end, ex)
        self._reports.append( r )

        try:
            for l in self._listeners:
                l.send(r)
        except Exception as e:
            #tb.print_exc()
            print(f'Notification failed with error {e}')
            # fail fast
            
            #self._backend.shutdown()
            #exit(1)

    def add_job(self, cmd, sched=30):
        trg = IntervalTrigger(seconds=sched)
        self._backend.add_job(self.run_job, trigger=trg, name=cmd, args=(cmd,) )

    def add_cron_job(self, cmd, crontab:str):
        trg = CronTrigger.from_crontab(crontab)
        self._backend.add_job(self.run_job, trigger=trg, name=cmd, args=(cmd,) )
        

    def get_recent_jobs(self, n:int) -> list:
        reports = self._reports
        n = min(n, len(reports))
        return reports[-n:]

    def get_future_jobs(self, n:int) -> typing.List[BacklogEntry]:
        jobs = self._backend.get_jobs()
        qq = queue.PriorityQueue()
        ret = []
        for j in jobs:
            qq.put( (j.next_run_time, j) )
        for i in range(n):
            next_time, j = qq.get()
            qq.put( (j.trigger.get_next_fire_time( next_time, next_time), j) )
            ret.append( BacklogEntry(j.name, next_time) )
        return ret