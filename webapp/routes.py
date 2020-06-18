import logging
from flask import render_template, abort
from webapp import app, pgdd

LOGGER = logging.getLogger(__name__)


@app.route('/<object_type>')
def view_schemas_list(object_type):
    try:
        object_list = pgdd.get_object_list(object_type)
    except TypeError:
        abort(404)

    return render_template('/object_list.html',
                           object_list=object_list,
                           object_type=object_type)

@app.errorhandler(404)
def page_not_found(err):
    """ Handles 404 errors to render custom 404 page """
    LOGGER.error('error: %s', err)
    return render_template('404.html'), 404


