from fastapi import Depends
from .celery import celery_app
from datetime import datetime, timedelta
from app.api.v1.dependencies import get_notification_service, NotificationService, TemplateNotificationService, get_template_notification_service
from app.schemas.notification import NotificationUpdate
from app.utilities.notification_utils import send_email_notification, send_push_notification, send_sms_notification, send_whatsapp_notification
from datetime import datetime, time, timedelta
from apscheduler.triggers.cron import CronTrigger
from app.core.schedule import scheduler

@celery_app.task()
def update_notification_schedule_task(schedule, notification):
    job_id_pattern = f"notification_{schedule.notification_id}_day_"
    for job in scheduler.get_jobs():
        if job.id.startswith(job_id_pattern):
            scheduler.remove_job(job.id)

    schedule_notification(schedule, notification)

@celery_app.task()
def delete_notification_schedule_task(notification_id):
    job_id_pattern = f"notification_{notification_id}_day_"
    for job in scheduler.get_jobs():
        if job.id.startswith(job_id_pattern):
            scheduler.remove_job(job.id)

@celery_app.task(bind=True)
async def send_notification(self, notification_id: int):
    service_notification: NotificationService = Depends(get_notification_service)
    service_template_notification: TemplateNotificationService = Depends(get_template_notification_service)
    # Récupération de la notification à partir de la base de données
    notification = service_notification.get_notification_by_id(notification_id)
    
    try:
        notification = service_notification.get_notification_by_id(notification_id)
        if not notification:
            return

        # Récupérer les modèles de notification correspondant
        templates = service_template_notification.filter_internal_template_notifications({"channel_id": notification.channel_id})
        if not templates:
            return
        
        # Personnaliser le contenu de la notification avec les données de la base de données
        content = templates[0].body.format(**{
            'username': notification.user.username,  # Exemple d'utilisation des données utilisateur
            # Ajouter d'autres placeholders en fonction de vos besoins
        })

        if not notification or notification.status != "pending":
            return  # Si la notification n'existe pas ou est déjà traitée, on passe à la suivante.

        # Envoyer la notification via le canal approprié (fonction spécifique à chaque canal)
        # Logique d'envoi (email, push, sms, etc.)
        if notification.channel.code == 'sms':
            send_sms_notification(notification.user.country_code+notification.user.phone_number, content)
        elif notification.channel.code == 'email':
            send_email_notification()
        elif notification.channel.code == 'whatsapp':
            send_whatsapp_notification(notification.user.country_code+notification.user.phone_number, content)
        elif notification.channel.code == 'push':
            send_push_notification(notification.user_id, content)
        else:
            return

        # Mettre à jour le statut de la notification
        await service_notification.update_internal_notification(notification_id, NotificationUpdate(status= "sent", sent_at=datetime.utcnow()))

    except Exception as e:
        # Gestion des erreurs et des réessais
        max_retries = 10  # Limite du nombre de réessais
        retry_delay = 1  # Temps d'attente entre les réessais en minutes
        if not notification.retries+1 < max_retries:
            # Marquer la notification comme échouée après plusieurs tentatives
            await service_notification.update_internal_notification(notification.id, NotificationUpdate(status= "failed", error_message=str(e)))
        raise self.retry(exc=e, countdown=60 * retry_delay)  # Réessayer 


def schedule_notification(schedule, notification):
    now = datetime.utcnow()

    if notification.schedule_at and notification.schedule_at > now:
        scheduler.add_job(
            send_notification,
            'date',
            run_date=notification.schedule_at,
            args=[schedule.notification_id],
            id=f"notification_{schedule.notification_id}_one_time"
        )
        return

    if schedule.recursive:
        frequency = schedule.frequency or 1
        days_of_week = schedule.days_of_week or [0, 1, 2, 3, 4, 5, 6]
        time_of_day = schedule.time_of_day or time(9, 0)

        for day in days_of_week:
            trigger = CronTrigger(
                day_of_week=day, 
                hour=time_of_day.hour, 
                minute=time_of_day.minute,
                start_date=schedule.start_date or now,
                end_date=schedule.end_date
            )

            scheduler.add_job(
                send_notification,
                trigger,
                args=[schedule.notification_id],
                id=f"notification_{schedule.notification_id}_day_{day}"
            )
