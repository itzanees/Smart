from celery import shared_task
from datetime import datetime, timedelta
from .models import Doctor, Schedule

@shared_task(bind=True)
def create_schedules_task(self):
    today = datetime.today()
    six_months_later = today + timedelta(days=180)
    total_doctors = Doctor.objects.count()
    success_count = 0
    progress = 0

    for index, doctor in enumerate(Doctor.objects.all(), start=1):
        current_date = today
        while current_date <= six_months_later:
            start_time = datetime.combine(current_date, datetime.min.time()).replace(hour=9)  # 9:00 AM
            end_time = datetime.combine(current_date, datetime.min.time()).replace(hour=15)  # 3:00 PM

            while start_time < end_time:
                if not Schedule.objects.filter(doctor=doctor, date=current_date, start_time=start_time.time()).exists():
                    Schedule.objects.create(
                        doctor=doctor,
                        date=current_date,
                        start_time=start_time.time(),
                        duration=30  # 30 minutes per slot
                    )
                    success_count += 1
                start_time += timedelta(minutes=30)

            current_date += timedelta(days=1)

        # Update progress percentage
        progress = int((index / total_doctors) * 100)
        self.update_state(state='PROGRESS', meta={'current': progress, 'total': 100})

    return {'current': 100, 'total': 100, 'status': f"Successfully created {success_count} schedules."}
