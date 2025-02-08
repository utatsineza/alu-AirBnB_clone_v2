#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of your
AirBnB Clone repo, using
the function do_pack."""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Function to generate a .tgz archive from the contents of the web_static
    folder."""

    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    archive_path = "versions/web_static_{}.tgz".format(time_stamp)
    local("tar -cvzf {} web_static".format(archive_path))
    if os.path.exists(archive_path):
        return archive_path
    else:
        return None

# Run the script like this:
# $ fab -f 1-pack_web_static.py do_pack
