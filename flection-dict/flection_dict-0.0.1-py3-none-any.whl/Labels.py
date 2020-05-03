from enum import Enum


class Labels(Enum):
    RZECZOWNIK = "A"
    CZASOWNIK = "B"
    PRZYMIOTNIK = "C"
    LICZEBNIK = "D"
    ZAIMEK = "E"
    PRZYSLOWEK = "F"
    NIEODMIENNY = "G"
    TEKST = "H"
    SKROT = "I"

    def __str__(self):
        switcherToName = {
            self.RZECZOWNIK: "Rzeczownik",
            self.CZASOWNIK: "Czasownik",
            self.PRZYMIOTNIK: "Przymiotnik",
            self.LICZEBNIK: "Liczebnik",
            self.ZAIMEK: "Zaimek",
            self.PRZYSLOWEK: "Przysłówek",
            self.NIEODMIENNY: "Nieodmienny",
            self.TEKST: "Tekst",
            self.SKROT: "Skrótowiec"
        }
        return switcherToName.get(self)

    @staticmethod
    def get_label_from_flectional_label(flectional_label):
        label_string = flectional_label.strip()
        label_string = flectional_label.strip('*')[0]
        if label_string not in set('ABCDEFGHI'):
            return None
        return Labels(label_string)

    def get_enum(self, index):
        switch_to_word_type = {
            self.RZECZOWNIK: list(Rzeczownik),
            self.CZASOWNIK: list(Czasownik),
            self.PRZYMIOTNIK: list(Przymiotnik),
            self.LICZEBNIK: list(Liczebnik),
            self.ZAIMEK: list(Zaimek),
            self.PRZYSLOWEK: list(Przyslowek)
        }

        return switch_to_word_type.get(self)[index]


class Forms:
    def rzeczownik(self):
        return list(Rzeczownik)

    def czasownik(self):
        return list(Czasownik)

    def przymiotnik(self):
        return list(Przymiotnik)

    def liczebnik(self):
        return list(Liczebnik)

    def zaimek(self):
        return list(Zaimek)

    def przyslowek(self):
        return list(Przyslowek)

    def count_indexes(self, regular_list, checked_word):
        indexes = []
        for index, word in enumerate(regular_list):
            if word == checked_word:
                indexes.append(index)
        if 0 in indexes:
            indexes.remove(0)
        return indexes

    def get_forms_values(self, regular_list, word):
        indexes = self.count_indexes(regular_list, word)
        label = Labels._get_label_from_flectional_label(regular_list[1])
        forms = []
        for index in indexes:
            forms.append(str(self.get_form_value(index, label)))
        return str(label) + ":\n\t" + "\n\t".join(forms)

    def get_form_label_from_index(self, index, label):
        method_name = label.name.lower()
        # if label in {Labels.NIEODMIENNY, Labels.TEKST, Labels.SKROT}:
        #     return ""
        method = getattr(self, method_name, lambda: "Invalid label")
        label_list = method()
        return label_list[index]

    def get_form_value(self, index, label):
        form_label = self.get_form_label_from_index(index, label)
        return str(form_label.value)


    @staticmethod
    def _get_index_of_label(label, searched_label):
        method_name = label.name.lower()
        method = getattr(method_name, lambda: "Invalid label")
        label_list = method()
        for index, label_iterator in enumerate(label_list):
            if label_iterator == searched_label:
                return index

class Rzeczownik(Enum):
    Singular_Nominative = "Liczba pojedyncza, Mianownik"
    Singular_Genitive = "Liczba pojedyncza, Dopełniacz"
    Singular_Dative = "Liczba pojedyncza, Celownik"
    Singular_Accusative = "Liczba pojedyncza, Biernik"
    Singular_Instrumental = "Liczba pojedyncza, Narzędnik"
    Singular_Locative = "Liczba pojedyncza, Miejscownik"
    Singular_Vocative = "Liczba pojedyncza, Wołacz"
    Plural_Nominative = "Liczba mnoga, Mianownik"
    Plural_Genitive = "Liczba mnoga, Dopełniacz"
    Plural_Dative = "Liczba mnoga, Celownik"
    Plural_Accusative = "Liczba mnoga, Biernik"
    Plural_Instrumental = "Liczba mnoga, Narzędnik"
    Plural_Locative = "Liczba mnoga, Miejscownik"
    Plural_Vocative = "Liczba mnoga, Wołacz"

    def __str__(self):
        return self.value

class Czasownik(Enum):
    Infinitive = "Bezokolicznik"
    Present_1_Singular = "Czas teraźniejszy, 1 osoba liczby pojedynczej"
    Present_2_Singular = "Czas teraźniejszy, 2 osoba liczby pojedynczej"
    Present_3_Singular = "Czas teraźniejszy, 3 osoba liczby pojedynczej"
    Present_1_Plural = "Czas teraźniejszy, 1 osoba liczby mnogiej"
    Present_2_Plural = "Czas teraźniejszy, 2 osoba liczby mnogiej"
    Present_3_Plural = "Czas teraźniejszy, 3 osoba liczby mnogiej"
    Imperative_2_Singular = "Tryb rozkazujący, 2 osoba liczby pojedynczej"
    Imperative_1_Plural = "Tryb rozkazujący, 1 osoba liczby mnogiej"
    Imperative_2_Plural = "Tryb rozkazujący, 2 osoba liczby mnogiej"
    Past_1_Singular_Masculine = "Czas przeszły, 1 osoba liczby pojedynczej, rodzaj męski"
    Past_2_Singular_Masculine = "Czas przeszły, 2 osoba liczby pojedynczej, rodzaj męski"
    Past_3_Singular_Masculine = "Czas przeszły, 3 osoba liczby pojedynczej, rodzaj męski"
    Past_1_Singular_Feminine = "Czas przeszły, 1 osoba liczby pojedynczej, rodzaj żeński"
    Past_2_Singular_Feminine = "Czas przeszły, 2 osoba liczby pojedynczej, rodzaj żeński"
    Past_3_Singular_Feminine = "Czas przeszły, 3 osoba liczby pojedynczej, rodzaj żeński"
    Past_1_Singular_Neuter = "Czas przeszły, 1 osoba liczby pojedynczej, rodzaj nijaki"
    Past_2_Singular_Neuter = "Czas przeszły, 2 osoba liczby pojedynczej, rodzaj nijaki"
    Past_3_Singular_Neuter = "Czas przeszły, 3 osoba liczby pojedynczej, rodzaj nijaki"
    Past_1_Plural_Masculine = "Czas przeszły, 1 osoba liczby mnogiej, rodzaj męskoosobowy"
    Past_2_Plural_Masculine = "Czas przeszły, 2 osoba liczby mnogiej, rodzaj męskoosobowy"
    Past_3_Plural_Masculine = "Czas przeszły, 3 osoba liczby mnogiej, rodzaj męskoosobowy"
    Past_1_Plural_NonMasculine = "Czas przeszły, 1 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    Past_2_Plural_NonMasculine = "Czas przeszły, 2 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    Past_3_Plural_NonMasculine = "Czas przeszły, 3 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    Conditional_1_Singular_Masculine = "Tryb przypuszczający, 1 osoba liczby pojedynczej, rodzaj męski"
    Conditional_2_Singular_Masculine = "Tryb przypuszczający, 2 osoba liczby pojedynczej, rodzaj męski"
    Conditional_3_Singular_Masculine = "Tryb przypuszczający, 3 osoba liczby pojedynczej, rodzaj męski"
    Conditional_1_Singular_Feminine = "Tryb przypuszczający, 1 osoba liczby pojedynczej, rodzaj żeński"
    Conditional_2_Singular_Feminine = "Tryb przypuszczający, 2 osoba liczby pojedynczej, rodzaj żeński"
    Conditional_3_Singular_Feminine = "Tryb przypuszczający, 3 osoba liczby pojedynczej, rodzaj żeński"
    Conditional_1_Singular_Neuter = "Tryb przypuszczający, 1 osoba liczby pojedynczej, rodzaj nijaki"
    Conditional_2_Singular_Neuter = "Tryb przypuszczający, 2 osoba liczby pojedynczej, rodzaj nijaki"
    Conditional_3_Singular_Neuter = "Tryb przypuszczający, 3 osoba liczby pojedynczej, rodzaj nijaki"
    Conditional_1_Plural_Masculine = "Tryb przypuszczający, 1 osoba liczby mnogiej, rodzaj męskoosobowy"
    Conditional_2_Plural_Masculine = "Tryb przypuszczający, 2 osoba liczby mnogiej, rodzaj męskoosobowy"
    Conditional_3_Plural_Masculine = "Tryb przypuszczający, 3 osoba liczby mnogiej, rodzaj męskoosobowy"
    Conditional_1_Plural_NonMasculine = "Tryb przypuszczający, 1 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    Conditional_2_Plural_NonMasculine = "Tryb przypuszczający, 2 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    Conditional_3_Plural_NonMasculine = "Tryb przypuszczający, 3 osoba liczby mnogiej, rodzaj niemęskoosobowy"
    Past_Impersonal = "Bezosobnik w czasie przeszłym"

    Present_Adverbial_Participle = "Imiesłów przysłówkowy współczesny"
    Active_Adjectival_Participle = "Imiesłów przymiotnikowy czynny"
    Passive_Adjectival_Participle = "Imiesłów przymiotnikowy bierny"
    Perfect_Adverbial_Participle = "Imiesłów przysłówkowy uprzedni"
    Gerundive = "Rzeczownik odczasownikowy"

    def __str__(self):
        return self.value

class Przymiotnik(Enum):
    Singular_Nominative_Masculine_Personal_Animate = "Liczba pojedyncza, Mianownik, rodzaj męski osobowy i męski żywotny"
    Singular_Genitive_Masculine_Personal_Animate = "Liczba pojedyncza, Dopełniacz, rodzaj męski osobowy i męski żywotny"
    Singular_Dative_Masculine_Personal_Animate = "Liczba pojedyncza, Celownik, rodzaj męski osobowy i męski żywotny"
    Singular_Accusative_Masculine_Personal_Animate = "Liczba pojedyncza, Biernik, rodzaj męski osobowy i męski żywotny"
    Singular_Instrumental_Masculine_Personal_Animate = "Liczba pojedyncza, Narzędnik, rodzaj męski osobowy i męski żywotny"
    Singular_Locative_Masculine_Personal_Animate = "Liczba pojedyncza, Miejscownik, rodzaj męski osobowy i męski żywotny"
    Singular_Vocative_Masculine_Personal_Animate = "Liczba pojedyncza, Wołacz, rodzaj męski osobowy i męski żywotny"
    Singular_Nominative_Masculine_NonPersonal = "Liczba pojedyncza, Mianownik, rodzaj męski nieosobowy"
    Singular_Genitive_Masculine_NonPersonal = "Liczba pojedyncza, Dopełniacz, rodzaj męski nieosobowy"
    Singular_Dative_Masculine_NonPersonal = "Liczba pojedyncza, Celownik, rodzaj męski nieosobowy"
    Singular_Accusative_Masculine_NonPersonal = "Liczba pojedyncza, Biernik, rodzaj męski nieosobowy"
    Singular_Instrumental_Masculine_NonPersonal = "Liczba pojedyncza, Narzędnik, rodzaj męski nieosobowy"
    Singular_Locative_Masculine_NonPersonal = "Liczba pojedyncza, Miejscownik, rodzaj męski nieosobowy"
    Singular_Vocative_Masculine_NonPersonal = "Liczba pojedyncza, Wołacz, rodzaj męski nieosobowy"
    Singular_Nominative_Feminine = "Liczba pojedyncza, Mianownik, rodzaj żeński"
    Singular_Genitive_Feminine = "Liczba pojedyncza, Dopełniacz, rodzaj żeński"
    Singular_Dative_Feminine = "Liczba pojedyncza, Celownik, rodzaj żeński"
    Singular_Accusative_Feminine = "Liczba pojedyncza, Biernik, rodzaj żeński"
    Singular_Instrumental_Feminine = "Liczba pojedyncza, Narzędnik, rodzaj żeński"
    Singular_Locative_Feminine = "Liczba pojedyncza, Miejscownik, rodzaj żeński"
    Singular_Vocative_Feminine = "Liczba pojedyncza, Wołacz, rodzaj żeński"
    Singular_Nominative_Neuter = "Liczba pojedyncza, Mianownik, rodzaj nijaki"
    Singular_Genitive_Neuter = "Liczba pojedyncza, Dopełniacz, rodzaj nijaki"
    Singular_Dative_Neuter = "Liczba pojedyncza, Celownik, rodzaj nijaki"
    Singular_Accusative_Neuter = "Liczba pojedyncza, Biernik, rodzaj nijaki"
    Singular_Instrumental_Neuter = "Liczba pojedyncza, Narzędnik, rodzaj nijaki"
    Singular_Locative_Neuter = "Liczba pojedyncza, Miejscownik, rodzaj nijaki"
    Singular_Vocative_Neuter = "Liczba pojedyncza, Wołacz, rodzaj nijaki"
    Plural_Nominative_Masculine = "Liczba mnoga, Mianownik, rodzaj męskoosobowy"
    Plural_Genitive_Masculine = "Liczba mnoga, Dopełniacz, rodzaj męskoosobowy"
    Plural_Dative_Masculine = "Liczba mnoga, Celownik, rodzaj męskoosobowy"
    Plural_Accusative_Masculine = "Liczba mnoga, Biernik, rodzaj męskoosobowy"
    Plural_Instrumental_Masculine = "Liczba mnoga, Narzędnik, rodzaj męskoosobowy"
    Plural_Locative_Masculine = "Liczba mnoga, Miejscownik, rodzaj męskoosobowy"
    Plural_Vocative_Masculine = "Liczba mnoga, Wołacz, rodzaj męskoosobowy"
    Plural_Nominative_NonMasculine = "Liczba mnoga, Mianownik, rodzaj niemęskoosobowy"
    Plural_Genitive_NonMasculine = "Liczba mnoga, Dopełniacz, rodzaj niemęskoosobowy"
    Plural_Dative_NonMasculine = "Liczba mnoga, Celownik, rodzaj niemęskoosobowy"
    Plural_Accusative_NonMasculine = "Liczba mnoga, Biernik, rodzaj niemęskoosobowy"
    Plural_Instrumental_NonMasculine = "Liczba mnoga, Narzędnik, rodzaj niemęskoosobowy"
    Plural_Locative_NonMasculine = "Liczba mnoga, Miejscownik, rodzaj niemęskoosobowy"
    Plural_Vocative_NonMasculine = "Liczba mnoga, Wołacz, rodzaj niemęskoosobowy"

    Positive_Form = "Stopień równy"
    Comparative_Form = "Stopień wyższy"
    Superlative_Form = "Stopień najwyższy"

    def __str__(self):
        return self.value

class Liczebnik(Enum):
    Singular_Nominative_Masculine_Personal = "Liczba pojedyncza, Mianownik, rodzaj męski osobowy"
    Singular_Genitive_Masculine_Personal = "Liczba pojedyncza, Dopełniacz, rodzaj męski osobowy"
    Singular_Dative_Masculine_Personal = "Liczba pojedyncza, Celownik, rodzaj męski osobowy"
    Singular_Accusative_Masculine_Personal = "Liczba pojedyncza, Biernik, rodzaj męski osobowy"
    Singular_Instrumental_Masculine_Personal = "Liczba pojedyncza, Narzędnik, rodzaj męski osobowy"
    Singular_Locative_Masculine_Personal = "Liczba pojedyncza, Miejscownik, rodzaj męski osobowy"
    Singular_Vocative_Masculine_Personal = "Liczba pojedyncza, Wołacz, rodzaj męski osobowy"
    Singular_Nominative_Masculine_Animate = "Liczba pojedyncza, Mianownik, rodzaj męski żywotny"
    Singular_Genitive_Masculine_Animate = "Liczba pojedyncza, Dopełniacz, rodzaj męski żywotny"
    Singular_Dative_Masculine_Animate = "Liczba pojedyncza, Celownik, rodzaj męski żywotny"
    Singular_Accusative_Masculine_Animate = "Liczba pojedyncza, Biernik, rodzaj męski żywotny"
    Singular_Instrumental_Masculine_Animate = "Liczba pojedyncza, Narzędnik, rodzaj męski żywotny"
    Singular_Locative_Masculine_Animate = "Liczba pojedyncza, Miejscownik, rodzaj męski żywotny"
    Singular_Vocative_Masculine_Animate = "Liczba pojedyncza, Wołacz, rodzaj męski żywotny"
    Singular_Nominative_Masculine_NonPersonal = "Liczba pojedyncza, Mianownik, rodzaj męski nieosobowy"
    Singular_Genitive_Masculine_NonPersonal = "Liczba pojedyncza, Dopełniacz, rodzaj męski nieosobowy"
    Singular_Dative_Masculine_NonPersonal = "Liczba pojedyncza, Celownik, rodzaj męski nieosobowy"
    Singular_Accusative_Masculine_NonPersonal = "Liczba pojedyncza, Biernik, rodzaj męski nieosobowy"
    Singular_Instrumental_Masculine_NonPersonal = "Liczba pojedyncza, Narzędnik, rodzaj męski nieosobowy"
    Singular_Locative_Masculine_NonPersonal = "Liczba pojedyncza, Miejscownik, rodzaj męski nieosobowy"
    Singular_Vocative_Masculine_NonPersonal = "Liczba pojedyncza, Wołacz, rodzaj męski nieosobowy"
    Singular_Nominative_Feminine = "Liczba pojedyncza, Mianownik, rodzaj żeński"
    Singular_Genitive_Feminine = "Liczba pojedyncza, Dopełniacz, rodzaj żeński"
    Singular_Dative_Feminine = "Liczba pojedyncza, Celownik, rodzaj żeński"
    Singular_Accusative_Feminine = "Liczba pojedyncza, Biernik, rodzaj żeński"
    Singular_Instrumental_Feminine = "Liczba pojedyncza, Narzędnik, rodzaj żeński"
    Singular_Locative_Feminine = "Liczba pojedyncza, Miejscownik, rodzaj żeński"
    Singular_Vocative_Feminine = "Liczba pojedyncza, Wołacz, rodzaj żeński"
    Singular_Nominative_Neuter = "Liczba pojedyncza, Mianownik, rodzaj nijaki"
    Singular_Genitive_Neuter = "Liczba pojedyncza, Dopełniacz, rodzaj nijaki"
    Singular_Dative_Neuter = "Liczba pojedyncza, Celownik, rodzaj nijaki"
    Singular_Accusative_Neuter = "Liczba pojedyncza, Biernik, rodzaj nijaki"
    Singular_Instrumental_Neuter = "Liczba pojedyncza, Narzędnik, rodzaj nijaki"
    Singular_Locative_Neuter = "Liczba pojedyncza, Miejscownik, rodzaj nijaki"
    Singular_Vocative_Neuter = "Liczba pojedyncza, Wołacz, rodzaj nijaki"
    Plural_Nominative_Masculine = "Liczba mnoga, Mianownik, rodzaj męskoosobowy"
    Plural_Genitive_Masculine = "Liczba mnoga, Dopełniacz, rodzaj męskoosobowy"
    Plural_Dative_Masculine = "Liczba mnoga, Celownik, rodzaj męskoosobowy"
    Plural_Accusative_Masculine = "Liczba mnoga, Biernik, rodzaj męskoosobowy"
    Plural_Instrumental_Masculine = "Liczba mnoga, Narzędnik, rodzaj męskoosobowy"
    Plural_Locative_Masculine = "Liczba mnoga, Miejscownik, rodzaj męskoosobowy"
    Plural_Vocative_Masculine = "Liczba mnoga, Wołacz, rodzaj męskoosobowy"
    Plural_Nominative_NonMasculine = "Liczba mnoga, Mianownik, rodzaj niemęskoosobowy"
    Plural_Genitive_NonMasculine = "Liczba mnoga, Dopełniacz, rodzaj niemęskoosobowy"
    Plural_Dative_NonMasculine = "Liczba mnoga, Celownik, rodzaj niemęskoosobowy"
    Plural_Accusative_NonMasculine = "Liczba mnoga, Biernik, rodzaj niemęskoosobowy"
    Plural_Instrumental_NonMasculine = "Liczba mnoga, Narzędnik, rodzaj niemęskoosobowy"
    Plural_Locative_NonMasculine = "Liczba mnoga, Miejscownik, rodzaj niemęskoosobowy"
    Plural_Vocative_NonMasculine = "Liczba mnoga, Wołacz, rodzaj niemęskoosobowy"

    def __str__(self):
        return self.value

class Zaimek(Enum):
    Singular_Nominative = "Liczba pojedyncza, Mianownik"
    Singular_Genitive = "Liczba pojedyncza, Dopełniacz"
    Singular_Dative = "Liczba pojedyncza, Celownik"
    Singular_Accusative = "Liczba pojedyncza, Biernik"
    Singular_Instrumental = "Liczba pojedyncza, Narzędnik"
    Singular_Locative = "Liczba pojedyncza, Miejscownik"
    Singular_Vocative = "Liczba pojedyncza, Wołacz"
    Plural_Nominative = "Liczba mnoga, Mianownik"
    Plural_Genitive = "Liczba mnoga, Dopełniacz"
    Plural_Dative = "Liczba mnoga, Celownik"
    Plural_Accusative = "Liczba mnoga, Biernik"
    Plural_Instrumental = "Liczba mnoga, Narzędnik"
    Plural_Locative = "Liczba mnoga, Miejscownik"
    Plural_Vocative = "Liczba mnoga, Wołacz"

    def __str__(self):
        return self.value

class Przyslowek(Enum):
    Positive_Form = "Stopień równy"
    Comparative_Form = "Stopień wyższy"
    Superlative_Form = "Stopień najwyższy"

    def __str__(self):
        return self.value