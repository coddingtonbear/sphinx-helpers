Sphinx Helpers
==============


Create an interpreted role more easily --


.. code-block:: python

    from sphinxcontrib.helpers import create_role

    def my_role_function(title, target, **kwargs):
        return "My Title", "my url"

    def setup(app):
        create_role(
            'my-role-name',
            my_role_function
        )
