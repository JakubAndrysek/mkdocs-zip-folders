# Author: Jakub Andrýsek
# Email: email@kubaandrysek.cz
# Website: https://kubaandrysek.cz
# License: MIT
# GitHub: https://github.com/JakubAndrysek/mkdocs-typedoc
# PyPI: https://pypi.org/project/mkdocs-typedoc/
import os
import zipfile
import logging

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

log: logging.Logger = logging.getLogger("mkdocs")

class ZipFoldersPlugin(BasePlugin):
    config_scheme = (
        ('folders', config_options.Type(list, default=[])),
        ('debug', config_options.Type(bool, default=False)),
    )

    def on_post_build(self, config):
        folders = self.config['folders']

        for folder in folders:
            path = os.path.join(config['docs_dir'], folder)
            if not os.path.exists(path):
                print(f"The folder {folder} does not exist.")
                continue

            self.zip_folder(path, self.config['debug'])

        return config

    @staticmethod
    def zip_folder(folder, debug=False):
        # Use os.path.basename to include the root directory in the zip file
        root_dir = os.path.basename(folder)
        zipf = zipfile.ZipFile(f'{folder}.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                # Create the file path relative to the root directory
                relpath = os.path.relpath(dirpath, os.path.dirname(folder))
                zipf.write(os.path.join(dirpath, filename), arcname=os.path.join(root_dir, relpath, filename))
        zipf.close()

        if debug:
            log.info(f"Zipped {folder} into {folder}.zip")