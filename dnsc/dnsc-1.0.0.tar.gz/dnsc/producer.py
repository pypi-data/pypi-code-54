import aiofiles
import asyncio
import asyncpg
import csv
import io
import tempfile
import tldextract
import logging


async def produce_all_targets(queue: asyncio.Queue, pool: asyncpg.pool.Pool, logger: logging.Logger = None):
    counter: int = 0

    try:
        async with pool.acquire() as dbconn:
            # Get the total number of targets so we can have a progress bar
            records = await dbconn.fetch("SELECT reltuples::bigint AS estimate FROM pg_class where relname='targets'")
            total_targets = records[0]['estimate']

            if logger:
                logger.info(f'produce_all_targets: iterating over an estimated {total_targets} records')

            async with dbconn.transaction():
                # Create a temporary file
                with tempfile.TemporaryFile(mode='w+b') as fout:
                    # Copy the entire table into our temporary file
                    await dbconn.copy_from_table('targets', columns=('hostname', 'domain'), output=fout, format='csv')
                    
                    # Go to the start of the file and start reading it
                    fout.seek(0)

                    if logger:
                        logger.info('produce_all_targets: reading from temporary file')
                    csvreader = csv.reader(io.TextIOWrapper(fout))
                    for row in csvreader:
                        if row[0]:
                            record = '.'.join(row)
                        else:
                            record = row[1]

                        try:
                            parts = tldextract.extract(record)
                        except Exception:
                            continue

                        # Push it to the queue
                        await queue.put((record, parts))
                        counter += 1

                        if counter % 10000 == 0:
                            logger.info(f'produce_all_targets: processed {counter} records')
    except Exception as e:
        if logger:
            logger.warning(f'produce_all_targets: {e}')

    if logger:
        logger.info(f'produce_all_targets: done ({counter} records)')


async def produce_aiofile(queue: asyncio.Queue, filename: str, batch: int = 0):
    async with aiofiles.open(filename, mode='r') as fin:
        async for line in fin:
            hostname = line.strip().lower()

            # Validate the hostname
            parts = tldextract.extract(hostname)

            # We only care about valid domains w/ suffixes
            if parts.suffix and parts.domain:
                await queue.put((hostname, parts))


async def produce_file(queue: asyncio.Queue, filename: str, batch: int = 0):
    """Read entries from a file and push them into the queue.

    If the "batch" parameter is provided then we push a list of hostnames into the queue
    instead of individual items. As a result, the consumer needs to be able to deal
    with a list of items from the queue.
    """
    with open(filename, mode='r') as fin:
        items = []
        for line in fin:
            hostname = line.strip().lower()

            # Validate the hostname
            parts = tldextract.extract(hostname)

            # We only care about valid domains w/ suffixes
            if parts.suffix and parts.domain:
                if batch > 0:
                    items.append((hostname, parts))
                else:
                    await queue.put((hostname, parts))

            if len(items) > batch:
                # Send it off for processing by the workers
                await queue.put(items)
                items = []

        if items:
            await queue.put(items)


async def produce_list(queue: asyncio.Queue, lst: list, batch: int = 0):
    """Read entries from a list and push them into the queue.

    If the "batch" parameter is provided then we push a list of hostnames into the queue
    instead of individual items. As a result, the consumer needs to be able to deal
    with a list of items from the queue.
    """

    items = []
    for hostname in lst:
        # Validate the hostname
        parts = tldextract.extract(hostname)

        # We only care about valid domains w/ suffixes
        if parts.suffix and parts.domain:
            if batch > 0:
                items.append((hostname, parts))
            else:
                await queue.put((hostname, parts))

        if len(items) > batch:
            # Send it off for processing by the workers
            await queue.put(items)
            items = []

    if items:
        await queue.put(items)
