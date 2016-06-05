from docutils import nodes, utils
from functools import wraps
import inspect
import logging
import imp
import os

from sphinx.util.nodes import split_explicit_title


logger = logging.getLogger(__name__)


class SimpleRole(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, '_%s' % k, v)

        super(SimpleRole, self).__init__()

    @classmethod
    def get_name(cls):
        filename, _ = os.path.splitext(
            os.path.basename(inspect.getfile(cls))
        )

        return filename

    def get_values(self):
        has_explicit, title, target = split_explicit_title(
            utils.unescape(self._text)
        )

        values = {
            'has_explicit_title': has_explicit,
            'title': title,
            'target': target,
        }

        return values

    def get_text(self):
        values = self.get_values()

        return values['title']

    def _get_all_nodes(self):
        return self.get_nodes(), []

    def get_nodes(self):
        return [
            nodes.Text(
                data=self.get_text(),
                rawsource=self._rawtext,
            )
        ]


class SimpleLinkRole(SimpleRole):
    def get_target(self):
        values = self.get_values()

        return values['target']

    def get_nodes(self):
        return [
            nodes.reference(
                rawsource=self._rawtext,
                text=self.get_text(),
                refuri=self.get_target(),
            )
        ]


def register_role(cls):
    @wraps(cls)
    def _custom_role(
        typ, rawtext, text, lineno, inliner, options={}, content=[]
    ):
        role = cls(
            typ=typ,
            rawtext=rawtext,
            text=text,
            lineno=lineno,
            inliner=inliner,
            options={},
            content=[],
        )

        return role._get_all_nodes()

    return _custom_role


def add_role(app, role_name, cls):
    app.add_role(role_name, register_role(cls))


def get_plugins(app):
    plugin_dir = os.path.join(
        app.confdir,
        app.config.helpers_path
    )

    for filename in os.listdir(plugin_dir):
        module_name, ext = os.path.splitext(filename)

        if ext == '.py':
            helper = imp.load_source(
                'sphinxcontrib.helpers.%s' % module_name,
                os.path.join(
                    plugin_dir,
                    filename,
                )
            )

            for name in dir(helper):
                cls = getattr(helper, name)
                if not inspect.isclass(cls):
                    continue
                if (
                    issubclass(cls, SimpleRole) and
                    not cls.__module__ == 'sphinxcontrib.helpers'
                ):
                    yield cls
        elif ext == '.pyc':
            pass
        else:
            logger.warning(
                "No handlers available for helper of type %s" % (
                    ext,
                )
            )


def setup(app):
    app.add_config_value(
        'helpers_path',
        'helpers/',
        'html',
    )

    for plugin in get_plugins(app):
        add_role(
            app,
            plugin.get_name(),
            plugin,
        )
