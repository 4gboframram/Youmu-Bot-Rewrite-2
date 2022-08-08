#    Copyright (C) 2022  4gboframram

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by

#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging


def get_logger(name: str):
    """
    Gets a logger and automatically sets format and output handling based on the configuration file.
    Should be used over logging.getLogger() when possible
    :param name: The name of the logger. Usually __name__.
    :return:
    """
    logger = logging.getLogger(name)
    from ..cfg import get_config

    cfg = get_config()
    logger.setLevel(cfg.logging_info.logging_level)
    out = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s:\t%(message)s")
    out.setFormatter(formatter)
    logger.addHandler(out)
    return logger
