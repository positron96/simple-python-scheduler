import subprocess as sp
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import queue
import traceback as tb
import email_sender
from report import Report

from attrs import define

@define
class BacklogEntry:
    cmd: str
    start: datetime

class Scheduler:

    def __init__(self):
        self.reports = []
        self.backend = BackgroundScheduler()#jobstores=jobstores)
        self.backend.start()
        self.listeners = []

    def add_listener(self, listr):
        self.listeners.append(listr)

    def run_job(self, cmd):
        ret = ''
        ex = None
        start = datetime.now()
        try:
            ret = sp.check_output(cmd, shell=True)
            ret = ret.decode('utf-8')
        except sp.CalledProcessError as e:
            ex = e
        end = datetime.now()
        r = Report(cmd, ret, start, end, ex)
        self.reports.append( r )

        try:
            for l in self.listeners:
                l.send(r)
        except Exception as e:
            tb.print_exc()
            # fail fast
            self.backend.stop()
            exit(1)

    def add_job(self, cmd, sched=30):
        trg = IntervalTrigger(seconds=sched)
        self.backend.add_job(self.run_job, trigger=trg, name=cmd, args=(cmd,) )

    def get_recent_jobs(self, n:int) -> list:
        reports = self.reports
        n = min(n, len(reports))
        return reports[-n:]

    def get_future_jobs(self, n:int) -> list[BacklogEntry]:
        jobs = self.backend.get_jobs()
        qq = queue.PriorityQueue()
        ret = []
        for j in jobs:
            qq.put( (j.next_run_time, j) )
        for i in range(n):
            next_time, j = qq.get()
            qq.put( (j.trigger.get_next_fire_time( next_time, next_time), j) )
            ret.append( BacklogEntry(j.name, next_time) )
        return ret