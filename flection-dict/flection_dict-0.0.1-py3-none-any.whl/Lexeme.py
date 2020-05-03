from flection_dictionary.Labels import Labels, Przyslowek, Czasownik, Przymiotnik
from flection_dictionary.Filters import Filters

class MultiSegment:
    def __init__(self, line):
        self.line = line

    def __repr__(self):
        line = []
        line += self.line[0].split(' ')

        for i in range(len(line) - 1, -1, -1):
            if line[i] == '' or line[i] == '$' or line[i] == '#':
                line.pop(i)
            else:
                is_label = True
                for j in range(len(line[i])):
                    if line[i][j] == '*':
                        is_label = True
                        break
                    elif ord(line[i][j]) > 90 or ord(line[i][j]) < 60:
                        is_label = False
                        break
                if is_label:
                    line.pop(i)
        multi_segment = ''
        for word in line:
            multi_segment += word + ' '
        return multi_segment


class Lexeme:
    def __init__(self, regular, multi_segments=None):
        if regular is not None:
            self.basic_form = regular[0]
            self.flectional_label = regular[1]
            self.flection = []
            self.label = Labels.get_label_from_flectional_label(self.flectional_label)
            for index, word in enumerate(regular):
                if index in {0, 1}:
                    continue
                if word.isalpha():
                    self.flection.append((word, self.label.get_enum(index - 2)))
        else:
            self.basic_form = "None"
            self.flectional_label = "None"
            self.label = "None"
            self.flection = []
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]

    @staticmethod
    def pairwise(list_):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(list_)
        return zip(a, a)

    def __repr__(self):
        lexeme = f"Basic form --- {self.basic_form}\nLabel --- {self.flectional_label} - {self.label}\n"
        lexeme += "Flections: \n"
        for flection in self.flection:
            lexeme += "\t" + flection[0] + " --- " + str(flection[1]) + "\n"
        if self.multi_segments:
            lexeme += "Multi segments: \n"
            for multi_segment in self.multi_segments:
                lexeme += f"\t{str(multi_segment)}"
        return lexeme

    @staticmethod
    def get_key(my_dict, val):
        for key, value in my_dict.items():
            if val == value:
                return key
        return "key doesn't exist"


class NounLexeme(Lexeme):  # Rzeczownik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular, multi_segments)
        self.gerundive = False
        if filter_structure and Czasownik.Gerundive in filter_structure.forms.keys():
            self.is_gerundive = True
            self.flection.append((filter_structure.forms[Czasownik.Infinitive][0], Czasownik.Infinitive))
            self.verb_data = filter_structure.forms[Czasownik.Infinitive]

    def __repr__(self):
        result = f"{super().__repr__()}\n"
        if self.gerundive:
            result += f"Czasownik: {self.verb_data}"
        return result

    def get_verb_data(self):
        return self.verb_data

    def is_gerundive(self):
        return self.gerundive


class VerbLexeme(Lexeme):  # Czasownik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)
        self.label = Labels.CZASOWNIK
        participles = [Czasownik.Present_Adverbial_Participle, Czasownik.Active_Adjectival_Participle,
                       Czasownik.Passive_Adjectival_Participle, Czasownik.Perfect_Adverbial_Participle]
        self.participles = dict()
        if filter_structure:
            for participle in participles:
                if participle in filter_structure.forms.keys():
                    self.flection.append((filter_structure.forms[participle][0], participle))
                    self.participles[participle] = filter_structure.forms[participle]
            if Czasownik.Gerundive in filter_structure.forms.keys():
                self.flection.append((filter_structure.forms[Czasownik.Gerundive][0], Czasownik.Gerundive))
                self.gerundive = filter_structure.forms[Czasownik.Gerundive]

    def get_present_adverbial_participle_data(self):
        enum = Czasownik.Present_Adverbial_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_active_adjectival_participle_data(self):
        enum = Czasownik.Active_Adjectival_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_passive_adjectival_participle_data(self):
        enum = Czasownik.Passive_Adjectival_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_perfect_adverbial_participle_data(self):
        enum = Czasownik.Perfect_Adverbial_Participle
        if enum in self.participles.keys():
            return self.participles[enum]
        else:
            return None

    def get_gerundive_data(self):
        if self.gerundive:
            return self.gerundive
        else:
            return None


class AdjectiveLexeme(Lexeme):  # Przymiotnik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)
        self.is_gradable = False
        self.is_participle = False
        if filter_structure:
            if filter_structure.filter_kind == Filters.AdjectionComparison:
                my_grade = Lexeme.get_key(filter_structure.forms, (self.basic_form, self.flectional_label))
                grades = {Przymiotnik.Positive_Form, Przymiotnik.Comparative_Form, Przymiotnik.Superlative_Form}
                grades.remove(my_grade)
                self.grades = dict()
                for grade in grades:
                    self.flection.append((filter_structure.forms[grade][0], grade))
                    self.grades[grade] = filter_structure.forms[grade]
                self.is_gradable = True
                self.my_grade = my_grade
            else:
                my_participle = Lexeme.get_key(filter_structure.forms, (self.basic_form, self.flectional_label))
                self.label = my_participle
                self.flection.append((filter_structure.forms[Czasownik.Infinitive][0], Czasownik.Infinitive))
                self.is_participle = True
                self.verb_data = filter_structure.forms[Czasownik.Infinitive]

    def get_grades(self):
        if hasattr(self, "grades"):
            return self.grades
        return None

    def get_verb_data(self):
        if hasattr(self, "verb_data"):
            return self.verb_data
        return None

    def get_my_grade(self):
        if hasattr(self, "my_grade"):
            return self.my_grade
        return None


class NumeralLexeme(Lexeme):  # Liczebnik
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)


class PronounLexeme(Lexeme):  # Zaimek
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular,  multi_segments)


class AdverbLexeme(Lexeme):  # Przysłówek
    def __init__(self, regular, filter_structure, multi_segments=None):
        super().__init__(regular, multi_segments)
        if filter_structure:
            if filter_structure.filter_kind == Filters.AdverbComparison:
                self.is_gradable = True
                self.my_grade = Przyslowek.Positive_Form
                grades = [Przyslowek.Comparative_Form, Przyslowek.Superlative_Form]
                self.grades = dict()
                for grade in grades:
                    self.flection.append((filter_structure.forms[grade][0], grade))
                    self.grades[grade] = filter_structure.forms[grade]
        else:  # w pospolite niestopniowalne przysłówki nie mają 3 kolumny :/
            self.flection.append((regular[0], Przyslowek.Positive_Form))
            self.is_gradable = False


class UninflectedLexeme(Lexeme):  # Nieodmienne
    def __init__(self, regular, filter_structure, multi_segments=None):
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.flection = []
        self.label = Labels.NIEODMIENNY
        if filter_structure:  # imiesłów przysłówkowy
            my_participle = Lexeme.get_key(filter_structure.forms, (self.basic_form, self.flectional_label))
            self.label = my_participle
            self.flection.append((regular[2], my_participle))
            self.flection.append((filter_structure.forms[Czasownik.Infinitive][0], Czasownik.Infinitive))
        else:
            self.flection.append((regular[2], Labels.NIEODMIENNY))
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]


class TextLexeme(Lexeme):  # Text
    def __init__(self, regular, filter_structure, multi_segments=None):
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.flection = []
        self.label = Labels.TEKST
        self.flection.append((regular[2], Labels.TEKST))
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]


class AcronymLexeme(Lexeme):  # Skrótowiec, Akronim
    def __init__(self, regular, filter_structure, multi_segments=None):
        self.basic_form = regular[0]
        self.flectional_label = regular[1]
        self.flection = []
        self.label = Labels.SKROT
        self.flection.append((regular[2], Labels.SKROT))
        self.multi_segments = [MultiSegment(multi_segment) for multi_segment in multi_segments]
