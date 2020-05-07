from .italian_vat_type import ItalianVATType


class FuzzyItalianVATType(ItalianVATType):

    def convert(self, candidate):
        return super().convert(candidate).zfill(11)