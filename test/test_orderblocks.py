# OrderBlocks extension for Jinja2 -- Test script
# Copyright (C) 2016 Graham Bell
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from jinja2 import Environment

from jinja2_orderblocks import OrderBlocks


class OrderBlockTestCase(TestCase):
    def test_basic(self):
        env = Environment(extensions=[OrderBlocks])

        template = env.from_string(
            'a'
            '{% orderblocks blocks %}'
            '{% block x %}b{% endblock %}'
            '{% block y %}c{% endblock %}'
            '{% block z %}d{% endblock %}'
            '{% endorderblocks %}'
            'e')

        self.assertEqual(template.render(), 'abcde')
        self.assertEqual(template.render(blocks=None), 'abcde')
        self.assertEqual(template.render(blocks=('x', 'y', 'z')), 'abcde')
        self.assertEqual(template.render(blocks=('z', 'y', 'x')), 'adcbe')
        self.assertEqual(template.render(blocks=('z', 'x', 'y')), 'adbce')
        self.assertEqual(template.render(blocks=('x', 'z', 'y')), 'abdce')
        self.assertEqual(template.render(blocks=('x', 'y')), 'abce')
        self.assertEqual(template.render(blocks=('x', 'z')), 'abde')
        self.assertEqual(template.render(blocks=('y', 'z')), 'acde')
        self.assertEqual(template.render(blocks=('z', 'y')), 'adce')
        self.assertEqual(template.render(blocks=('z', 'x')), 'adbe')
        self.assertEqual(template.render(blocks=('x')), 'abe')
        self.assertEqual(template.render(blocks=('y')), 'ace')
        self.assertEqual(template.render(blocks=('z')), 'ade')
