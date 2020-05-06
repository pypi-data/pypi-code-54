
import unittest

from fractions import Fraction
from decimal import Decimal

from .pn import PN, LPN, Tr, ML, Li, tr, lpn, pn, _Lcl
from ..rn.rn import RN, LRN, RNU, Ra, Ir


# terms
tr1 = Tr(-3)
tr2 = Tr(Fraction(5, 7))
tr3 = Tr(RN(RNU(s='[2]√3')))
tr4 = Tr(RN(RNU(s='4[2]√5'), 5))
tr5 = Tr(-4, ML([Li('x', 2)]))
tr6 = Tr(Fraction(5, 2), ML([Li('x', 1), Li('y', 3)]))
tr7 = Tr(Fraction(3, 10), ML([Li('x', 10)]))
tr8 = Tr(16, ML([Li('y', 4)]))
tr9 = Tr(RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)]))
tr10 = Tr(RN(RNU(s='[3]√4')), ML([Li('y', 5)]))
tr11 = Tr(RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10)]))
tr12 = Tr(RN(RNU(s='[5]√162')), ML([Li('y', 5)]))


# linear polynomials
pn1 = LPN([tr1, tr3])
pn2 = LPN([tr2, tr5])
pn3 = LPN([tr3, tr8])
pn4 = LPN([tr4, tr11])
pn5 = LPN([tr5, tr6, tr9])
pn6 = LPN([tr6, tr6, tr12])
pn7 = LPN([tr7, tr11, tr8])
pn8 = LPN([tr8, tr9, tr8])
pn9 = LPN([tr9, tr6, tr1])
pn10 = LPN([tr10, tr3, tr4, tr12])
pn11 = LPN([tr11, tr9, tr6, tr2])
pn12 = LPN([tr12, tr4, tr10, tr6])


class TestPN(unittest.TestCase):
    def test_Tr(self):
        terms = [tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8, tr9, tr10, tr11, tr12]

        # test properties
        # test bool
        for term in terms:
            self.assertEqual(bool(term), True)
        self.assertEqual(bool(Tr(0)), False)

        # test degree
        self.assertEqual(tr1.degree, 0)
        self.assertEqual(tr2.degree, 0)
        self.assertEqual(tr3.degree, 0)
        self.assertEqual(tr4.degree, 0)

        self.assertEqual(tr5.degree, 2)
        self.assertEqual(tr6.degree, 4)
        self.assertEqual(tr7.degree, 10)
        self.assertEqual(tr8.degree, 4)

        self.assertEqual(tr9.degree, 4)
        self.assertEqual(tr10.degree, 5)
        self.assertEqual(tr11.degree, 10)
        self.assertEqual(tr12.degree, 5)

        # test variable degree
        self.assertEqual(tr5.variable_degree('x'), 2)
        self.assertEqual(tr6.variable_degree('y'), 3)
        self.assertEqual(tr7.variable_degree('x'), 10)
        self.assertEqual(tr8.variable_degree('y'), 4)

        self.assertEqual(tr9.variable_degree('x'), 1)
        self.assertEqual(tr10.variable_degree('y'), 5)
        self.assertEqual(tr11.variable_degree('x'), 10)
        self.assertEqual(tr12.variable_degree('y'), 5)

        # test is constant
        self.assertEqual(tr1.is_constant, True)
        self.assertEqual(tr2.is_constant, True)
        self.assertEqual(tr3.is_constant, True)
        self.assertEqual(tr4.is_constant, True)

        self.assertEqual(tr5.is_constant, False)
        self.assertEqual(tr6.is_constant, False)
        self.assertEqual(tr7.is_constant, False)
        self.assertEqual(tr8.is_constant, False)

        self.assertEqual(tr9.is_constant, False)
        self.assertEqual(tr10.is_constant, False)
        self.assertEqual(tr11.is_constant, False)
        self.assertEqual(tr12.is_constant, False)

        # test is integer
        self.assertEqual(tr1.is_integer, True)
        self.assertEqual(tr2.is_integer, False)
        self.assertEqual(tr3.is_integer, False)
        self.assertEqual(tr4.is_integer, False)

        self.assertEqual(tr5.is_integer, False)
        self.assertEqual(tr6.is_integer, False)
        self.assertEqual(tr7.is_integer, False)
        self.assertEqual(tr8.is_integer, False)

        self.assertEqual(tr9.is_integer, False)
        self.assertEqual(tr10.is_integer, False)
        self.assertEqual(tr11.is_integer, False)
        self.assertEqual(tr12.is_integer, False)

        # test parameters
        self.assertEqual(tr1.parameters, set())
        self.assertEqual(tr2.parameters, set())
        self.assertEqual(tr3.parameters, set())
        self.assertEqual(tr4.parameters, set())

        self.assertEqual(tr5.parameters, {'x'})
        self.assertEqual(tr6.parameters, {'x', 'y'})
        self.assertEqual(tr7.parameters, {'x'})
        self.assertEqual(tr8.parameters, {'y'})

        self.assertEqual(tr9.parameters, {'x', 'y'})
        self.assertEqual(tr10.parameters, {'y'})
        self.assertEqual(tr11.parameters, {'x'})
        self.assertEqual(tr12.parameters, {'y'})

        # test has_rational_coefficient
        self.assertEqual(tr1.has_rational_coefficient, True)
        self.assertEqual(tr2.has_rational_coefficient, True)
        self.assertEqual(tr3.has_rational_coefficient, False)
        self.assertEqual(tr4.has_rational_coefficient, False)

        self.assertEqual(tr5.has_rational_coefficient, True)
        self.assertEqual(tr6.has_rational_coefficient, True)
        self.assertEqual(tr7.has_rational_coefficient, True)
        self.assertEqual(tr8.has_rational_coefficient, True)

        self.assertEqual(tr9.has_rational_coefficient, False)
        self.assertEqual(tr10.has_rational_coefficient, False)
        self.assertEqual(tr11.has_rational_coefficient, False)
        self.assertEqual(tr12.has_rational_coefficient, False)

        # test is perfect square
        self.assertEqual(tr('4x2').is_perfect_square, True)
        self.assertEqual(tr('6x4').is_perfect_square, False)
        self.assertEqual(tr('1y2x4').is_perfect_square, True)
        self.assertEqual(tr('3x6y3').is_perfect_square, False)

        self.assertEqual(tr9.is_perfect_square, False)
        self.assertEqual(tr10.is_perfect_square, False)
        self.assertEqual(tr11.is_perfect_square, False)
        self.assertEqual(tr12.is_perfect_square, False)

        self.assertEqual(tr('81x4y7').is_perfect_square, False)
        self.assertEqual(tr('121x4z6').is_perfect_square, True)
        self.assertEqual(tr('25x1').is_perfect_square, False)
        self.assertEqual(tr('4x6y2').is_perfect_square, True)

        # test is perfect cube
        self.assertEqual(tr('8x3').is_perfect_cube, True)
        self.assertEqual(tr('6x6').is_perfect_cube, False)
        self.assertEqual(tr('1y3x6').is_perfect_cube, True)
        self.assertEqual(tr('3x6y3').is_perfect_cube, False)

        self.assertEqual(tr9.is_perfect_cube, False)
        self.assertEqual(tr10.is_perfect_cube, False)
        self.assertEqual(tr11.is_perfect_cube, False)
        self.assertEqual(tr12.is_perfect_cube, False)

        self.assertEqual(tr('27x6y5').is_perfect_cube, False)
        self.assertEqual(tr('64x6z9').is_perfect_cube, True)
        self.assertEqual(tr('125x1').is_perfect_cube, False)
        self.assertEqual(tr('8x9y3').is_perfect_cube, True)

        # test comparisons
        # test eq
        self.assertEqual(tr1 == Tr(Fraction(-6, 2)), True)
        self.assertEqual(tr2 == Tr(Fraction(5, 6)), False)
        self.assertEqual(tr3 == Tr(RN(RNU(s='[4]√9'))), True)
        self.assertEqual(tr4 == Tr(RN(3, 5)), False)

        self.assertEqual(tr5 == Tr(-4, ML([Li('x', 1), Li('x', 1)])), True)
        self.assertEqual(tr6 == Tr(Fraction(5, 3), ML([Li('x', 2), Li('y', 3)])), False)
        self.assertEqual(tr7 == Tr(Fraction(3, 10), ML([Li('x', 10)])), True)
        self.assertEqual(tr8 == Tr(16, ML([Li('z', 4)])), False)

        self.assertEqual(tr9 == Tr(RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 2), Li('y', 1)])), True)
        self.assertEqual(tr10 == Tr(RN(RNU(s='[2]√2')), ML([Li('y', 3)])), False)
        self.assertEqual(tr11 == Tr(RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10), Li('z', 0)])), True)
        self.assertEqual(tr12 == Tr(RN(RNU(s='[6]√162')), ML([Li('y', 5)])), False)

        # test operations
        # test is compatible
        self.assertEqual(tr1.is_compatible(tr2), True)
        self.assertEqual(tr1.is_compatible(tr6), False)
        self.assertEqual(tr1.is_compatible(tr10), False)
        self.assertEqual(tr1.is_compatible(tr12), False)

        self.assertEqual(tr5.is_compatible(tr2), False)
        self.assertEqual(tr5.is_compatible(tr8), False)
        self.assertEqual(tr5.is_compatible(tr9), False)
        self.assertEqual(tr5.is_compatible(tr11), False)

        self.assertEqual(tr11.is_compatible(tr4), False)
        self.assertEqual(tr11.is_compatible(tr7), True)
        self.assertEqual(tr11.is_compatible(tr9), False)
        self.assertEqual(tr11.is_compatible(tr11), True)

        # test is divisible
        self.assertEqual(tr1.is_divisible(tr2), True)
        self.assertEqual(tr1.is_divisible(tr6), False)
        self.assertEqual(tr1.is_divisible(tr10), False)
        self.assertEqual(tr1.is_divisible(tr12), False)

        self.assertEqual(tr5.is_divisible(tr2), True)
        self.assertEqual(tr5.is_divisible(tr8), False)
        self.assertEqual(tr5.is_divisible(tr9), False)
        self.assertEqual(tr5.is_divisible(tr11), False)

        self.assertEqual(tr11.is_divisible(tr4), True)
        self.assertEqual(tr11.is_divisible(tr5), True)
        self.assertEqual(tr11.is_divisible(tr9), False)
        self.assertEqual(tr11.is_divisible(tr11), True)

        # test add
        self.assertEqual(tr1 + tr3, Tr(RN(RNU(s='[2]√3')) - 3))
        # self.assertEqual(tr2 + tr7, NotImplemented)
        # self.assertEqual(tr3 + tr11, NotImplemented)

        self.assertEqual(tr1 + 4, Tr(1))
        self.assertEqual(tr2 + Fraction(2, 5), Tr(Fraction(39, 35)))
        self.assertEqual(tr3 + RN(RNU(s='[2]√3')), Tr(RN(RNU(s='2[2]√3'))))
        self.assertEqual(tr4 + 5.0, Tr(RN(RNU(s='4[2]√5'), 5) + Fraction(5, 1)))

        # self.assertEqual(tr5 + tr2, NotImplemented)
        # self.assertEqual(tr6 + tr8, NotImplemented)
        self.assertEqual(tr7 + tr11, Tr(RN(3, 10) + RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10)])))

        self.assertEqual(tr9 + tr6, Tr(RN(5, 2) + RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)])))
        # self.assertEqual(tr10 + tr7, NotImplemented)
        self.assertEqual(tr12 + tr10, Tr(RN(RNU(s='[3]√4')) + RN(RNU(s='[5]√162')), ML([Li('y', 5)])))

        # test sub
        self.assertEqual(tr1 - tr3, Tr(-RN(RNU(s='[2]√3')) - 3))
        # self.assertEqual(tr2 - tr7, NotImplemented)
        # self.assertEqual(tr3 - tr11, NotImplemented)

        self.assertEqual(tr1 - 4, Tr(-7))
        self.assertEqual(tr2 - Fraction(2, 5), Tr(Fraction(11, 35)))
        self.assertEqual(tr3 - RN(RNU(s='[2]√3')), Tr(RN(0)))
        self.assertEqual(tr4 - 5.0, Tr(RN(RNU(s='4[2]√5'), 5) - Fraction(5, 1)))

        # self.assertEqual(tr5 - tr2, NotImplemented)
        # self.assertEqual(tr6 - tr8, NotImplemented)
        self.assertEqual(tr7 - tr11, Tr(RN(3, 10) - RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10)])))

        self.assertEqual(tr9 - tr6, Tr(-RN(5, 2) + RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)])))
        # self.assertEqual(tr10 - tr7, NotImplemented)
        self.assertEqual(tr12 - tr10, Tr(-RN(RNU(s='[3]√4')) + RN(RNU(s='[5]√162')), ML([Li('y', 5)])))

        # test mul
        self.assertEqual(tr1 * tr3, Tr(RN(RNU(s='-3[2]√3'))))
        self.assertEqual(tr2 * tr7, Tr(Fraction(3, 14), ML([Li('x', 10)])))
        self.assertEqual(tr3 * tr11, Tr(RN(RNU(s='5[2]√6'), 4), ML([Li('x', 10)])))

        self.assertEqual(tr1 * 4, Tr(-12))
        self.assertEqual(tr2 * Fraction(2, 5), Tr(Fraction(2, 7)))
        self.assertEqual(tr3 * RN(RNU(s='[2]√3')), Tr(3))
        self.assertEqual(tr4 * 5.0, Tr(RN(RNU(s='20[2]√5'), 5)))

        self.assertEqual(tr5 * tr2, Tr(Fraction(-20, 7), ML([Li('x', 2)])))
        self.assertEqual(tr6 * tr8, Tr(40, ML([Li('x', 1), Li('y', 7)])))
        self.assertEqual(tr7 * tr11, Tr(RN(RNU(s='3[2]√2'), 8), ML([Li('x', 20)])))

        self.assertEqual(tr5 * 4, Tr(-16, ML([Li('x', 2)])))
        self.assertEqual(tr6 * Fraction(2, 5), Tr(1, ML([Li('x', 1), Li('y', 3)])))
        self.assertEqual(tr7 * RN(RNU(s='[2]√3')), Tr(RN(RNU(s='3[2]√3'), 10), ML([Li('x', 10)])))
        self.assertEqual(tr8 * 5.0, Tr(80, ML([Li('y', 4)])))

        self.assertEqual(tr9 * tr6, Tr(RN(RNU(s='5[2]√2'), 2), ML([Li('x', 2), Li('y', 6)])))
        self.assertEqual(tr10 * tr7, Tr(RN(RNU(s='3[3]√4'), 10), ML([Li('x', 10), Li('y', 5)])))
        self.assertEqual(tr12 * tr10, Tr(RN(RNU(s='[5]√162')) * RN(RNU(s='[3]√4')), ML([Li('y', 10)])))

        self.assertEqual(tr9 * 4, Tr(RN(RNU(s='4[2]√2')), ML([Li('x', 1), Li('y', 3)])))
        self.assertEqual(tr10 * Fraction(2, 5), Tr(RN(RNU(s='2[3]√4'), 5), ML([Li('y', 5)])))
        self.assertEqual(tr11 * RN(RNU(s='[2]√3')), Tr(RN(RNU(s='5[2]√6'), 4), ML([Li('x', 10)])))
        self.assertEqual(tr12 * 5.0, Tr(RN(RNU(s='5[5]√162')), ML([Li('y', 5)])))

        # test truediv
        self.assertEqual(tr1 / tr4, Tr(RN(RNU(s='-3[2]√5'), 4)))
        self.assertEqual(tr2 / tr2, Tr(1))
        self.assertEqual(tr3 / tr1, Tr(RN(RNU(s='-1[2]√3'), 3)))
        self.assertEqual(tr4 / tr3, Tr(RN(RNU(s='4[2]√15'), 15)))

        self.assertEqual(tr5 / tr1, Tr(Fraction(4, 3), ML([Li('x', 2)])))
        self.assertEqual(tr6 / tr9, Tr(RN(RNU(s='5[2]√2'), 4)))
        self.assertEqual(tr7 / tr5, Tr(Fraction(-3, 40), ML([Li('x', 8)])))
        self.assertEqual(tr8 / tr4, Tr(RN(RNU(s='4[2]√5')), ML([Li('y', 4)])))

        self.assertEqual(tr9 / tr6, Tr(RN(RNU(s='2[2]√2'), 5)))
        self.assertEqual(tr10 / tr8, Tr(RN(RNU(s='[3]√4'), 16), ML([Li('y', 1)])))
        self.assertEqual(tr11 / tr5, Tr(RN(RNU(s='-5[2]√2'), 16), ML([Li('x', 8)])))
        self.assertEqual(tr12 / tr10, Tr(RN(RNU(s='[5]√162')) / RN(RNU(s='[3]√4'))))

        # test r-operations
        # test for:
        # - RN
        # - int
        # - float
        # - Fraction
        # - Decimal
        # test r-add
        self.assertEqual(RN(4) + tr1, Tr())
        self.assertEqual(4 + tr1, Tr())
        self.assertEqual(4.0 + tr1, Tr())
        self.assertEqual(Fraction(4) + tr1, Tr())
        self.assertEqual(Decimal(4) + tr1, Tr())

        # test r-sub
        self.assertEqual(RN(4) - tr1, Tr(7))
        self.assertEqual(4 - tr1, Tr(7))
        self.assertEqual(4.0 - tr1, Tr(7))
        self.assertEqual(Fraction(4) - tr1, Tr(7))
        self.assertEqual(Decimal(4) - tr1, Tr(7))

        # test r-mul
        self.assertEqual(RN(4) * tr1, Tr(-12))
        self.assertEqual(4 * tr1, Tr(-12))
        self.assertEqual(4.0 * tr1, Tr(-12))
        self.assertEqual(Fraction(4) * tr1, Tr(-12))
        self.assertEqual(Decimal(4) * tr1, Tr(-12))

        # test GCD
        self.assertEqual(Tr(3, ML([Li('x', 2), Li('y', 1)])).GCD(Tr(15, ML([Li('a', 3), Li('x', 2)]))),
                         Tr(3, ML([Li('x', 2)])))
        self.assertEqual(Tr(Fraction(1, 4), ML([Li('a', 1), Li('b', 2), Li('x', 1)])).GCD(Tr(Fraction(-2, 3),
                                                                                             ML([Li('a', 2), Li('b', 1),
                                                                                                 Li('x', 3)]))),
                         Tr(1, ML([Li('a', 1), Li('b', 1), Li('x', 1)])))
        self.assertEqual(Tr(2, ML([Li('a', 2), Li('x', 1)])).GCD(Tr(4, ML([Li('a', 1), Li('x', 3)]))),
                         Tr(2, ML([Li('a', 1), Li('x', 1)])))
        self.assertEqual(Tr(4, ML([Li('a', 3), Li('b', 1), Li('c', 2)])).GCD(Tr(16, ML([Li('a', 1), Li('c', 3)]))),
                         Tr(4, ML([Li('a', 1), Li('c', 2)])))

        # test eval_to
        self.assertEqual(tr1.eval_to({}), -3)
        self.assertEqual(tr4.eval_to({}), RN(RNU(s='4[2]√5'), 5))
        self.assertEqual(tr5.eval_to({'x': 3}), -36)
        self.assertEqual(tr9.eval_to({'x': RN(RNU(s='[2]√2')), 'y': 2}), 16)
        self.assertEqual(tr11.eval_to({'x': 1}), RN(RNU(s='5[2]√2'), 4))

    def test_LPN(self):
        polynomials = [pn1, pn2, pn3, pn4, pn5, pn6, pn7, pn8, pn9, pn10, pn11, pn12]

        # test init
        self.assertEqual(pn1.terms, [Tr(RN(RNU(s='[2]√3')) + RN(RNU(s='-3')))])
        self.assertEqual(pn2.terms, [Tr(Fraction(5, 7)), Tr(-4, ML([Li('x', 2)]))])
        self.assertEqual(pn3.terms, [Tr(RN(RNU(s='[2]√3'))), Tr(16, ML([Li('y', 4)]))])
        self.assertEqual(pn4.terms, [Tr(RN(RNU(s='4[2]√5'), 5)), Tr(RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10)]))])

        self.assertEqual(pn5.terms, sorted([Tr(-4, ML([Li('x', 2)])),
                                            Tr(RN(5, 2) + RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)]))]))
        self.assertEqual(pn6.terms, sorted([Tr(RN(RNU(s='[5]√162')), ML([Li('y', 5)])),
                                            Tr(5, ML([Li('x', 1), Li('y', 3)]))]))
        self.assertEqual(pn7.terms, sorted([Tr(RN(3, 10) + RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10)])),
                                            Tr(16, ML([Li('y', 4)]))]))
        self.assertEqual(pn8.terms, sorted([Tr(32, ML([Li('y', 4)])),
                                            Tr(RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)]))]))

        self.assertEqual(pn9.terms, sorted([Tr(RN(5, 2) + RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)])),
                                            Tr(-3)]))
        self.assertEqual(pn10.terms, sorted([Tr(RN(RNU(s='[3]√4')) + RN(RNU(s='[5]√162')), ML([Li('y', 5)])),
                                             Tr(RN(RNU(s='4/5[2]√5')) + RN(RNU(s='[2]√3')))]))
        self.assertEqual(pn11.terms, sorted([Tr(RN(5, 2) + RN(RNU(s='[2]√2')), ML([Li('x', 1), Li('y', 3)])),
                                             Tr(RN(RNU(s='5[2]√2'), 4), ML([Li('x', 10)])), Tr(Fraction(5, 7))]))
        self.assertEqual(pn12.terms, sorted([Tr(RN(RNU(s='[3]√4')) + RN(RNU(s='[5]√162')), ML([Li('y', 5)])),
                                             Tr(Fraction(5, 2), ML([Li('x', 1), Li('y', 3)])),
                                             Tr(RN(RNU(s='4[2]√5'), 5))]))

        # test properties
        # test degree
        self.assertEqual(pn1.degree, 0)
        self.assertEqual(pn2.degree, 2)
        self.assertEqual(pn3.degree, 4)
        self.assertEqual(pn4.degree, 10)

        self.assertEqual(pn5.degree, 4)
        self.assertEqual(pn6.degree, 5)
        self.assertEqual(pn7.degree, 10)
        self.assertEqual(pn8.degree, 4)

        self.assertEqual(pn9.degree, 4)
        self.assertEqual(pn10.degree, 5)
        self.assertEqual(pn11.degree, 10)
        self.assertEqual(pn12.degree, 5)

        # test variable degree
        self.assertEqual(pn2.variable_degree('x'), 2)
        self.assertEqual(pn3.variable_degree('y'), 4)
        self.assertEqual(pn4.variable_degree('x'), 10)
        self.assertEqual(pn5.variable_degree('x'), 2)

        self.assertEqual(pn6.variable_degree('x'), 1)
        self.assertEqual(pn7.variable_degree('x'), 10)
        self.assertEqual(pn8.variable_degree('x'), 1)
        self.assertEqual(pn9.variable_degree('x'), 1)

        self.assertEqual(pn10.variable_degree('y'), 5)
        self.assertEqual(pn11.variable_degree('x'), 10)
        self.assertEqual(pn11.variable_degree('y'), 3)
        self.assertEqual(pn12.variable_degree('y'), 5)

        # test is constant
        self.assertEqual(pn1.is_constant, True)
        self.assertEqual(pn2.is_constant, False)
        self.assertEqual(pn3.is_constant, False)
        self.assertEqual(pn4.is_constant, False)

        self.assertEqual(pn5.is_constant, False)
        self.assertEqual(pn6.is_constant, False)
        self.assertEqual(pn7.is_constant, False)
        self.assertEqual(pn8.is_constant, False)

        self.assertEqual(pn9.is_constant, False)
        self.assertEqual(pn10.is_constant, False)
        self.assertEqual(pn11.is_constant, False)
        self.assertEqual(pn12.is_constant, False)

        # test is integer
        self.assertEqual(LPN([2, 5]).is_integer, True)
        self.assertEqual(pn1.is_integer, False)
        self.assertEqual(pn2.is_integer, False)
        self.assertEqual(pn3.is_integer, False)

        self.assertEqual(pn5.is_integer, False)
        self.assertEqual(pn6.is_integer, False)
        self.assertEqual(pn7.is_integer, False)
        self.assertEqual(pn8.is_integer, False)

        self.assertEqual(pn9.is_integer, False)
        self.assertEqual(pn10.is_integer, False)
        self.assertEqual(pn11.is_integer, False)
        self.assertEqual(pn12.is_integer, False)

        # test parameters
        self.assertEqual(pn1.parameters, set())
        self.assertEqual(pn2.parameters, {'x'})
        self.assertEqual(pn3.parameters, {'y'})
        self.assertEqual(pn4.parameters, {'x'})

        self.assertEqual(pn5.parameters, {'x', 'y'})
        self.assertEqual(pn6.parameters, {'x', 'y'})
        self.assertEqual(pn7.parameters, {'x', 'y'})
        self.assertEqual(pn8.parameters, {'x', 'y'})

        self.assertEqual(pn9.parameters, {'x', 'y'})
        self.assertEqual(pn10.parameters, {'y'})
        self.assertEqual(pn11.parameters, {'x', 'y'})
        self.assertEqual(pn12.parameters, {'x', 'y'})

        # test is mono variable
        self.assertEqual(pn1.is_mono_variable, False)
        self.assertEqual(pn2.is_mono_variable, True)
        self.assertEqual(pn3.is_mono_variable, True)
        self.assertEqual(pn4.is_mono_variable, True)

        self.assertEqual(pn5.is_mono_variable, False)
        self.assertEqual(pn6.is_mono_variable, False)
        self.assertEqual(pn7.is_mono_variable, False)
        self.assertEqual(pn8.is_mono_variable, False)

        self.assertEqual(pn9.is_mono_variable, False)
        self.assertEqual(pn10.is_mono_variable, True)
        self.assertEqual(pn11.is_mono_variable, False)
        self.assertEqual(pn12.is_mono_variable, False)

        # test has rational coefficients
        self.assertEqual(pn1.has_rational_coefficients, False)
        self.assertEqual(pn2.has_rational_coefficients, True)
        self.assertEqual(pn3.has_rational_coefficients, False)
        self.assertEqual(pn4.has_rational_coefficients, False)

        self.assertEqual(pn5.has_rational_coefficients, False)
        self.assertEqual(pn6.has_rational_coefficients, False)
        self.assertEqual(pn7.has_rational_coefficients, False)
        self.assertEqual(pn8.has_rational_coefficients, False)

        self.assertEqual(pn9.has_rational_coefficients, False)
        self.assertEqual(pn10.has_rational_coefficients, False)
        self.assertEqual(pn11.has_rational_coefficients, False)
        self.assertEqual(pn12.has_rational_coefficients, False)

        # test denominators_LCM
        self.assertEqual(pn1.denominators_LCM, 1)
        self.assertEqual(pn2.denominators_LCM, 7)
        self.assertEqual(pn3.denominators_LCM, 1)
        self.assertEqual(pn4.denominators_LCM, 20)

        self.assertEqual(pn5.denominators_LCM, 2)
        self.assertEqual(pn6.denominators_LCM, 1)
        self.assertEqual(pn7.denominators_LCM, 20)
        self.assertEqual(pn8.denominators_LCM, 1)

        self.assertEqual(pn9.denominators_LCM, 2)
        self.assertEqual(pn10.denominators_LCM, 5)
        self.assertEqual(pn11.denominators_LCM, 28)
        self.assertEqual(pn12.denominators_LCM, 10)

        # test terms_GCD
        self.assertEqual(pn1.terms_GCD, pn1.terms[0])
        self.assertEqual(pn2.terms_GCD, Tr(1))
        self.assertEqual(pn3.terms_GCD, Tr(1))
        self.assertEqual(pn4.terms_GCD, Tr(1))

        self.assertEqual(pn5.terms_GCD, Tr(1, ML([Li('x', 1)])))
        self.assertEqual(pn6.terms_GCD, Tr(1, ML([Li('y', 3)])))
        self.assertEqual(pn7.terms_GCD, Tr(1))
        self.assertEqual(pn8.terms_GCD, Tr(1, ML([Li('y', 3)])))

        self.assertEqual(pn9.terms_GCD, Tr(1))
        self.assertEqual(pn10.terms_GCD, Tr(1))
        self.assertEqual(pn11.terms_GCD, Tr(1))
        self.assertEqual(pn12.terms_GCD, Tr(1))

        # test complete and ordered
        self.assertEqual(pn2.complete_and_ordered('x'), [tr5, Tr(0, ML([Li('x', 1)])), tr2])
        self.assertEqual(pn3.complete_and_ordered('y'), [tr8, Tr(0, ML([Li('y', 3)])), Tr(0, ML([Li('y', 2)])),
                                                         Tr(0, ML([Li('y', 1)])), tr3])
        self.assertEqual(pn5.complete_and_ordered('x'), [tr5, tr6 + tr9, Tr(0)])
        self.assertEqual(pn9.complete_and_ordered('y'), [tr6 + tr9, Tr(0, ML([Li('y', 2)])), Tr(0, ML([Li('y', 1)])),
                                                         tr1])

        # test comparisons

        # test operations
        # test add
        self.assertEqual(LPN([tr('3x3'), tr('-4y2')]) + LPN([tr('5y2'), tr('-4x3')]), LPN([tr('1y2'), tr('-1x3')]))
        self.assertEqual(LPN([tr('-4x5')]) + LPN([tr('4x5')]), LPN([0]))

        # test neg
        for _pn in polynomials:
            self.assertEqual((-_pn).terms, [-term for term in _pn.terms])

        # test sub
        self.assertEqual(LPN([tr('1b3'), tr('-2a2b1'), tr('-3a1b2')]) - LPN([tr('4a1b2'), tr('2a2b1'), tr('1b3')]),
                         LPN([tr('-4a2b1'), tr('-7a1b2')]))
        self.assertEqual(LPN([tr('3y6')]) - LPN([tr('3y6')]), LPN([0]))

        # test mul
        self.assertEqual(LPN([tr('1a1'), tr('-1b1')]) * LPN([tr('1a1'), tr('1b1')]), LPN([tr('1a2'), tr('-1b2')]))
        self.assertEqual(LPN([tr('2a2'), tr('1a0')]) * LPN([tr('2a2'), tr('1a0')]),
                         LPN([tr('4a4'), tr('1a0'), tr('4a2')]))

        # test floordiv
        # self.assertEqual(LPN([tr('16x5'), tr('-8x3'), tr('2x1'), tr('-1a0')]) // LPN([tr('1x3'), tr('-1a0')]),
        #                  LPN([tr('16x2'), tr('-8a0')]))
        # self.assertEqual(LPN([tr('1x5'), tr('-3x4'), tr('5x3'), tr('-2x2'), tr('6x1'), tr('-10a0')]) // LPN([tr('1x3'),
        #                  tr('-2a0')]), LPN([tr('1x2'), tr('-3x1'), tr('5a0')]))

        # test mod
        self.assertEqual(LPN([tr('16x5'), tr('-8x3'), tr('2x1'), tr('-1a0')]) % LPN([tr('1x3'), tr('-1a0')]),
                         LPN([tr('16x2'), tr('2x1'), tr('-9a0')]))
        self.assertEqual(LPN([tr('1x5'), tr('-3x4'), tr('5x3'), tr('-2x2'), tr('6x1'), tr('-10a0')]) % LPN([tr('1x3'),
                                                                                                            tr(
                                                                                                                '-2a0')]),
                         LPN([0]))

        # test pow
        self.assertEqual(LPN([tr('4x2')]) ** 2, LPN([tr('16x4')]))
        self.assertEqual(LPN([tr('1a1'), tr('-2b1')]) ** RN(2), LPN([tr('1a2'), tr('-4a1b1'), tr('4b2')]))

        # test r-operations
        # test radd
        self.assertEqual(tr('3a0') + LPN([tr('4a0')]), LPN([tr('7a0')]))
        self.assertEqual(RN(3) + LPN([tr('4a0')]), LPN([tr('7a0')]))
        self.assertEqual(3 + LPN([tr('4a0')]), LPN([tr('7a0')]))
        self.assertEqual(3.0 + LPN([tr('4a0')]), LPN([tr('7a0')]))
        self.assertEqual(Fraction(3, 1) + LPN([tr('4a0')]), LPN([tr('7a0')]))
        self.assertEqual(Decimal(3) + LPN([tr('4a0')]), LPN([tr('7a0')]))

        # test rsub
        self.assertEqual(tr('3a0') - LPN([tr('4a0')]), LPN([tr('-1a0')]))
        self.assertEqual(RN(3) - LPN([tr('4a0')]), LPN([tr('-1a0')]))
        self.assertEqual(3 - LPN([tr('4a0')]), LPN([tr('-1a0')]))
        self.assertEqual(3.0 - LPN([tr('4a0')]), LPN([tr('-1a0')]))
        self.assertEqual(Fraction(3, 1) - LPN([tr('4a0')]), LPN([tr('-1a0')]))
        self.assertEqual(Decimal(3) - LPN([tr('4a0')]), LPN([tr('-1a0')]))

        # test rmul
        self.assertEqual(tr('3a0') * LPN([tr('4a0')]), LPN([tr('12a0')]))
        self.assertEqual(RN(3) * LPN([tr('4a0')]), LPN([tr('12a0')]))
        self.assertEqual(3 * LPN([tr('4a0')]), LPN([tr('12a0')]))
        self.assertEqual(3.0 * LPN([tr('4a0')]), LPN([tr('12a0')]))
        self.assertEqual(Fraction(3, 1) * LPN([tr('4a0')]), LPN([tr('12a0')]))
        self.assertEqual(Decimal(3) * LPN([tr('4a0')]), LPN([tr('12a0')]))

        # test rpow
        self.assertEqual(tr('3a0') ** LPN([tr('4a0')]), LPN([tr('81a0')]))
        self.assertEqual(RN(3) ** LPN([tr('4a0')]), LPN([tr('81a0')]))
        self.assertEqual(3 ** LPN([tr('4a0')]), LPN([tr('81a0')]))
        self.assertEqual(3.0 ** LPN([tr('4a0')]), LPN([tr('81a0')]))
        self.assertEqual(Fraction(3, 1) ** LPN([tr('4a0')]), LPN([tr('81a0')]))
        self.assertEqual(Decimal(3) ** LPN([tr('4a0')]), LPN([tr('81a0')]))

        # test eval to
        self.assertEqual(LPN([tr('4x1y1z1')]).eval_to({'x': 3, 'y': 1, 'z': 2}), RN(24))
        self.assertEqual(LPN([tr('3x2y1'), tr('-6y1')]).eval_to({'x': RN(2), 'y': RN(3)}), RN(18))

    def test_PN(self):
        # test data parser
        PN1 = PN(LPN([Tr(RN(4, 3), ML([Li('x', 2), Li('y', 1)])), Tr(-2, ML([Li('x', 3)]))]),
                 LPN([Tr(RN(1, 2), ML([Li('y', 3)])), Tr(RN(5, 4), ML([Li('x', 2)]))]))
        PN2 = PN(LPN([tr('6x3'), tr('-10x6y1')]), LPN([tr('12x2y4'), tr('4x5')]))
        PN3 = PN(RN(1, 2), RN(3, 4))
        PN4 = PN(tr('1x1'), tr('1x1'))
        PN5 = PN(0)
        PN6 = PN(RN(2, 5))

        self.assertEqual(PN1.numerator, LPN([tr('16x2y1'), tr('-24x3')]))
        self.assertEqual(PN1.denominator, LPN([tr('6y3'), tr('15x2')]))
        self.assertEqual(PN2.numerator, LPN([tr('3x1'), tr('-5x4y1')]))
        self.assertEqual(PN2.denominator, LPN([tr('6y4'), tr('2x3')]))

        self.assertEqual(PN3.numerator, 2)
        self.assertEqual(PN3.denominator, 3)
        self.assertEqual(PN4.numerator, 1)
        self.assertEqual(PN4.denominator, 1)

        self.assertEqual(PN5.numerator, 0)
        self.assertEqual(PN5.denominator, 1)
        self.assertEqual(PN6.numerator, 2)
        self.assertEqual(PN6.denominator, 5)

        # # test decomposing methods FOR MONO VARIABLE elements
        # # will assign new PN values
        #
        # test special type determination
        # I degree
        lpn1 = lpn('3x1 -2a0')
        lpn2 = lpn('4x2 -2x2 +4a0 -2x2 -5x1')
        lpn3 = lpn('-4a0 +4x1 -3x1 +4a0')
        lpn4 = lpn('5x1')

        self.assertEqual(_Lcl.get_special_type(lpn1), 'I degree')
        self.assertEqual(_Lcl.get_special_type(lpn2), 'I degree')
        self.assertEqual(_Lcl.get_special_type(lpn3), 'I degree')
        self.assertEqual(_Lcl.get_special_type(lpn4), 'I degree')

        # II degree
        lpn5 = lpn('3x2 -3a0')
        lpn6 = lpn('4x1 +3a0 -5x2')
        lpn7 = lpn('4x2 +3x1 -6a0 -3x1')
        lpn8 = lpn('-7x2 4x1 -1a0')

        self.assertEqual(_Lcl.get_special_type(lpn5), 'II degree')
        self.assertEqual(_Lcl.get_special_type(lpn6), 'II degree')
        self.assertEqual(_Lcl.get_special_type(lpn7), 'II degree')
        self.assertEqual(_Lcl.get_special_type(lpn8), 'II degree')

        # binomial
        lpn9 = lpn('3x5 -1a0')
        lpn10 = lpn('-5x6 -3a0 +4x6')
        lpn11 = lpn('4x3 +5a0 -2x3 +6x9 -2x3')
        lpn12 = lpn('10x7 -10a0')

        self.assertEqual(_Lcl.get_special_type(lpn9), 'binomial')
        self.assertEqual(_Lcl.get_special_type(lpn10), 'binomial')
        self.assertEqual(_Lcl.get_special_type(lpn11), 'binomial')
        self.assertEqual(_Lcl.get_special_type(lpn12), 'binomial')

        # trinomial
        lpn13 = lpn('5x4 +3a0 -12x2')
        lpn14 = lpn('-4x3 -5a0 +10x6 -4x6')
        lpn15 = lpn('5x2 +9a0 -2x1 +6x4 +2x1')
        lpn16 = lpn('7x8 +13x8 -3x4 -16a0')

        self.assertEqual(_Lcl.get_special_type(lpn13), 'trinomial')
        self.assertEqual(_Lcl.get_special_type(lpn14), 'trinomial')
        self.assertEqual(_Lcl.get_special_type(lpn15), 'trinomial')
        self.assertEqual(_Lcl.get_special_type(lpn16), 'trinomial')

        # none
        lpn17 = lpn('3x4 -5x1')
        lpn18 = lpn('5x2 -4x4 +6a0 +7x5')
        lpn19 = lpn('1x3 1x2 1x1 1a0')
        lpn20 = lpn('27x3 -9x2 9x1 -27a0')

        self.assertEqual(_Lcl.get_special_type(lpn17), '')
        self.assertEqual(_Lcl.get_special_type(lpn18), '')
        self.assertEqual(_Lcl.get_special_type(lpn19), '')
        self.assertEqual(_Lcl.get_special_type(lpn20), '')

        # test single reduction from special types
        # I degree
        self.assertEqual(_Lcl.reduce_pn_element(lpn1), [lpn1])
        self.assertEqual(_Lcl.reduce_pn_element(lpn2), [lpn2])
        self.assertEqual(_Lcl.reduce_pn_element(lpn3), [lpn3])
        self.assertEqual(_Lcl.reduce_pn_element(lpn4), [lpn4])

        # II degree
        self.assertEqual(_Lcl.reduce_pn_element(lpn5), [lpn('3a0'), lpn('1x1 -1a0'), lpn('1x1 +1a0')])
        root_one = RN(LRN([RNU(s='2'), RNU(Ra(-1), Ir(19, 2))]), 5)
        root_two = RN(LRN([RNU(s='2'), RNU(Ra(1), Ir(19, 2))]), 5)
        self.assertEqual(_Lcl.reduce_pn_element(lpn6), [lpn('-5a0'), lpn('1x1') - root_one, lpn('1x1') - root_two])
        root_one = RN(RNU(Ra(1), Ir(6, 2)), 2)
        root_two = RN(RNU(Ra(-1), Ir(6, 2)), 2)
        self.assertEqual(_Lcl.reduce_pn_element(lpn7), [lpn('4a0'), lpn('1x1') - root_one, lpn('1x1') - root_two])
        self.assertEqual(_Lcl.reduce_pn_element(lpn8), [lpn8])

        # binomial
        # test deprecated
        # self.assertEqual(_Lcl.reduce_pn_element(lpn9), [lpn9])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn10), [lpn10])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn11), [lpn11])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn12), [lpn12])

        # trinomial
        root_one = RN(LRN([RNU(s='6'), RNU(Ra(1), Ir(21, 2))]), 5)
        root_two = RN(LRN([RNU(s='6'), RNU(Ra(-1), Ir(21, 2))]), 5)
        self.assertEqual(_Lcl.reduce_pn_element(lpn13), [lpn('5a0'), lpn('1x2') - root_one, lpn('1x2') - root_two])
        root_one = RN(LRN([RNU(s='2'), RNU(Ra(1), Ir(34, 2))]), 6)
        root_two = RN(LRN([RNU(s='2'), RNU(Ra(-1), Ir(34, 2))]), 6)
        self.assertEqual(_Lcl.reduce_pn_element(lpn14), [lpn('6a0'), lpn('1x3') - root_one, lpn('1x3') - root_two])
        self.assertEqual(_Lcl.reduce_pn_element(lpn15), [lpn15])
        root_one = RN(LRN([RNU(s='3'), RNU(Ra(1), Ir(1289, 2))]), 40)
        root_two = RN(LRN([RNU(s='3'), RNU(Ra(-1), Ir(1289, 2))]), 40)
        self.assertEqual(_Lcl.reduce_pn_element(lpn16), [lpn('20a0'), lpn('1x4') - root_one, lpn('1x4') - root_two])

        # none
        # test case 1
        self.assertEqual(_Lcl.reduce_pn_element(lpn17), [lpn('1x1'), lpn('3x3 -5')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('5x4 -25y3')), [lpn('5a0'), lpn('1x4 -5y3')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x3y1 4x2y2')), [lpn('1x2y1'), lpn('1x1 4y1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('3x6 +3x1 -6x1y2')), [lpn('3x1'), lpn('1x5 1a0 -2y2')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('3x2 +5x6 -7x4')), [lpn('1x2'), lpn('3a0 5x4 -7x2')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('5z5 +5z4')), [lpn('5z4'), lpn('1z1 +1a0')])

        # test case 2
        self.assertEqual(_Lcl.reduce_pn_element(lpn('3b1c1 +2a1b1 -2a1 -3c1')), [lpn('1b1 -1a0'), lpn('3c1 +2a1')])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn('')), [lpn(''), lpn('')])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn('')), [lpn(''), lpn('')])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn('')), [lpn(''), lpn('')])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn('')), [lpn(''), lpn('')])
        # self.assertEqual(_Lcl.reduce_pn_element(lpn('')), [lpn(''), lpn('')])

        # test case 3-a
        self.assertEqual(_Lcl.reduce_pn_element(lpn('25a2 -9b2')), [lpn('5a1 3b1'), lpn('5a1 -3b1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x2 -9y2')), [lpn('1x1 3y1'), lpn('1x1 -3y1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('-1b2 16a4')), [lpn('4a2 1b1'), lpn('4a2 -1b1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('-1y2 64x6')), [lpn('8x3 1y1'), lpn('8x3 -1y1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('121y8 -49x2')), [lpn('11y4 7x1'), lpn('11y4 -7x1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x6 -25y2')), [lpn('1x3 5y1'), lpn('1x3 -5y1')])

        # test case 3-a/b
        self.assertEqual(_Lcl.reduce_pn_element(lpn('8a3 +1b3')), [lpn('2a1 +1b1'), lpn('4a2 -2a1b1 1b2')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1a3b3 +1a0')), [lpn('1a1b1 +1a0'), lpn('1a2b2 -1a1b1 +1a0')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x6 -1y3')), [lpn('1x2 -1y1'), lpn('1x4 +1x2y1 +1y2')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('-1a3b3 -27a0')), [lpn('-1a0'), lpn('1a1b1 +3a0'),
                                                                       lpn('1a2b2 -3a1b1 +9a0')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1a3 +1x6')), [lpn('1a1 +1x2'), lpn('1a2 -1a1x2 +1x4')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('125a3 +8b3')), [lpn('5a1 +2b1'), lpn('25a2 -10a1b1 +4b2')])

        # test case 4
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1a3 +1b3 +3a2b1 +3a1b2')), [lpn('1a1 +1b1'), lpn('1a1 +1b1'),
                                                                                 lpn('1a1 +1b1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1a3 -6a2b1 +12a1b2 -8b3')), [lpn('1a1 -2b1'), lpn('1a1 -2b1'),
                                                                                  lpn('1a1 -2b1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('-1a3 +3a2b1 -3a1b2 +1b3')), [lpn('-1a1 +1b1'), lpn('-1a1 +1b1'),
                                                                                  lpn('-1a1 +1b1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1a3b3 -3a2b2 +3a1b1 -1a0')), [lpn('1a1b1 -1a0'), lpn('1a1b1 -1a0'),
                                                                                   lpn('1a1b1 -1a0')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x3 +15x2 +75x1 +125a0')), [lpn('1x1 +5a0'), lpn('1x1 +5a0'),
                                                                                 lpn('1x1 +5a0')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1a6x9 -6a4x6 +12a2x3 -8a0')), [lpn('1a2x3 -2a0'),
                                                                                    lpn('1a2x3 -2a0'),
                                                                                    lpn('1a2x3 -2a0')])

        # test case 5
        self.assertEqual(_Lcl.reduce_pn_element(lpn('9a2 +4b2 +1a0 -12a1b1 +6a1 -4b1')), [lpn('3a1 -2b1 +1a0'),
                                                                                          lpn('3a1 -2b1 +1a0')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x2 +1y4 +1a0 +2x1y2 -2x1 -2y2')),
                         [lpn('1x1 +1y2 -1a0'), lpn('1x1 +1y2 -1a0')])
        self.assertEqual(_Lcl._verify_case5_match(lpn('1a8 -2a6 -2a5 +1a4 +2a3 +1a2')),
                         [lpn('-1a4 +1a2 +1a1'), lpn('-1a4 +1a2 +1a1')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('25x2 +9y2 +4a0 -30x1y1 +20x1 -12y1')),
                         [lpn('5x1 -3y1 +2'), lpn('5x1 -3y1 +2')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('1x3y1 -3x1y2 +1a0') * lpn('1x3y1 -3x1y2 +1a0')),
                         [lpn('1x3y1 -3x1y2 +1a0'), lpn('1x3y1 -3x1y2 +1a0')])
        self.assertEqual(_Lcl.reduce_pn_element(lpn('2x1y3 +3x2 -1y2') * lpn('2x1y3 +3x2 -1y2')),
                         [lpn('2x1y3 +3x2 -1y2'), lpn('2x1y3 +3x2 -1y2')])

        # test case 6
        self.assertEqual(_Lcl._verify_case6_match(lpn('1x3 -2x2 +4x1 -3a0')), [lpn('1x1 -1a0'),
                                                                               lpn('1x2 -1x1 +3a0')])
        self.assertEqual(_Lcl._verify_case6_match(lpn('3a3 -2a2 -5a1 -6a0')), [lpn('1a1 -2a0'),
                                                                               lpn('3a2 +4a1 +3a0')])
        self.assertEqual(_Lcl._verify_case6_match(lpn('5x2 -4x1 -1a0')), [lpn('1x1 -1a0'), lpn('5x1 +1a0')])

    def test_reduce(self):
        # test polynomial reduction mechanics
        self.assertEqual(pn('[2x1 -2y1]/[1y1 -1x1]').reduce, [[lpn('2')], [lpn('-1')]])
        self.assertEqual(pn('[1x2 -1x1]/[1x1 -1]').reduce, [[lpn('1x1')], [lpn('1')]])
        self.assertEqual(pn('[1x2 +3x1]/[3x1]').reduce, [[lpn('1x1 +3')], [lpn('3')]])
        self.assertEqual(pn('[2a1 -2]/[5a1 -5]').reduce, [[lpn('2')], [lpn('5')]])
        self.assertEqual(pn('[-1x1 -1y1]/[1x1 +1y1]').reduce, [[lpn('1')], [lpn('-1')]])
        self.assertEqual(pn('[4x2 -2x1]/[4x2]').reduce, [[lpn('2x1 -1')], [lpn('2x1')]])

        self.assertEqual(pn('[6a1 -3b1]/[6a1]').reduce, [[lpn('2a1 -1b1')], [lpn('2a1')]])
        self.assertEqual(pn('[2x1 -2y1]/[2x1 +2y1]').reduce, [[lpn('1x1 -1y1')], [lpn('1x1 +1y1')]])
        self.assertEqual(pn('[1a1 +1b1]/[1a2 +1a1b1]').reduce, [[lpn('1')], [lpn('1a1')]])
        self.assertEqual(pn('[1a2 -2a1]/[1a1 -2]').reduce, [[lpn('1a1')], [lpn('1')]])
        self.assertEqual(pn('[1x1]/[2x2 -1x1]').reduce, [[lpn('1')], [lpn('2x1 -1')]])
        self.assertEqual(pn('[1x3 -1x2]/[4x2y1]').reduce, [[lpn('1x1 -1')], [lpn('4y1')]])

        self.assertEqual(pn('[1y1 -1y2]/[1a1 -1a1y1]').reduce, [[lpn('1y1')], [lpn('1a1')]])
        self.assertEqual(pn('[1a1x1]/[1x2 -1a1x1]').reduce, [[lpn('1a1')], [lpn('1x1 -1a1')]])
        self.assertEqual(pn('[4x1y1]/[2x2y1 -2x1y1]').reduce, [[lpn('2')], [lpn('1x1 -1')]])
        self.assertEqual(pn('[1a1 +1a1x1]/[1y1 +1x1y1]').reduce, [[lpn('1a1')], [lpn('1y1')]])
        self.assertEqual(pn('[2a2 -10a1]/[1a1x1 -5x1]').reduce, [[lpn('2a1')], [lpn('1x1')]])
        self.assertEqual(pn('[1x1y1]/[1x2 -1x1y1]').reduce, [[lpn('1y1')], [lpn('1x1 -1y1')]])

        self.assertEqual(pn('[6x2 -12x1 +6]/[1x2 -1]').reduce, [[lpn('6'), lpn('1x1 -1')], [lpn('1x1 +1')]])
        self.assertEqual(pn('[1x1y2 -1x1]/[1 -1y1]').reduce, [[lpn('1x1'), lpn('1 +1y1'), lpn('-1')], [lpn('1')]])
        self.assertEqual(pn('[4a2 -4]/[2a1 +2]').reduce, [[lpn('2'), lpn('1a1 -1')], [lpn('1')]])
        self.assertEqual(pn('[6a1x1 -6a2]/[1x2 -1a2]').reduce, [[lpn('6a1')], [lpn('1x1 +1a1')]])
        self.assertEqual(pn('[12a1 -3a2]/[4y1 -1a1y1]').reduce, [[lpn('3a1')], [lpn('1y1')]])
        self.assertEqual(pn('[2x6 +2x2]/[2x2]').reduce, [[lpn('1x4 +1')], [lpn('1')]])

        self.assertEqual(pn('[-24a1b1x1]/[8a1x1 -12b1x1]').reduce, [[lpn('-6a1b1')], [lpn('2a1 -3b1')]])
        self.assertEqual(pn('[4a2 -1b2]/[1b3 -2b2a1]').reduce, [[lpn('2a1 +1b1')], [lpn('1b2'), lpn('-1')]])
        self.assertEqual(pn('[1x3 -1y3]/[1x3y3]').reduce, [[lpn('1x1 -1y1'), lpn('1x2 +1x1y1 +1y2')], [lpn('1x3y3')]])
        self.assertEqual(pn('[1a3 -8]/[1a2 +2a1 +4]').reduce, [[lpn('1a1 -2')], [lpn('1')]])
        self.assertEqual(pn('[1a2 -5a1 +6]/[2a1 -6]').reduce, [[lpn('1a1 -2')], [lpn('2')]])
        self.assertEqual(pn('[3x1y1 +3y2]/[1x2 -1y2]').reduce, [[lpn('3y1')], [lpn('1x1 -1y1')]])

        self.assertEqual(pn('[3x5]/[12x1 +12x2]').reduce, [[lpn('1x4')], [lpn('4'), lpn('1 +1x1')]])
        self.assertEqual(pn('[8a3 +4a1]/[4a2 +1]').reduce, [[lpn('4a1'), lpn('2a2 +1')], [lpn('4a2 +1')]])
        self.assertEqual(pn('[1y2 -2y1 -3]/[1y2 -1]').reduce, [[lpn('1y1 -3')], [lpn('1y1 -1')]])
        self.assertEqual(pn('[1x4 +16]/[1x4 +16 -8x2]').reduce,
                         [[lpn('1x4 +16')], [lpn('2 +1x1'), lpn('-2 +1x1'), lpn('2 +1x1'), lpn('-2 +1x1')]])
        self.assertEqual(pn('[14a1 -7b1]/[4a2 -1b2]').reduce, [[lpn('7')], [lpn('2a1 +1b1')]])
        # self.assertEqual(((pn('[4x1 -4y1]/[1]') + (pn('[1x1 -1y1]/[1]')) ** 2) / (pn('[1x1 -1y1]/[1]') ** 2)).reduce,
        #                  [[lpn('4 +1x1 -1y1')], [lpn('1x1 -1y1')]])

        self.assertEqual(pn('[1a4 -1]/[1a3 -1]').reduce, [[lpn('1a2 +1'), lpn('1a1 +1')], [lpn('1a2 +1a1 +1')]])
        self.assertEqual(pn('[1a1x1 +2x1 -1a1 -2]/[1a1x1 -2x1 -1a1 +2]').reduce, [[lpn('1a1 +2')], [lpn('1a1 -2')]])
        self.assertEqual(pn('[1a2 -4]/[1a2 -4a1 +4]').reduce, [[lpn('1a1 +2'), lpn('-1')], [lpn('-1a1 2')]])
        self.assertEqual(pn('[9a2 -9]/[3a1 +3]').reduce, [[lpn('3'), lpn('1a1 -1')], [lpn('1')]])
        self.assertEqual(pn('[1a1y1 +1a1x1 +2y1 +2x1]/[4a1y1 +4a1x1]').reduce, [[lpn('1a1 +2')], [lpn('4a1')]])
        self.assertEqual(pn('[9 -3y1]/[3a2 -1a2y1]').reduce, [[lpn('3')], [lpn('1a2')]])

        self.assertEqual(pn('[1x2 -2x1 -3]/[1x2 -6x1 +9]').reduce, [[lpn('1x1 +1'), lpn('-1')], [lpn('-1x1 3')]])
        self.assertEqual(pn('[1a2x1 +2a1x1 +1x1]/[2x1 +2a1x1]').reduce, [[lpn('1a1 +1')], [lpn('2')]])
        self.assertEqual(pn('[1x2 -9]/[6a1 +2a1x1]').reduce, [[lpn('1x1 -3')], [lpn('2a1')]])
        self.assertEqual(pn('[4x2 -4x1 +1]/[2a1x1 +2x1 -1a1 -1]').reduce, [[lpn('-2x1 1')], [lpn('1a1 +1'), lpn('-1')]])
        self.assertEqual(pn('[1x2 -4]/[1x2 -1x1 -2]').reduce, [[lpn('1x1 +2')], [lpn('1x1 +1')]])
        self.assertEqual(pn('[1a4 -16]/[2a2 +8]').reduce, [[lpn('1a1 -2'), lpn('1a1 +2')], [lpn('2')]])

        self.assertEqual(pn('[1a1x1 -1x1 +3a1 -3]/[1x2 +4x1 +3]').reduce, [[lpn('1a1 -1')], [lpn('1x1 +1')]])
        self.assertEqual(pn('[1y2 -9]/[1y3 -3y2]').reduce, [[lpn('1y1 +3')], [lpn('1y2')]])
        self.assertEqual(pn('[1x3 +4x2 +4x1]/[4 -1x2]').reduce, [[lpn('1x1'), lpn('1x1 +2')],
                                                                 [lpn('-2 +1x1'), lpn('-1')]])
        self.assertEqual(pn('[1x2y1 -4y1]/[-2y1 -1x1y1]').reduce, [[lpn('-2 +1x1'), lpn('-1')], [lpn('1')]])
        self.assertEqual(pn('[1a2 -10a1 +25]/[1a2 -25]').reduce, [[lpn('-1a1 +5')], [lpn('1a1 +5'), lpn('-1')]])
        self.assertEqual(pn('[6x3 -6x1y2]/[1x2 +1x1y1]').reduce, [[lpn('6'), lpn('1x1 -1y1')], [lpn('1')]])

        self.assertEqual(pn('[2a2 -1a2x1]/[4y1 -2x1y1]').reduce, [[lpn('1a2')], [lpn('2y1')]])
        self.assertEqual(pn('[6x2y1 -12x1y1]/[9x4y1 -18x3y1]').reduce, [[lpn('2')], [lpn('3x2')]])
        self.assertEqual(pn('[1x3 -1a3]/[3x1 -3a1]').reduce, [[lpn('1x2 +1a1x1 +1a2')], [lpn('3')]])
        self.assertEqual(pn('[2a4 -2x4]/[4a2 +4x2]').reduce, [[lpn('1a1 +1x1'), lpn('1a1 -1x1')], [lpn('2')]])
        self.assertEqual(pn('[1x2 -2x1]/[1x2 +2x1 -8]').reduce, [[lpn('1x1')], [lpn('1x1 +4')]])
        self.assertEqual(pn('[6a1x2 -6a1y2]/[3x3 -3y3]').reduce, [[lpn('2a1'), lpn('1x1 +1y1')],
                                                                  [lpn('1x2 +1x1y1 +1y2')]])

        self.assertEqual(pn('[4a3 -4a2]/[1a3 -2a2 +1a1]').reduce, [[lpn('4a1')], [lpn('-1a1 +1'), lpn('-1')]])
        self.assertEqual((((pn('[1x1 -2]/[1]') ** 2) + tr('2x1')) / (tr('2') * pn('[1x3 +8]/[1]'))).reduce,
                         [[lpn('1')], [lpn('2'), lpn('1x1 +2')]])
        self.assertEqual(pn('[30a2b2]/[1a2b1 -1a1b2]').reduce, [[lpn('30a1b1')], [lpn('1a1 -1b1')]])
        self.assertEqual((pn('[1x2 -1]/[1]') / (lpn('1x1 +1') * lpn('1x2 -2x1 +1'))).reduce,
                         [[lpn('1')], [lpn('1x1 -1')]])
        self.assertEqual(pn('[1a3 -1b3]/[1a2 -1b2]').reduce, [[lpn('1a2 +1a1b1 +1b2')], [lpn('1a1 +1b1')]])
        self.assertEqual(pn('[1x3 -2x2 +1x1]/[1x3 -3x2 +3x1 -1]').reduce, [[lpn('1x1'), lpn('-1')],
                                                                           [lpn('1x1 -1'), lpn('-1')]])


if __name__ == '__main__':
    unittest.main()
