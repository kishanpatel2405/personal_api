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
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"name": name, "email": email}], template_id=5,
                                                   params={"name": name})
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


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def send_credit_notification(
        self,
        first_name: str,
        last_name: str,
        company_name: str,
        company_email: str,
        subject: str,
        previous_credit: str,
        credit_change: str,
        new_credit: str,
        credit_type: str,
):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"name": f"{first_name} {last_name}", "email": company_email}],
        subject=subject,
        template_id=config.TEMPLATE_ID_OF_CREDIT_UPDATE_EMAIL_TEMPLATE,
        params={
            "first_name": first_name,
            "last_name": last_name,
            "company_name": company_name,
            "subject": subject,
            "previous_credit": previous_credit,
            "credit_change": credit_change,
            "new_credit": new_credit,
            "credit_type": credit_type,
        },
    )

    sib_api_v3_sdk.TransactionalEmailsApi(sendinblue_api_client).send_transac_email(send_smtp_email)
