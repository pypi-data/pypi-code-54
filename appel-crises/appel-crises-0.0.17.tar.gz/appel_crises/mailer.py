"""Python module that manages the emails for the app.

It uses SendinBlue API as documented here : https://developers.sendinblue.com/reference

"""
import logging
import re
from datetime import datetime
from typing import Dict, Iterable, Tuple, List

from aiohttp import ClientSession
from asgiref.sync import async_to_sync

from appel_crises.settings import SENDIN_BLUE_API_KEY

SB_SEND_MAIL_URL = "https://api.sendinblue.com/v3/smtp/email"
SB_FETCH_EVENTS_URL = "https://api.sendinblue.com/v3/smtp/statistics/events"

_logger = logging.getLogger(__name__)

MailingPerson = Dict[str, str]
DeliveryResult = Tuple[str, datetime]


def format_text_for_email(text: str) -> str:
    """
    Format the text correctly so it can be pretty in mailers.

    For example:
    >>> text = chr(10).join("Hello,", "", "My name is Hadrien.", "Bye")
    >>> format_text_for_email(text)
    '<div>Hello,</div><div><br></div><div>My name is Hadrien.</div><div>Bye</div>'

    :param text: a string, as returned by the browser
    :return: a string, prettyfied with html tags
    """
    raw_lines = text.split("\n")
    beautified_lines = ""

    for i, line in enumerate(raw_lines):
        if re.fullmatch(r"\s*", line):
            if i == 0 or i == len(raw_lines) - 1:
                continue
            line = "<br>"
        line = "<div>" + line + "</div>"
        beautified_lines += line

    return beautified_lines


def mailing_person(email: str, name: str = None) -> MailingPerson:
    """Build a MailingPerson dict."""
    if name is not None:
        return dict(name=name, email=email)
    else:
        return dict(email=email)


def get_aiohttp_session() -> ClientSession:
    """Open session"""
    return ClientSession(headers={'api-key': SENDIN_BLUE_API_KEY})


async def send(session: ClientSession, body: Dict) -> bool:
    """Send an email with params in body."""
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


async def send_mail(
    session: ClientSession,
    sender: MailingPerson,
    to: Iterable[MailingPerson],
    subject: str,
    text: str = "",
    bcc: Iterable[MailingPerson] = None,
    cc: Iterable[MailingPerson] = None,
) -> bool:
    """Uses SendinBlue API to send an email"""

    body = dict(
        sender=sender,
        to=to,
        htmlContent=format_text_for_email(text),
        textContent=text,
        subject=subject,
    )

    if bcc is not None:
        body['bcc'] = bcc

    if cc is not None:
        body['cc'] = cc

    return await send(session, body)


async def send_template(
    session: ClientSession,
    template_id: int,
    to: Iterable[MailingPerson],
    bcc: Iterable[MailingPerson] = None,
    cc: Iterable[MailingPerson] = None,
) -> bool:
    """Uses SendinBlue API to send an email from a template"""

    body = dict(to=to, templateId=template_id)

    if bcc is not None:
        body['bcc'] = bcc

    if cc is not None:
        body['cc'] = cc

    return await send(session, body)


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
