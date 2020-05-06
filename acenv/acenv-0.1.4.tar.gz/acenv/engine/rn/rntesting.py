
import unittest
from fractions import Fraction
from decimal import Decimal

from .rn import *


class TestRN(unittest.TestCase):
    def test_rnu(self):
        # test string parser
        self.assertEqual(RNU(s='-2'), RNU(Ra(-2)))
        self.assertEqual(RNU(s='5/4'), RNU(Ra(Fraction(5, 4))))
        self.assertEqual(RNU(s='6.7'), RNU(Ra(Fraction(67, 10))))
        self.assertEqual(RNU(s='-7.6'), RNU(Ra(Fraction(-76, 10))))

        self.assertEqual(RNU(s='[2]√2'), RNU(Ra(1), Ir(2, 2)))
        self.assertEqual(RNU(s='[3]√-4/6'), RNU(Ra(-1), Ir(Fraction(2, 3), 3)))
        self.assertEqual(RNU(s='-3.3[4]√5/2'), RNU(Ra(Fraction(-33, 10)), Ir(Fraction(5, 2), 4)))
        self.assertEqual(RNU(s='-5/4[5]√-6.2'), RNU(Ra(Fraction(-5, 4)), Ir(Fraction(-31, 5), 5)))

        # test data parser
        self.assertEqual(RNU(Ra(2), Ir(-4, 3)), RNU(Ra(-2), Ir(4, 3)))
        self.assertEqual(RNU(Ra(1), Ir(8, 2)), RNU(Ra(2), Ir(2, 2)))
        self.assertEqual(RNU(Ra(1), Ir(81, 3)), RNU(Ra(3), Ir(3, 3)))
        self.assertEqual(RNU(Ra(4), Ir(0, 3)), RNU(Ra(0), Ir(1, 1)))

        # test rationalization
        self.assertEqual(RNU(Ra(3), Ir(Fraction(1, 3), 2)), RNU(Ra(1), Ir(3, 2)))
        self.assertEqual(RNU(Ra(1), Ir(Fraction(1, 32), 3)), RNU(Ra(Fraction(1, 4)), Ir(2, 3)))
        self.assertEqual(RNU(Ra(2), Ir(Fraction(1, 6), 3)), RNU(Ra(Fraction(1, 3)), Ir(36, 3)))
        self.assertEqual(RNU(Ra(4), Ir(Fraction(1, 4), 3)), RNU(Ra(2), Ir(2, 3)))

        # test is_compatible
        self.assertEqual(RNU(Ra(3), Ir(3, 4)).is_compatible(RNU(Ra(4), Ir(3, 4))), True)
        self.assertEqual(RNU(Ra(1), Ir(2, 2)).is_compatible(RNU(Ra(-2), Ir(2, 3))), False)
        self.assertEqual(RNU(Ra(5), Ir(8, 2)).is_compatible(RNU(Ra(10), Ir(2, 2))), True)
        self.assertEqual(RNU(Ra(1), Ir(4, 2)).is_compatible(RNU(Ra(10), Ir(1, 1))), True)

        # test add
        self.assertEqual(RNU(Ra(3), Ir(3, 4)) + RNU(Ra(4), Ir(3, 4)), RNU(Ra(7), Ir(3, 4)))
        self.assertEqual(RNU(Ra(1), Ir(2, 2)) + RNU(Ra(-2), Ir(2, 2)), RNU(Ra(-1), Ir(2, 2)))
        self.assertEqual(RNU(Ra(5), Ir(8, 2)) + RNU(Ra(10), Ir(2, 2)), RNU(Ra(20), Ir(2, 2)))
        self.assertEqual(RNU(Ra(1), Ir(4, 2)) + RNU(Ra(10), Ir(1, 1)), RNU(Ra(12), Ir(1, 1)))

    def test_lrn(self):
        # assign values
        lrn_1 = LRN([RNU(Ra(6))])  # 6
        lrn_2 = LRN([RNU(Ra(-4))])  # -4
        lrn_3 = LRN([RNU(Ra(Fraction(4, 5)))])  # 4/5
        lrn_4 = LRN([RNU(Ra(Fraction(-8, 3)))])  # -8/3
        lrn_5 = LRN([RNU(Ra(1), Ir(2, 2))])  # √2
        lrn_6 = LRN([RNU(Ra(-1), Ir(3, 2))])  # -√3
        lrn_7 = LRN([RNU(Ra(1), Ir(5, 3))])  # [3]√5
        lrn_8 = LRN([RNU(Ra(-1), Ir(6, 5))])  # -[5]√6
        lrn_9 = LRN([RNU(Ra(2), Ir(3, 2))])  # 2√3
        lrn_10 = LRN([RNU(Ra(-4), Ir(5, 2))])  # -4√5
        lrn_11 = LRN([RNU(Ra(Fraction(5, 3)), Ir(6, 2))])  # 5/3√6
        lrn_12 = LRN([RNU(Ra(Fraction(-8, 7)), Ir(10, 3))])  # -8/7[3]√10
        lrn_13 = LRN([RNU(Ra(2)), RNU(Ra(-1), Ir(2, 2))])  # 2 - √2
        lrn_14 = LRN([RNU(Ra(Fraction(1, 2))), RNU(Ra(1), Ir(5, 3))])  # 1/2 + [3]√5
        lrn_15 = LRN([RNU(Ra(4)), RNU(Ra(-2), Ir(2, 2)), RNU(Ra(1), Ir(3, 3))])  # 4 - 2√2 + [3]√3
        lrn_16 = LRN([RNU(Ra(7)), RNU(Ra(Fraction(2, 3)), Ir(5, 2))])  # 7 + 2/3√5
        lrn_17 = LRN([RNU(Ra(2)), RNU(Ra(4)), RNU(Ra(-2), Ir(2, 2))])  # 2 + 4 - 2√2
        lrn_18 = LRN([RNU(Ra(Fraction(7, 5))), RNU(Ra(Fraction(1, 2))), RNU(Ra(-1), Ir(5, 3))])  # 7/5 + 1/2 - [3]√5
        lrn_19 = LRN([RNU(Ra(2), Ir(5, 3)), RNU(Ra(-6), Ir(5, 3)), RNU(Ra(3))])  # 2[3]√5 - 6[3]√5 + 3
        lrn_20 = LRN([RNU(Ra(2), Ir(9, 4)), RNU(Ra(5), Ir(3, 2)), RNU(Ra(-6))])  # 2[4]√9 + 5√3 - 6

        # test data parser
        self.assertEqual(set(lrn_17.units), {RNU(Ra(-2), Ir(2, 2)), RNU(Ra(6))})
        self.assertEqual(set(lrn_18.units), {RNU(Ra(-1), Ir(5, 3)), RNU(Ra(Fraction(19, 10)))})
        self.assertEqual(set(lrn_19.units), {RNU(Ra(-4), Ir(5, 3)), RNU(Ra(3))})
        self.assertEqual(set(lrn_20.units), {RNU(Ra(7), Ir(3, 2)), RNU(Ra(-6))})

        # # test properties
        # test is_rational
        self.assertEqual(lrn_1.is_rational, True)
        self.assertEqual(lrn_2.is_rational, True)
        self.assertEqual(lrn_3.is_rational, True)
        self.assertEqual(lrn_4.is_rational, True)

        self.assertEqual(lrn_5.is_rational, False)
        self.assertEqual(lrn_6.is_rational, False)
        self.assertEqual(lrn_7.is_rational, False)
        self.assertEqual(lrn_8.is_rational, False)

        self.assertEqual(lrn_9.is_rational, False)
        self.assertEqual(lrn_10.is_rational, False)
        self.assertEqual(lrn_11.is_rational, False)
        self.assertEqual(lrn_12.is_rational, False)

        # test is_irrational
        self.assertEqual(lrn_1.is_irrational, False)
        self.assertEqual(lrn_2.is_irrational, False)
        self.assertEqual(lrn_3.is_irrational, False)
        self.assertEqual(lrn_4.is_irrational, False)

        self.assertEqual(lrn_5.is_irrational, True)
        self.assertEqual(lrn_6.is_irrational, True)
        self.assertEqual(lrn_7.is_irrational, True)
        self.assertEqual(lrn_8.is_irrational, True)

        self.assertEqual(lrn_9.is_irrational, False)
        self.assertEqual(lrn_10.is_irrational, False)
        self.assertEqual(lrn_11.is_irrational, False)
        self.assertEqual(lrn_12.is_irrational, False)

        # test is_integer
        self.assertEqual(lrn_1.is_integer, True)
        self.assertEqual(lrn_2.is_integer, True)
        self.assertEqual(lrn_3.is_integer, False)
        self.assertEqual(lrn_4.is_integer, False)

        self.assertEqual(lrn_5.is_integer, False)
        self.assertEqual(lrn_6.is_integer, False)
        self.assertEqual(lrn_7.is_integer, False)
        self.assertEqual(lrn_8.is_integer, False)

        self.assertEqual(lrn_9.is_integer, False)
        self.assertEqual(lrn_10.is_integer, False)
        self.assertEqual(lrn_11.is_integer, False)
        self.assertEqual(lrn_12.is_integer, False)

        # test comparisons
        # test eq
        self.assertEqual(lrn_1 == LRN([RNU(Ra(6))]), True)
        self.assertEqual(lrn_2 == LRN([RNU(Ra(4))]), False)
        self.assertEqual(lrn_3 == LRN([RNU(Ra(-1), Ir(4, 5))]), False)
        self.assertEqual(lrn_4 == LRN([RNU(Ra(Fraction(16, -6)))]), True)

        self.assertEqual(lrn_5 == LRN([RNU(Ra(-1), Ir(2, 2))]), False)
        self.assertEqual(lrn_6 == LRN([RNU(Ra(-1), Ir(3, 2))]), True)
        self.assertEqual(lrn_7 == LRN([RNU(Ra(1), Ir(5, 3))]), True)
        self.assertEqual(lrn_8 == LRN([RNU(Ra(-1), Ir(6, 4))]), False)

        self.assertEqual(lrn_9 == LRN([RNU(Ra(4), Ir(3, 2))]), False)
        self.assertEqual(lrn_10 == LRN([RNU(Ra(-4), Ir(5, 2))]), True)
        self.assertEqual(lrn_11 == LRN([RNU(Ra(Fraction(5, 3)), Ir(6, 2))]), True)
        self.assertEqual(lrn_12 == LRN([RNU(Ra(Fraction(-8, 7)), Ir(10, 3))]), True)

        # test gt
        self.assertEqual(lrn_1 > lrn_3, True)
        self.assertEqual(lrn_2 > lrn_5, False)
        self.assertEqual(lrn_3 > lrn_12, True)
        self.assertEqual(lrn_4 > lrn_18, False)

        self.assertEqual(lrn_5 > lrn_2, True)
        self.assertEqual(lrn_6 > lrn_7, False)
        self.assertEqual(lrn_7 > lrn_11, False)
        self.assertEqual(lrn_8 > lrn_16, False)

        self.assertEqual(lrn_13 > lrn_4, True)
        self.assertEqual(lrn_14 > lrn_17, False)
        self.assertEqual(lrn_15 > lrn_6, True)
        self.assertEqual(lrn_16 > lrn_11, True)

        # test lt
        self.assertEqual(lrn_1 < lrn_3, False)
        self.assertEqual(lrn_2 < lrn_5, True)
        self.assertEqual(lrn_3 < lrn_12, False)
        self.assertEqual(lrn_4 < lrn_18, True)

        self.assertEqual(lrn_5 < lrn_2, False)
        self.assertEqual(lrn_6 < lrn_7, True)
        self.assertEqual(lrn_7 < lrn_11, True)
        self.assertEqual(lrn_8 < lrn_16, True)

        self.assertEqual(lrn_13 < lrn_4, False)
        self.assertEqual(lrn_14 < lrn_17, True)
        self.assertEqual(lrn_15 < lrn_6, False)
        self.assertEqual(lrn_16 < lrn_11, False)

        # test operations
        # test neg
        self.assertEqual(-lrn_1, LRN([RNU(Ra(-6))]))
        self.assertEqual(-lrn_2, LRN([RNU(Ra(4))]))
        self.assertEqual(-lrn_7, LRN([RNU(Ra(-1), Ir(5, 3))]))
        self.assertEqual(-lrn_8, LRN([RNU(Ra(1), Ir(6, 5))]))

        self.assertEqual(-lrn_9, LRN([RNU(Ra(-2), Ir(3, 2))]))
        self.assertEqual(-lrn_10, LRN([RNU(Ra(4), Ir(5, 2))]))
        self.assertEqual(-lrn_11, LRN([RNU(Ra(Fraction(-5, 3)), Ir(6, 2))]))
        self.assertEqual(-lrn_12, LRN([RNU(Ra(Fraction(8, 7)), Ir(10, 3))]))

        self.assertEqual(-lrn_14, LRN([RNU(Ra(Fraction(-1, 2))), RNU(Ra(-1), Ir(5, 3))]))
        self.assertEqual(-lrn_16, LRN([RNU(Ra(-7)), RNU(Ra(Fraction(-2, 3)), Ir(5, 2))]))
        self.assertEqual(-lrn_18, LRN([RNU(Ra(Fraction(-7, 5))), RNU(Ra(Fraction(-1, 2))), RNU(Ra(1), Ir(5, 3))]))
        self.assertEqual(-lrn_20, LRN([RNU(Ra(-2), Ir(9, 4)), RNU(Ra(-5), Ir(3, 2)), RNU(Ra(6))]))

        # test add
        self.assertEqual(lrn_1 + lrn_2, LRN([RNU(Ra(2))]))
        self.assertEqual(lrn_2 + lrn_5, LRN([RNU(Ra(-4)), RNU(Ra(1), Ir(2, 2))]))
        self.assertEqual(lrn_3 + lrn_11, LRN([RNU(Ra(Fraction(4, 5))), RNU(Ra(Fraction(5, 3)), Ir(6, 2))]))
        self.assertEqual(lrn_4 + lrn_15, LRN([RNU(Ra(Fraction(4, 3))), RNU(Ra(-2), Ir(2, 2)), RNU(Ra(1), Ir(3, 3))]))

        self.assertEqual(lrn_5 + lrn_3, LRN([RNU(Ra(Fraction(4, 5))), RNU(Ra(1), Ir(2, 2))]))
        self.assertEqual(lrn_8 + lrn_6, LRN([RNU(Ra(-1), Ir(3, 2)), RNU(Ra(-1), Ir(6, 5))]))
        self.assertEqual(lrn_10 + lrn_9, LRN([RNU(Ra(-4), Ir(5, 2)), RNU(Ra(2), Ir(3, 2))]))
        self.assertEqual(lrn_12 + lrn_20, LRN([RNU(Ra(Fraction(-8, 7)), Ir(10, 3)), RNU(Ra(7), Ir(3, 2)), RNU(Ra(-6))]))

        self.assertEqual(lrn_15 + lrn_4, LRN([RNU(Ra(Fraction(4, 3))), RNU(Ra(-2), Ir(2, 2)), RNU(Ra(1), Ir(3, 3))]))
        self.assertEqual(lrn_16 + lrn_7, LRN([RNU(Ra(7)), RNU(Ra(Fraction(2, 3)), Ir(5, 2)), RNU(Ra(1), Ir(5, 3))]))
        self.assertEqual(lrn_18 + lrn_13,
                         LRN([RNU(Ra(Fraction(39, 10))), RNU(Ra(-1), Ir(5, 3)), RNU(Ra(-1), Ir(2, 2))]))
        self.assertEqual(lrn_19 + lrn_17, LRN([RNU(Ra(9)), RNU(Ra(-4), Ir(5, 3)), RNU(Ra(-2), Ir(2, 2))]))

        # test sub
        # -> test neg
        self.assertEqual(-lrn_1, LRN([RNU(Ra(-6))]))
        self.assertEqual(-lrn_2, LRN([RNU(Ra(4))]))
        self.assertEqual(-lrn_3, LRN([RNU(Ra(Fraction(-4, 5)))]))
        self.assertEqual(-lrn_4, LRN([RNU(Ra(Fraction(8, 3)))]))

        # # test mul
        # -> already tested

        # test pow
        self.assertEqual(lrn_16 ** LRN([RNU(s='2')]), LRN([RNU(s='49'), RNU(s='20/9'), RNU(s='28/3[2]√5')]))

    def test_rn(self):
        rn1 = RN(2, 4)
        rn2 = RN(RNU(Ra(2), Ir(2, 2)), 4)
        rn3 = RN(LRN([RNU(s='3[2]√3'), RNU(s='-6')]), 3)
        rn4 = RN(LRN([RNU(s='2[2]√2'), RNU(s='-8[2]√5')]), 6)
        rn5 = RN(LRN([RNU(s='2/3[2]√3'), RNU(s='-5/3[2]√10')]), Fraction(1, 2))
        rn6 = RN(LRN([RNU(s='1/2'), RNU(s='3/4[2]√5')]), Fraction(3, 4))

        rn7 = RN(1, RNU(s='[2]√2'))
        rn8 = RN(LRN([RNU(s='2[2]√2'), RNU(s='-3')]), RNU(s='[2]√3'))
        rn9 = RN(LRN([RNU(s='2[2]√6'), RNU(s='8')]), RNU(s='4[3]√2'))
        rn10 = RN(1, LRN([RNU(s='[2]√2'), RNU(s='-1[2]√3')]))
        rn11 = RN(LRN([RNU(s='[2]√5'), RNU(s='-1[2]√6')]), LRN([RNU(s='[2]√5'), RNU(s='[2]√6')]))
        rn12 = RN(RNU(s='3[3]√2'), LRN([RNU(s='2[2]√10'), RNU(s='-1[2]√2')]))

        # test data parser
        self.assertEqual(rn1.numerator, LRN([RNU(Ra(1))]))
        self.assertEqual(rn1.denominator, LRN([RNU(Ra(2))]))
        self.assertEqual(rn2.numerator, LRN([RNU(Ra(1), Ir(2, 2))]))
        self.assertEqual(rn2.denominator, LRN([RNU(Ra(2))]))

        self.assertEqual(rn3.numerator, LRN([RNU(s='[2]√3'), RNU(s='-2')]))
        self.assertEqual(rn3.denominator, LRN([RNU(s='1')]))
        self.assertEqual(rn4.numerator, LRN([RNU(s='[2]√2'), RNU(s='-4[2]√5')]))
        self.assertEqual(rn4.denominator, LRN([RNU(s='3')]))

        self.assertEqual(rn5.numerator, LRN([RNU(s='4[2]√3'), RNU(s='-10[2]√10')]))
        self.assertEqual(rn5.denominator, LRN([RNU(s='3')]))
        self.assertEqual(rn6.numerator, LRN([RNU(s='2'), RNU(s='3[2]√5')]))
        self.assertEqual(rn6.denominator, LRN([RNU(s='3')]))

        self.assertEqual(rn7.numerator, LRN([RNU(s='[2]√2')]))
        self.assertEqual(rn7.denominator, LRN([RNU(s='2')]))
        self.assertEqual(rn8.numerator, LRN([RNU(s='2[2]√6'), RNU(s='-3[2]√3')]))
        self.assertEqual(rn8.denominator, LRN([RNU(s='3')]))

        self.assertEqual(rn9.numerator, LRN([RNU(s='[6]√54'), RNU(s='2[3]√4')]))
        self.assertEqual(rn9.denominator, LRN([RNU(s='2')]))
        self.assertEqual(rn10.numerator, LRN([RNU(s='-1[2]√2'), RNU(s='-1[2]√3')]))
        self.assertEqual(rn10.denominator, LRN([RNU(s='1')]))

        self.assertEqual(rn11.numerator, LRN([RNU(s='-11'), RNU(s='2[2]√30')]))
        self.assertEqual(rn11.denominator, LRN([RNU(s='1')]))
        self.assertEqual(rn12.numerator, LRN([RNU(s='6[6]√4000'), RNU(s='3[6]√32')]))
        self.assertEqual(rn12.denominator, LRN([RNU(s='38')]))

        # test properties
        # test is rational (is irrational)
        self.assertEqual(rn1.is_rational, True)
        self.assertEqual(rn2.is_rational, False)
        self.assertEqual(rn3.is_rational, False)
        self.assertEqual(rn4.is_rational, False)

        self.assertEqual(rn5.is_rational, False)
        self.assertEqual(rn6.is_rational, False)
        self.assertEqual(rn7.is_rational, False)
        self.assertEqual(rn8.is_rational, False)

        self.assertEqual(rn9.is_rational, False)
        self.assertEqual(rn10.is_rational, False)
        self.assertEqual(rn11.is_rational, False)
        self.assertEqual(rn12.is_rational, False)

        # test is integer
        for rn in [rn1, rn2, rn3, rn4, rn5, rn6, rn7, rn8, rn9, rn10, rn11, rn12]:
            self.assertEqual(rn.is_integer, False)

        self.assertEqual(RN(2).is_integer, True)
        self.assertEqual(RN(3).is_integer, True)
        self.assertEqual(RN(4, 2).is_integer, True)
        self.assertEqual(RN(4, 4).is_integer, True)

        # test has num and has den
        self.assertEqual(rn1.has_numerator, True)
        self.assertEqual(rn2.has_numerator, True)
        self.assertEqual(rn3.has_numerator, True)
        self.assertEqual(rn4.has_numerator, True)

        self.assertEqual(rn5.has_numerator, True)
        self.assertEqual(rn6.has_numerator, True)
        self.assertEqual(rn7.has_numerator, True)
        self.assertEqual(rn8.has_numerator, True)

        self.assertEqual(rn9.has_numerator, True)
        self.assertEqual(rn10.has_numerator, True)
        self.assertEqual(rn11.has_numerator, True)
        self.assertEqual(rn12.has_numerator, True)

        self.assertEqual(rn1.has_denominator, True)
        self.assertEqual(rn2.has_denominator, True)
        self.assertEqual(rn3.has_denominator, False)
        self.assertEqual(rn4.has_denominator, True)

        self.assertEqual(rn5.has_denominator, True)
        self.assertEqual(rn6.has_denominator, True)
        self.assertEqual(rn7.has_denominator, True)
        self.assertEqual(rn8.has_denominator, True)

        self.assertEqual(rn9.has_denominator, True)
        self.assertEqual(rn10.has_denominator, False)
        self.assertEqual(rn11.has_denominator, False)
        self.assertEqual(rn12.has_denominator, True)

        # test is rationalized
        for rn in [rn1, rn2, rn3, rn4, rn5, rn6, rn7, rn8, rn9, rn10, rn11, rn12]:
            self.assertEqual(rn.is_rationalized, True)

        # test comparisons
        # RN
        # LRN
        # RNU
        # int
        # float
        # Fraction
        # Decimal

        # test eq
        self.assertEqual(rn1 == RN(1, 2), True)
        self.assertEqual(rn2 == RN(RNU(s='[2]√2')), False)
        self.assertEqual(rn3 == RN(LRN([RNU(s='[2]√3'), RNU(s='-2')])), True)
        self.assertEqual(rn4 == RN(1, 3), False)

        self.assertEqual(rn1 == LRN([RNU(s='2/3')]), False)
        self.assertEqual(rn2 == LRN([RNU(s='1/2[2]√2')]), True)
        self.assertEqual(rn3 == LRN([RNU(s='3/2')]), False)
        self.assertEqual(rn4 == LRN([RNU(s='1/3[2]√2'), RNU(s='-4/3[2]√5')]), True)

        self.assertEqual(rn1 == RNU(s='1/2'), True)
        self.assertEqual(rn2 == RNU(s='1/2[2]√2'), True)
        self.assertEqual(rn3 == RNU(s='[2]√3'), False)
        self.assertEqual(rn4 == RNU(s='1/3[2]√2'), False)

        self.assertEqual(RN(4, 2) == 2, True)
        self.assertEqual(rn1 == 3, False)
        self.assertEqual(RN(7) == 7, True)
        self.assertEqual(rn1 == 8, False)

        self.assertEqual(rn1 == 0.5, True)
        self.assertEqual(rn2 == 0.87, False)
        self.assertEqual(RN(Fraction(3, 4)) == 0.75, True)
        self.assertEqual(rn4 == 1.41, False)

        self.assertEqual(rn1 == Fraction(1, 2), True)
        self.assertEqual(rn2 == Fraction(3, 2), False)
        self.assertEqual(RN(15, 3) == Fraction(15, 3), True)
        self.assertEqual(rn4 == Fraction(13456, 2345), False)

        self.assertEqual(rn1 == Decimal(Decimal(1) / Decimal(2)), True)
        self.assertEqual(rn2 == Decimal(23.5), False)
        self.assertEqual(RN(Decimal(3.4)) == Decimal(3.4), True)
        self.assertEqual(rn4 == Decimal(6.789), False)

        # test operations
        # test neg
        self.assertEqual(-rn1, RN(-2, 4))
        self.assertEqual(-rn2, RN(RNU(s='-2[2]√2'), 4))
        self.assertEqual(-rn3, RN(LRN([RNU(s='-1[2]√3'), RNU(s='2')]), 1))
        self.assertEqual(-rn4, RN(LRN([RNU(s='-1[2]√2'), RNU(s='4[2]√5')]), 3))

        self.assertEqual(-rn7, RN(LRN([RNU(s='-1[2]√2')]), 2))
        self.assertEqual(-rn9, RN(LRN([RNU(s='-1[6]√54'), RNU(s='-2[3]√4')]), 2))
        self.assertEqual(-rn11, RN(LRN([RNU(s='11'), RNU(s='-2[2]√30')]), 1))
        self.assertEqual(-rn12, RN(LRN([RNU(s='-6[6]√4000'), RNU(s='-3[6]√32')]), 38))

        # test add
        self.assertEqual(rn1 + rn4, RN(LRN([RNU(s='3'), RNU(s='2[2]√2'), RNU(s='-8[2]√5')]), 6))
        self.assertEqual(rn2 + rn8, RN(LRN([RNU(s='3[2]√2'), RNU(s='4[2]√6'), RNU(s='-6[2]√3')]), 6))
        self.assertEqual(rn3 + rn12, RN(LRN([RNU(s='38[2]√3'), RNU(s='-76'), RNU(s='6[6]√4000'), RNU(s='3[6]√32')]),
                                        38))

        self.assertEqual(rn4 + rn3, RN(LRN([RNU(s='[2]√2'), RNU(s='-4[2]√5'), RNU(s='3[2]√3'), RNU(s='-6')]), 3))
        self.assertEqual(rn5 + rn9, RN(LRN([RNU(s='8[2]√3'), RNU(s='-20[2]√10'), RNU(s='3[6]√54'), RNU(s='6[3]√4')]),
                                       6))
        self.assertEqual(rn6 + rn10, RN(LRN([RNU(s='2'), RNU(s='3[2]√5'), RNU(s='-3[2]√2'), RNU(s='-3[2]√3')]), 3))

        # test sub
        # -> tested in neg and add

        # test mul
        self.assertEqual(rn1 * rn6, RN(LRN([RNU(s='2'), RNU(s='3[2]√5')]), 6))
        self.assertEqual(rn2 * rn7, RN(1, 2))
        self.assertEqual(rn3 * rn11, RN(LRN([RNU(s='6[2]√10'), RNU(s='-11[2]√3'), RNU(s='-4[2]√30'), RNU(s='22')])))

        self.assertEqual(rn4 * rn3, RN(LRN([RNU(s='[2]√6'), RNU(s='-2[2]√2'), RNU(s='-4[2]√15'), RNU(s='8[2]√5')]), 3))
        self.assertEqual(rn5 * rn8, RN(LRN([RNU(s='24[2]√2'), RNU(s='-36'), RNU(s='-40[2]√15'), RNU(s='30[2]√30')]),
                                       9))
        self.assertEqual(rn6 * rn9, RN(LRN([RNU(s='2[6]√54'), RNU(s='4[3]√4'), RNU(s='3[6]√6750'),
                                            RNU(s='6[6]√2000')]), 6))

        # test truediv
        self.assertEqual(rn1 / rn6, RN(3, LRN([RNU(s='4'), RNU(s='6[2]√5')])))
        self.assertEqual(rn2 / rn9, RN(RNU(s='[2]√2'), LRN([RNU(s='[6]√54'), RNU(s='2[3]√4')])))
        self.assertEqual(rn3 / rn12, RN(LRN([RNU(s='38[2]√3'), RNU(s='-76')]), LRN([RNU(s='6[6]√4000'),
                                                                                    RNU(s='3[6]√32')])))

        self.assertEqual(rn4 / rn2, RN(LRN([RNU(s='2'), RNU(s='-4[2]√10')]), 3))
        self.assertEqual(rn5 / rn7, RN(LRN([RNU(s='4[2]√6'), RNU(s='-20[2]√5')]), 3))
        self.assertEqual(rn6 / rn10, RN(LRN([RNU(s='2[2]√2'), RNU(s='-2[2]√3'), RNU(s='3[2]√10'),
                                             RNU(s='-3[2]√15')]), 3))

        # test floordiv
        self.assertEqual(rn1 // rn6, RN(0))
        self.assertEqual(rn2 // rn9, RN(0))
        self.assertEqual(rn3 // rn12, RN(0))

        self.assertEqual(rn4 // rn2, RN(-3))
        self.assertEqual(rn5 // rn7, RN(-11))
        self.assertEqual(rn6 // rn10, RN(0))

        # test mod
        self.assertEqual(rn1 % rn6, rn1)
        self.assertEqual(rn2 % rn9, rn2)
        self.assertEqual(rn3 % rn12, rn3)

        self.assertEqual(rn4 % rn2, RN(LRN([RNU(s='11[2]√2'), RNU(s='-8[2]√5')]), 6))
        self.assertEqual(rn5 % rn7, RN(LRN([RNU(s='33[2]√2'), RNU(s='8[2]√3'), RNU(s='-20[2]√10')]), 6))
        self.assertEqual(rn6 % rn10, rn6)

        # test pow
        self.assertEqual(rn1 ** RN(2), RN(1, 4))
        self.assertEqual(rn2 ** RN(2), RN(1, 2))
        self.assertEqual(rn3 ** RN(2), RN(LRN([RNU(s='7'), RNU(s='-4[2]√3')])))

        self.assertEqual(rn4 ** RN(2), RN(LRN([RNU(s='82'), RNU(s='-8[2]√10')]), 9))
        self.assertEqual(rn5 ** RN(2), RN(LRN([RNU(s='1048'), RNU(s='-80[2]√30')]), 9))
        self.assertEqual(rn6 ** RN(2), RN(LRN([RNU(s='49'), RNU(s='12[2]√5')]), 9))

        # test sqrt
        self.assertEqual(rn1.sqrt(), RN(RNU(s='1[2]√2'), 2))
        self.assertEqual(RN(4).sqrt(), 2)
        # self.assertEqual()

        self.assertEqual(rn7.sqrt(), RN(RNU(s='1[4]√2'), RNU(s='1[2]√2')))
        # self.assertEqual()
        # self.assertEqual()

        # test abs
        for rn in [rn1, rn2, rn3, rn4, rn5, rn6, rn7, rn8, rn9, rn10, rn11, rn12]:
            if float(rn) < 0:
                self.assertEqual(abs(rn), -rn)
            else:
                self.assertEqual(abs(rn), rn)

        # test r-operations
        # LRN
        # RNU
        # int
        # float
        # Fraction
        # Decimal

        rn13 = RN(LRN([RNU(s='[2]√2'), RNU(s='8')]), 2)
        rn14 = RN(LRN([RNU(s='8'), RNU(s='-1[2]√2')]), 2)
        rn15 = RN(RNU(s='2[2]√2'))
        rn16 = RN(RNU(s='4[2]√2'))
        rn17 = RN(5)
        rn18 = RN(LRN([RNU(s='8'), RNU(s='-5[2]√2')]), 2)
        rn19 = RN(16)

        # test r-add
        self.assertEqual(LRN([RNU(s='4')]) + rn2, rn13)
        self.assertEqual(RNU(s='4') + rn2, rn13)
        self.assertEqual(int(4) + rn2, rn13)
        self.assertEqual(float(4) + rn2, rn13)
        self.assertEqual(Fraction(4) + rn2, rn13)
        self.assertEqual(Decimal(4) + rn2, rn13)

        # test r-sub
        self.assertEqual(LRN([RNU(s='4')]) - rn2, rn14)
        self.assertEqual(RNU(s='4') - rn2, rn14)
        self.assertEqual(int(4) - rn2, rn14)
        self.assertEqual(float(4) - rn2, rn14)
        self.assertEqual(Fraction(4) - rn2, rn14)
        self.assertEqual(Decimal(4) - rn2, rn14)

        # test r-mul
        self.assertEqual(LRN([RNU(s='4')]) * rn2, rn15)
        self.assertEqual(RNU(s='4') * rn2, rn15)
        self.assertEqual(int(4) * rn2, rn15)
        self.assertEqual(float(4) * rn2, rn15)
        self.assertEqual(Fraction(4) * rn2, rn15)
        self.assertEqual(Decimal(4) * rn2, rn15)

        # test r-truediv
        self.assertEqual(LRN([RNU(s='4')]) / rn2, rn16)
        self.assertEqual(RNU(s='4') / rn2, rn16)
        self.assertEqual(int(4) / rn2, rn16)
        self.assertEqual(float(4) / rn2, rn16)
        self.assertEqual(Fraction(4) / rn2, rn16)
        self.assertEqual(Decimal(4) / rn2, rn16)

        # test r-floordiv
        self.assertEqual(LRN([RNU(s='4')]) // rn2, rn17)
        self.assertEqual(RNU(s='4') // rn2, rn17)
        self.assertEqual(int(4) // rn2, rn17)
        self.assertEqual(float(4) // rn2, rn17)
        self.assertEqual(Fraction(4) // rn2, rn17)
        self.assertEqual(Decimal(4) // rn2, rn17)

        # test r-mod
        self.assertEqual(LRN([RNU(s='4')]) % rn2, rn18)
        self.assertEqual(RNU(s='4') % rn2, rn18)
        self.assertEqual(int(4) % rn2, rn18)
        self.assertEqual(float(4) % rn2, rn18)
        self.assertEqual(Fraction(4) % rn2, rn18)
        self.assertEqual(Decimal(4) % rn2, rn18)

        # test r-pow
        self.assertEqual(LRN([RNU(s='4')]) ** RN(2), rn19)
        self.assertEqual(RNU(s='4') ** RN(2), rn19)
        self.assertEqual(int(4) ** RN(2), rn19)
        self.assertEqual(float(4) ** RN(2), rn19)
        self.assertEqual(Fraction(4) ** RN(2), rn19)
        self.assertEqual(Decimal(4) ** RN(2), rn19)


if __name__ == '__main__':
    unittest.main()
