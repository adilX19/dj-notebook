# from django.core.management import call_command

# from django_cron import CronJobBase, Schedule

# class MyCronJob(CronJobBase):
#     RUN_EVERY_MINS = 2 # every 2 minute

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'notes.MyCronJob'    # a unique code

#     def do(self):
#       try:
#         call_command('dbbackup')
#       except:
#         pass