"""Python module that manages the emails for the app.

It uses SendinBlue API as documented here : https://developers.sendinblue.com/reference

"""
import logging
from datetime import datetime
from typing import Dict, Iterable, Tuple, List

from aiohttp import ClientSession
from asgiref.sync import async_to_sync

from appel_crises.settings import SENDIN_BLUE_API_KEY, MAIN_EMAIL, MAIN_NAME

SB_SEND_MAIL_URL = "https://api.sendinblue.com/v3/smtp/email"
SB_FETCH_EVENTS_URL = "https://api.sendinblue.com/v3/smtp/statistics/events"

_logger = logging.getLogger(__name__)

MailingPerson = Dict[str, str]
DeliveryResult = Tuple[str, datetime]


def mailing_person(email: str, name: str = None) -> MailingPerson:
    """Build a MailingPerson dict."""
    if name is not None:
        return dict(name=name, email=email)
    else:
        return dict(email=email)


MAIN_PERSON = mailing_person(MAIN_EMAIL, MAIN_NAME)


def get_aiohttp_session() -> ClientSession:
    """Open session"""
    return ClientSession(headers={'api-key': SENDIN_BLUE_API_KEY})


async def send_mail(
    session: ClientSession,
    sender: MailingPerson,
    to: Iterable[MailingPerson],
    html_content: str,
    subject: str,
    text_content: str = "",
    bcc: Iterable[MailingPerson] = None,
    cc: Iterable[MailingPerson] = None,
) -> bool:
    """Uses SendinBlue API to send an email"""

    body = dict(
        sender=sender,
        to=to,
        htmlContent=html_content,
        textContent=text_content,
        subject=subject,
    )

    if bcc is not None:
        body['bcc'] = bcc

    if cc is not None:
        body['cc'] = cc

    async with session.post(SB_SEND_MAIL_URL, json=body) as resp:
        if resp.status == 201:
            return True
        else:
            _logger.error(
                "Invalid response %d on POST to send mail: %s",
                resp.status,
                await resp.text(),
            )
            return False


@async_to_sync
async def get_delivered_emails(offset: int, limit: int = 100) -> List[DeliveryResult]:
    """Fetch the delivered emails."""
    params = dict(offset=offset, limit=limit, event="delivered")

    async with get_aiohttp_session() as session:
        async with session.get(SB_FETCH_EVENTS_URL, params=params) as resp:
            data = await resp.json()

    if not data or 'events' not in data:
        return []

    result = [(e['email'], datetime.fromisoformat(e['date'])) for e in data['events']]

    return result
