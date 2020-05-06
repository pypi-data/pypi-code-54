
import unittest

from fractions import Fraction

from .ex import Ex
from ..engine.pn.pn import lpn


class TestEx(unittest.TestCase):
    def test_value(self):
        self.assertEqual(Ex('[ab(1-(a-b)/(a+b))((1)/(a)+(1)/(b))]^2 / [b^2(1-(a+b)/(a-b))((1)/(a)-(1)/(b))]^2').reduced,
                         [[lpn('1a2')], [lpn('1b2')]])
        self.assertEqual(Ex('{[(2b-1)^3-(1)/(2b-1)]/[(8b^2-8b)/(2b-1)]-b^2}(1-[(b^2-2b)/(b^2-2b+1)])').reduced,
                         [[lpn('1')], [lpn('1')]])
        self.assertEqual(Ex('[((1)/(x-2) - (1)/(3-x)) / [(5-2x)/(x^2+3-4x)] + [(1-x)/(x-2)]^2] / [[(x-1)/(x-2)]^2 '
                            '- (x-1)/(4+x^2-4x)]').reduced, [[lpn('1')], [lpn('1x1 -2')]])
        self.assertEqual(Ex('[(2x+y)/(x-y) - (x^2+5xy)/(x^2-y^2)]^3 / [(x^6+y^6-2x^3y^3)/(x^3+3x^2y+3xy^2+y^3)] '
                            '+ (y-x)/[(x^2+xy+y^2)^2]').reduced, [[lpn('0')], [lpn('1')]])

        # self.assertEqual(Ex('[[[(3x^2-2)/(x-1)+[(6x-2)/(x-3)][(9-x^2)/(3x-1)]][(1)/(x-2)]+1]^2][(x+1+x-2)/(x+1)]^3')
        #                  .reduced, [[lpn('1x1 -1')], [lpn('2x1 -3')]])
        # self.assertEqual(Ex('[((x+2y^2)^3)/((1-x)^2)] / [((2y^2+x)^2)/((x-1)^3)]').reduced,
        #                  [[lpn('1x1 +2y2'), lpn('1x1 -1')], [lpn('1')]])
        self.assertEqual(Ex('[((2a-b)/(a^2-b^2)-(2)/(a+b))^2/((a^2)/(a^2-b^2)-1)^2]^2').reduced,
                         [[lpn('1')], [lpn('1b4')]])
        self.assertEqual(Ex('1/2[(a-x)/(m)]+(11)/(5x)+(5x^2-2m)/(10mx)-(a)/(2m)').reduced,
                         [[lpn('2')], [lpn('1x1')]])

        self.assertEqual(Ex('[(x^2-y^2)/(16y^4-(y+1)^2)][(4y^2+y+1)/(3x-3y)][(4y^2-y-1)/(x+y)]').reduced,
                         [[lpn('1')], [lpn('3')]])
        self.assertEqual(Ex('{{[((1)/(x-3)+(1)/(1-x))(x^2-4x+3)-(4)/(3x-1)](1/6)}^2}/[(x^2-2x+1)/(3x^2-4x+1)]').reduced,
                         [[lpn('1x1 -1')], [lpn('3x1 -1')//Fraction(3), lpn('3')]])
        self.assertEqual(Ex('{[(2b-1)^3-(1)/(2b-1)]/[(8b^2-8b)/(2b-1)]-b^2}[1-(b^2-2b)/(b^2-2b+1)]').reduced,
                         [[lpn('1')], [lpn('1')]])
        # self.assertEqual(Ex('[(2x)/(x+y)+(4y)/(x-y)-(4y^2)/(x^2-y^2)]/{[2-(y)/(x+y)][((2+x-2y)(x+y))/(x(2x+y))]}')
        #                  .reduced, [[lpn('2x2')], [lpn('1x1 -1y1'), lpn('2 +1x1 -2y2')]])


if __name__ == '__main__':
    unittest.main()
