from datasets import company_type_conversion, share_holder_conversion


class CompanyType:
    def __init__(self, company_type, share_holder=None):
        self.share_holder = share_holder
        self.type = company_type


class Company:
    """
    Model describing a Company
    """
    def __init__(self, registration_number, registration_date, name, name_in_nepali, company_type, address):
        self.address = address
        self.company_type = company_type
        self.name_in_nepali = name_in_nepali
        self.name = name
        self.registration_number = registration_number
        self.registration_date = registration_date
        self._company_type_model()

    def _company_type_model(self):
        final_data = {}
        data = self.company_type.split('>>')
        for d in data:
            d = d.lstrip().rstrip()
            if d in company_type_conversion:
                final_data['company_type'] = company_type_conversion[d]
                continue
            elif d in share_holder_conversion:
                final_data['share_holder'] = share_holder_conversion[d]
                continue
        self.company_type = CompanyType(**final_data)

    def __repr__(self):
        return self.name
