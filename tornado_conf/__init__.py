from tornado.util import ObjectDict


def setup_settings(settings_package, pull_options=True, default_settings='base', final=False):
    from tornado.log import enable_pretty_logging
    from tornado.options import options

    options.define('settings', default=default_settings, help='Define settings module')

    def parse_callback():
        global settings
        settings.load(settings_package, options.settings)

        if pull_options:
            # let's pull options from the settings and vice versa
            for option_name in options:
                src, dst = (settings, options) if option_name in settings else (options, settings)
                setattr(dst, option_name, src[option_name])
            # resets logging configuration
            enable_pretty_logging()

    options.add_parse_callback(callback=parse_callback)

    global settings
    settings.setup_settings = [settings_package, default_settings, final]

    if final:
        options.run_parse_callbacks()


class Conf(ObjectDict):

    def load(self, settings_package, settings_module):
        from importlib import import_module
        settings_module = import_module('.{module}'.format(module=settings_module), settings_package)
        self.update({opt: val for opt, val in settings_module.__dict__.items() if not opt.startswith('_')})


settings = Conf()

del ObjectDict
__all__ = ['settings', 'setup_settings', 'Conf']



