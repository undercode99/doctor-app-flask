from flask_apscheduler import APScheduler
from app.services import PatientServices
scheduler = APScheduler()


""" job function """
def update_data_vaccine_patients():
    with scheduler.app.app_context():
        PatientServices.updateVaccineFromGoogleBigQuery()
    


""" init jobs """
def init_jobs(app):
    scheduler.init_app(app)
    scheduler.add_job(id = 'Update Google Big Query Patients', func=update_data_vaccine_patients, trigger='cron', hour='01', minute='00')
    scheduler.start()


