# from app.api.v1.dependencies import get_notification_service, NotificationService, get_template_notification_service, TemplateNotificationService
# from app.schemas.notification import NotificationUpdate
# from datetime import datetime

# class NotificationServiceClass:
#     def __init__(self):
#         self.notification_service = get_notification_service()
#         self.template_service = get_template_notification_service()

#     def get_notification_by_id(self, notification_id):
#         return self.notification_service.get_notification_by_id(notification_id)

#     async def send_notification(self, notification_id):
#         # Récupération de la notification à partir de la base de données
#         notification = self.get_notification_by_id(notification_id)
        
#         try:
#             notification = self.get_notification_by_id(notification_id)
#             if not notification:
#                 return

#             # Récupérer les modèles de notification correspondant
#             templates = self.template_service.filter_internal_template_notifications({"channel_id": notification.channel_id})
#             if not templates:
#                 return
            
#             # Personnaliser le contenu de la notification avec les données de la base de données
#             content = templates[0].body.format(**{
#                 'username': notification.user.username,  # Exemple d'utilisation des données utilisateur
#                 # Ajouter d'autres placeholders en fonction de vos besoins
#             })

#             if not notification or notification.status != "pending":
#                 return  # Si la notification n'existe pas ou est déjà traitée, on passe à la suivante.

#             # Envoyer la notification via le canal approprié (fonction spécifique à chaque canal)
#             # Logique d'envoi (email, push, sms, etc.)
#             if notification.channel.code == 'sms':
#                 send_sms_notification(notification.user.country_code+notification.user.phone_number, content)
#             elif notification.channel.code == 'email':
#                 send_email_notification()
#             elif notification.channel.code == 'whatsapp':
#                 send_whatsapp_notification(notification.user.country_code+notification.user.phone_number, content)
#             elif notification.channel.code == 'push':
#                 send_push_notification(notification.user_id, content)
#             else:
#                 return

#             # Mettre à jour le statut de la notification
#             await self.notification_service.update_internal_notification(notification_id, NotificationUpdate(status= "sent", sent_at=datetime.utcnow()))

#         except Exception as e:
#             # Gestion des erreurs et des réessais
#             max_retries = 10  # Limite du nombre de réessais
#             retry_delay = 1  # Temps d'attente entre les réessais en minutes
#             if not notification.retries+1 < max_retries:
#                 # Marquer la notification comme échouée après plusieurs tentatives
#                 await self.notification_service.update_internal_notification(notification.id, NotificationUpdate(status= "failed", error_message=str(e)))
#             raise self.retry(exc=e, countdown=60 * retry_delay)  # Réessayer 

# send_notification_service = NotificationServiceClass()
