from deepcrawl.utils import ImmutableAttributesMixin

report_immutable_fields = (
    'id',
    'account_id',
    'project_id',
    'crawl_id',

    'report_type',
    'report_template',
    'total_rows',
    'basic_total',
    'removed_total',
    'added_total',
    'missing_total',
    'change_weight',
    'total_weight',
    'beta',

    '_datasource_href',
    '_report_template_href',
    '_recent_report_trend_href',
    '_account_href',
    '_project_href',
    '_crawl_href',
    '_report_type_href',
    '_href',
    '_href_alt',
    '_report_downloads_href',
    '_report_rows_href',
    '_statistics_href',
    '_issues_href',
    '_added_report_href',
    '_added_report_href_alt',
    '_basic_report_href',
    '_basic_report_href_alt',
    '_missing_report_href',
    '_missing_report_href_alt',
)


class DeepCrawlReport(ImmutableAttributesMixin):
    __slots__ = report_immutable_fields

    mutable_attributes = []

    def __init__(self, account_id, project_id, crawl_id, report_data: dict):
        # relations
        self.id = report_data.get("id")
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id

        # attributes
        self.report_type = report_data.get('report_type')
        self.report_template = report_data.get('report_template')
        self.total_rows = report_data.get('total_rows')
        self.basic_total = report_data.get('basic_total')
        self.removed_total = report_data.get('removed_total')
        self.added_total = report_data.get('added_total')
        self.missing_total = report_data.get('missing_total')
        self.change_weight = report_data.get('change_weight')
        self.total_weight = report_data.get('total_weight')
        self.beta = report_data.get('beta')

        self._datasource_href = report_data.get('_datasource_href')
        self._report_template_href = report_data.get('_report_template_href')
        self._recent_report_trend_href = report_data.get('_recent_report_trend_href')
        self._account_href = report_data.get('_account_href')
        self._project_href = report_data.get('_project_href')
        self._crawl_href = report_data.get('_crawl_href')
        self._report_type_href = report_data.get('_report_type_href')
        self._href = report_data.get('_href')
        self._href_alt = report_data.get('_href_alt')
        self._report_downloads_href = report_data.get('_report_downloads_href')
        self._report_rows_href = report_data.get('_report_rows_href')
        self._statistics_href = report_data.get('_statistics_href')
        self._issues_href = report_data.get('_issues_href')
        self._added_report_href = report_data.get('_added_report_href')
        self._added_report_href_alt = report_data.get('_added_report_href_alt')
        self._basic_report_href = report_data.get('_basic_report_href')
        self._basic_report_href_alt = report_data.get('_basic_report_href_alt')
        self._missing_report_href = report_data.get('_missing_report_href')
        self._missing_report_href_alt = report_data.get('_missing_report_href_alt')

        super(DeepCrawlReport, self).__init__()
