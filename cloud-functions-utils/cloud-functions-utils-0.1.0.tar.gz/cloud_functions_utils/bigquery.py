"""
This module provides a function to insert rows into a Google BigQuery table.
"""

import os

from datetime import datetime

from google.cloud import bigquery


class InsertionError(Exception):
    """
    Error that is thrown when insertion into Google BigQuery does not succeed.
    """


class EmptyRowsError(Exception):
    """
    Error that is thrown when trying to insert an empty list to Google BigQuery.
    """


class BQInserter:
    def __init__(self, project=None, dataset=None, table=None):
        self._project = project or os.environ["BQ_PROJECT"]
        self._dataset = dataset or os.environ["BQ_DATASET"]
        self._table = table or os.environ["BQ_TABLE"]
        self._bq_client = bigquery.Client()
        self._bq_dataset = bigquery.dataset.DatasetReference.from_string(
            f"{self._project}.{self._dataset}"
        )
        self._bq_table = self._bq_dataset.table(self._table)

    @staticmethod
    def _add_inserted_at_field(rows):
        inserted_at = datetime.now()
        for row in rows:
            row.update({"inserted_at": inserted_at})

    def __call__(self, rows):
        print(f"Inserting rows into `{self._project}:{self._dataset}.{self._table}`.")
        if not rows:
            raise EmptyRowsError
        self._add_inserted_at_field(rows)
        errors = self._bq_client.insert_rows(
            self._bq_client.get_table(self._bq_table), rows
        )
        if errors:
            raise InsertionError(errors)


def insert_rows(rows, project=None, dataset=None, table=None):
    BQInserter(project, dataset, table)(rows)
