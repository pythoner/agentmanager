import ConfigParser
import os.path


# FIXME:just a temporary solution to resolve the problem that unit test
# can't load the configuration file
def _get_ut_conf_path(conf_file):
    ut_conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..',
                                                '..',
                                                'etc/',
                                                conf_file)
                                   )
    return ut_conf_path

cf = ConfigParser.ConfigParser()
if not cf.read('/etc/agentmanager/agentmanager.conf'):
    ut_conf_path = _get_ut_conf_path('agentmanager.conf')
    cf.read(ut_conf_path)

lcf = ConfigParser.ConfigParser()
if not lcf.read('/etc/agentmanager/logging.conf'):
    ut_conf_path = _get_ut_conf_path('logging.conf')
    lcf.read(ut_conf_path)


def get_conf(section, option, default=None):
    try:
        conf = cf.get(section, option)
        return conf
    except ConfigParser.Error:
        if default is not None:
            return default
        else:
            raise


def get_conf_int(section, option, default=None):
    conf = get_conf(section, option, default)
    try:
        return int(conf)
    except ValueError:
        msg = 'Config option \'%(option)s\' of section \'%(section)s\' ' \
              'should be integer.'
        raise ValueError(msg % {'section': section, 'option': option})
    except TypeError:
        msg = 'Wrong type filled in config option \'%(option)s\' of section' \
              ' \'%(section)s\'.'
        raise TypeError(msg % {'section': section, 'option': option})


def get_log_conf(section, option, default=None):
    try:
        conf = lcf.get(section, option, raw=True)
        return conf
    except ConfigParser.Error:
        if default is not None:
            return default
        else:
            raise
