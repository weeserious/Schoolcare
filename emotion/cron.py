from django_cron import CronJobBase, Schedule

class PerformPeriodicAnalysis(CronJobBase):
    RUN_EVERY_MINS = 1  
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'emotion.perform_periodic_analysis' 

    def do(self):
        
        from .tasks import perform_periodic_analysis
        perform_periodic_analysis()
