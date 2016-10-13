OrderBlocks Extension for Jinja2
================================

Introduction
------------

This is an extension for the `Jinja2 <http://jinja.pocoo.org/>`_
template engine which allows you to select and reorder inheritance blocks.


Example 1: Ordering Specified by Child Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, a website might wish to publish a number of articles.
Each article shows some basic information about the article, the main
story itself and perhaps some images.
This could be done with a template `"article.html"` which
inherits from the website's main `"layout.html"` template and
overrides the `content` block to contain three new blocks:
`introduction`, `story` and `images`::

    {% extends 'layout.html' %}

    {% block content %}
        {% orderblocks article_order %}
            {% block introduction %}
                <ul>
                    <li>Some introductory information</li>
                    <li>E.g. date, author, &hellip;</li>
                </ul>
            {% endblock %}

            {% block story %}
                <p>Article story goes here &hellip;</p>
            {% endblock %}

            {% block images %}
                <p>
                    <img src="..." />
                </p>
            {% endblock %}
        {% endorderblocks %}
    {% endblock %}

Note that the blocks are enclosed in the `orderblocks` tag.
This takes one argument, specifying the order in which to show the
contained blocks.
(Any non-block contents are ignored.)
In this case this argument is given by the `article_order` parameter.
When this is undefined, as it is here, (or None) the blocks are shown in their
original ordering.

However there might also be some special kinds of articles, such as
an image feature article.
Here the images should appear in a special display before the story text.
The template for this kind of article can inherit from the `"article.html"`
template but specify a value for the `article_order` parameter::

    {% extends 'article.html' %}

    {% set article_order = ('introduction', 'images', 'story') %}

    {% block images %}
        <!-- Placeholder for fancy image display! -->
        <big>{{ super() }}</big>
    {% endblock %}

Example 2: Dynamically-specified Ordering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The block ordering parameter can of course also be specified by
a template context parameter.
Here a page allows the user to specify which sections
they wish to see, and their ordering, via a request argument::

    from flask import Flask, render_template, request

    app = Flask(__name__)

    app.jinja_options['extensions'].append(
        'jinja2_orderblocks.OrderBlocks')

    @app.route('/example/')
    def example_page():
        return render_template(
            'example_template.html',
            article_order=request.args['order'].split(','))

It could be used with a template which included a number of sections,
such as the following fragment::

    {% orderblocks article_order %}
        {% block x %}
            <section>
                <h2>Section X</h2>
                <p>&hellip;</p>
            </section>
        {% endblock %}

        {% block y %}
            <section>
                <h2>Section Y</h2>
                <p>&hellip;</p>
            </section>
        {% endblock %}

        {% block z %}
            <section>
                <h2>Section Z</h2>
                <p>&hellip;</p>
            </section>
        {% endblock %}
    {% endorderblocks %}

The sections could be requested in reverse order via
`http://.../example/?order=z,y,x`
or a single section could be requested using
`http://.../example/?order=y`.

Note on Implementation
~~~~~~~~~~~~~~~~~~~~~~

This extension, as currently implemented, works by replacing the
`orderblocks` tag with a for loop which iterates over the list of
requested block names, and includes blocks which match the requested
names.
In other words it converts a structure like this::

    {% orderblocks block_order %}
        {% block x %}
            <p>X</p>
        {% endblock %}

        {% block y %}
            <p>Y</p>
        {% endblock %}
    {% endorderblocks %}

into a for loop of if blocks such as::

    {% for block_name in block_order %}
        {% if block_name == 'x' %}
            {% block x %}
                <p>X</p>
            {% endblock %}
        {% endif %}

        {% if block_name == 'y' %}
            {% block y %}
                <p>Y</p>
            {% endblock %}
        {% endif %}
    {% endfor %}

Installation
------------

The extension can be installed using the ``setup.py`` script::

    python setup.py install

Before doing that, you might like to run the unit tests::

    PYTHONPATH=lib python -m unittest discover

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
