import sib_api_v3_sdk
from celery import shared_task

from config import config
from services.authentication import get_name_from_email

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = config.SENDINBLUE_API_KEY

sendinblue_api_client = sib_api_v3_sdk.ApiClient(configuration)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def task_send_welcome_mail(self, name: str, email: str):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"name": name, "email": email}], template_id=5, params={"name": name})
    sib_api_v3_sdk.TransactionalEmailsApi(sendinblue_api_client).send_transac_email(send_smtp_email)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def verification_mail(self, email: str, token: str):
    name = get_name_from_email(email)
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"name": name, "email": email}],
        template_id=config.TEMPLATE_ID_OF_EMAIL_STRUCTURE_FOR_USER_EMAIL_VERIFICATION,
        params={"name": name, "verification_link": token},
    )
    sib_api_v3_sdk.TransactionalEmailsApi(sendinblue_api_client).send_transac_email(send_smtp_email)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def task_test(self, email: str):
    result = get_name_from_email(email)
    print(result)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def forgot_password_mail(self, email: str, token: str):
    name = get_name_from_email(email)
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"name": name, "email": email}],
        template_id=config.TEMPLATE_ID_OF_EMAIL_STRUCTURE_FOR_FORGOT_PASSWORD_EMAIL_VERIFICATION,
        params={"name": name, "reset_password_link": token},
    )
    sib_api_v3_sdk.TransactionalEmailsApi(sendinblue_api_client).send_transac_email(send_smtp_email)
