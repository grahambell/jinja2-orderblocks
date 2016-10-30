# OrderBlocks extension for Jinja2
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

from jinja2 import ext, nodes


class OrderBlocks(ext.Extension):
    """
    Extension for Jinja2 to reorder blocks.

    This adds a tag `{% orderblocks %} ... {% endorderblocks %}`
    which can be used to change the order of the blocks it contains.
    It takes one argument which should be a list (or other iterable)
    of block names in the order in which they should be displayed.
    Block names can be omitted from the list to prevent them from
    being shown at all.  Nodes other than blocks inside the `orderblocks`
    section are ignored.

    >>> from jinja2 import Environment
    >>> env = Environment(extensions=[
    ...     'jinja2_orderblocks.OrderBlocks'])
    >>> template = env.from_string(
    ...     '{% orderblocks block_order %}'
    ...     '{% block one %}1{% endblock %}'
    ...     '{% block two %}2{% endblock %}'
    ...     '{% endorderblocks %}')
    >>> print(template.render(block_order=['two', 'one']))
    21
    """

    tags = set(['orderblocks'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        # Get the block selection from the tag argument.
        block_selection = parser.parse_expression()

        # Make "Name" node for "For" node target.
        block_name = nodes.Name('_ext_ob_blknm', 'store')

        # For each block, add an "If" node checking if it matches the target.
        # Also record the original "default" ordering of the blocks.
        blocks = []
        block_names = []
        for node in parser.parse_statements(['name:endorderblocks'],
                                            drop_needle=True):
            if isinstance(node, nodes.Block):
                blocks.append(nodes.If(
                    nodes.Compare(
                        block_name,
                        [nodes.Operand('eq', nodes.Const(node.name))]),
                    [node], []))

                block_names.append(node.name)

        # Make a "For" node iterating over the given block selection.  If the
        # block selection is undefined or None then use the original ordering.
        return nodes.For(
            block_name,
            nodes.CondExpr(
                nodes.And(
                    nodes.Test(block_selection, 'defined',
                               [], [], None, None),
                    nodes.Not(
                        nodes.Test(block_selection, 'none',
                                   [], [], None, None)),
                ),
                block_selection,
                nodes.Tuple([nodes.Const(x) for x in block_names], 'store')),
            blocks, [], None, False)
