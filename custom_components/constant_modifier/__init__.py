import os
import logging
import importlib

from homeassistant.core import HomeAssistant
from homeassistant.config import load_yaml_config_file, YAML_CONFIG_FILE
from homeassistant.__main__ import get_arguments

LOGGER = logging.getLogger(__name__)
DOMAIN = "constant_modifier"


def setup(hass, config):
    """
    No-op. This code runs way too late to do anything useful.
    """
    return True


def get_ha_config():
    """
    Duplicate enough of the HA startup sequence to extract the config *really* early.
    """

    args = get_arguments()

    hass = HomeAssistant()
    hass.config.config_dir = os.path.abspath(os.path.join(os.getcwd(), args.config))

    return load_yaml_config_file(hass.config.path(YAML_CONFIG_FILE))


def inject(config):
    """
    Patches constants specified as key/value pairs. For example:

    constant_modifier:
      # `MAX_PENDING_MSG` is a top-level constant
      homeassistant.components.websocket_api.http.MAX_PENDING_MSG: 4096

      homeassistant.components.websocket_api.http:
        MAX_PENDING_MSG: 4096  # `MAX_PENDING_MSG` is a top-level constant

      zhaquirks.xiaomi:
        MotionCluster.reset_s: 5  # `MotionCluster` is a class with a `reset_s` attr
    """

    for module_name, replacements in config[DOMAIN].items():
        # Old-style "module.ATTR: value" is replaced with "module: ATTR: value"
        if not isinstance(replacements, dict):
            value = replacements
            module_name, constant = module_name.rsplit(".", 1)
            replacements = {constant: value}

        for path, value in replacements.items():
            *attrs, attr = path.split('.')
            obj = importlib.import_module(module_name)

            for a in attrs:
                obj = getattr(obj, a)

            old_value = getattr(obj, attr)
            setattr(obj, attr, value)

            LOGGER.warning(
                "Patched %s, %s = %s (was %s)",
                module_name,
                path,
                value,
                old_value,
            )


# We are a purposefully a legacy integration so we can run this when we're imported.
# This allows us to run way before anything else has even had a chance to load.
inject(get_ha_config())        
