from datetime import datetime


async def get_emails(db, address):
    emails = await db.emails.find(
        {'to': address}
    ).to_list(50)
    return emails


async def get_email(db, uuid):
    email = await db.emails.find_one({'uuid': uuid})
    return email


async def create_mailbox(db, address, token):
    document = {
        'address': address,
        'token': token,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'emails': [],
    }
    mailbox = await db.mailboxes.insert_one(document)
    return mailbox


async def get_mailbox_by_address(db, address):
    mailbox = await db.mailboxes.find_one({'address': address})
    return mailbox


async def get_mailbox_by_token(db, token):
    mailbox = await db.mailboxes.find_one({'token': token})
    return mailbox


async def delete_mailbox_by_token(db, token):
    await db.mailboxes.delete_many({'token': token})
