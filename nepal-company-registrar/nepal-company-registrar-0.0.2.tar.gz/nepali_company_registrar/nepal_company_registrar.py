import requests
from bs4 import BeautifulSoup

from nepali_company_registrar.conf import OGD_URL
from nepali_company_registrar.models import Company

from nepali_company_registrar.exceptions import CompanyNotFoundException


class NepalCompanyRegistrar:
    def __init__(self, company_name_input: str):

        self._company_name_input = company_name_input.lower()
        self._search_companies = []

    def _search_company(self, company_name: str):
        search_response = requests.post(
            url=OGD_URL,
            data={
                'txt_search': company_name
            }
        )

        soup = BeautifulSoup(markup=search_response.content, features='html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            data = [col.string for col in cols[1:]] if len(cols) == 7 else None
            if data:
                self._search_companies.append(Company(*data))
        return self._search_companies

    def is_valid(self):
        search_companies = [
            company.name.lower() for company in
            self._search_company(company_name=self._company_name_input)
        ]
        if self._company_name_input in search_companies:
            return True
        return False

    def get_company_detail(self):
        if not self.is_valid():
            raise CompanyNotFoundException('Company is not registered in Nepal Company Registrar.')
        company = self._search_companies[0]

        return {
            'name': company.name,
            'name_in_nepali': company.name_in_nepali,
            'registration_number': company.registration_number,
            'registration_date': company.registration_date,
            'company_type': company.company_type.type,
            'share_holder': company.company_type.share_holder,
            'address': company.address,
        }

    def list_similar_companies(self):
        companies = self._search_company(company_name=self._company_name_input)
        return [
            {
                'name': company.name
            }
            for company in companies
        ]
