import asyncio
import time
from asyncio import Semaphore
from random import random
from typing import Iterable, List, Union

from aiohttp import ClientSession
from asgiref.sync import async_to_sync
from django.core.management import BaseCommand
from django.utils import timezone

from appel_crises.data import DISTRICT_TO_MP
from appel_crises.data.gvt import GVT
from appel_crises.mailer import (
    send_mail,
    mailing_person,
    get_aiohttp_session,
    MailingPerson,
    send_template,
)
from appel_crises.models import Signature, CallOutEmail
from appel_crises.settings import MAIN_EMAIL, APPMODE, SIGNATURE_TEMPLATE_ID

MAX_CONCURRENT_REQUESTS = 100
SendSignature = Union[Signature, type(None)]
SendCallOutEmail = Union[CallOutEmail, type(None)]


def get_gvt_address() -> MailingPerson:
    """Returns an address from the government, as specified in data.gvt ."""
    return random.choice(GVT)


def mailing_persons_from_circonscriptions(circo_numbers: str) -> List[MailingPerson]:
    """
    Fetch the list of mailing persons from stored data.

    :param circo_numbers: The circonscription numbers, comma separated,
                          for example: "93.1,75.3"
    :returns: A list of MailingPerson, as the mailer expects it as
              recipients of an email.
    """
    circoncriptions = circo_numbers.split(',')

    return [mailing_person_from_circonscription(number) for number in circoncriptions]


def mailing_person_from_circonscription(circo_number: str) -> MailingPerson:
    """
    Match a circonscription number with the associated mp data,
    formatted as the mailer expects it.
    """
    mp = DISTRICT_TO_MP[circo_number]

    if APPMODE != 'prod':
        mailto = "hadrien.renaudlebret@gmail.com"
    else:
        mailto = mp[3]

    return mailing_person(mailto, mp[0])


class Command(BaseCommand):
    help = "Send emails for all Signature for which it hasn't been done before."

    def handle(self, *args, **options):
        self.send_to_signatures()
        self.send_call_out_emails()

    def send_to_signatures(self):
        """Do the job."""
        start = time.time()

        # Because @async_to_sync doesn't update types
        # noinspection PyTypeChecker
        modified: List[Signature] = self.async_sent_to_signatures(
            list(Signature.get_unsent())
        )

        Signature.objects.bulk_update(modified, ("email_sent_at",))

        stop = time.time()
        self.stdout.write(
            f"Successfully sent {len(modified)} signatures emails "
            f"in {stop - start:.2}s."
        )

    @async_to_sync
    async def async_sent_to_signatures(
        self, signatures: Iterable[Signature]
    ) -> List[Signature]:
        """Send the mail to the signatures in an async way."""
        sem = Semaphore(MAX_CONCURRENT_REQUESTS)

        async with get_aiohttp_session() as session:
            results: List[SendSignature] = await asyncio.gather(
                *(
                    self.send_one_mail_to_a_signature(session, s, sem)
                    for s in signatures
                )
            )

        return [s for s in results if s is not None]

    async def send_one_mail_to_a_signature(
        self, session: ClientSession, signature: Signature, sem: Semaphore
    ) -> SendSignature:
        """
        Send an email to the corresponding signature.

        :param session: The client with which to send the email
        :param signature: the recipient of the email
        :param sem: A semaphore object to limit the number of concurrent requests
        :return: the signature, is sending was successful
        """
        name = signature.first_name + " " + signature.surname

        async with sem:
            sending_result = await send_template(
                session=session,
                to=(mailing_person(signature.email, name),),
                template_id=SIGNATURE_TEMPLATE_ID,
            )

        if sending_result:
            signature.email_sent_at = timezone.now()
            return signature

        else:
            self.stderr.write(f"Sending mail to {signature} failed.")
            return None

    def send_call_out_emails(self):
        """Send the pending emails in CallOutEmail table."""
        start = time.time()

        # noinspection PyTypeChecker
        modified: List[CallOutEmail] = self.async_call_out_emails(
            list(CallOutEmail.get_unsent())
        )

        CallOutEmail.objects.bulk_update(modified, ("email_sent_at",))

        stop = time.time()
        self.stdout.write(
            f"Successfully sent {len(modified)} call out emails in {stop - start:.2}s."
        )

    @async_to_sync
    async def async_call_out_emails(
        self, emails: List[CallOutEmail]
    ) -> List[CallOutEmail]:
        """Send the emails in an async way."""
        sem = Semaphore(MAX_CONCURRENT_REQUESTS)

        async with get_aiohttp_session() as session:
            result = await asyncio.gather(
                *(self.send_one_call_out_email(session, e, sem) for e in emails)
            )

        return [r for r in result if r is not None]

    async def send_one_call_out_email(
        self, session: ClientSession, email: CallOutEmail, sem: Semaphore
    ) -> SendCallOutEmail:
        """Send one call out email."""
        sender = mailing_person(MAIN_EMAIL, email.sender)
        to = mailing_persons_from_circonscriptions(email.circonscription_numbers)
        if email.send_to_government:
            to.append(get_gvt_address())
        cc = (mailing_person(email.from_email, email.sender),)

        async with sem:
            sending_result = await send_mail(
                session,
                sender=sender,
                to=to,
                subject=email.subject,
                text=email.content,
                cc=cc,
            )

        if sending_result:
            email.email_sent_at = timezone.now()
            return email

        else:
            self.stderr.write(f"Sending mail to {email} failed.")
            return None
