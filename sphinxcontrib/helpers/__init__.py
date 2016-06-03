from docutils import nodes, utils
from functools import wraps

from sphinx.util.nodes import split_explicit_title


def custom_role_generator(fn):
    @wraps(fn)
    def _custom_role(
        typ, rawtext, text, lineno, inliner, options={}, content=[]
    ):
        has_explicit, title, target = split_explicit_title(
            utils.unescape(text)
        )

        title, target = fn(
            title,
            target,
        )

        reference = nodes.reference(
            rawtext,
            title,
            refuri=target,
        )

        return [reference], []

    return _custom_role


def create_url_role(app, role_name, fn):
    app.add_role(role_name, custom_role_generator(fn))
