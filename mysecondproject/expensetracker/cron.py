# # from django_cron import CronJobBase, Schedule
# import logging

# logger = logging.getLogger(__name__)

# class MyFirstCronJob(CronJobBase):
#     RUN_EVERY_MINS = 1
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = "a_unique_code"

#     def do(self):
#         logger.info("doing the crone job")
#         print("hello from MyFirstCronJob")