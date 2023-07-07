# Author: Jakub Andrýsek
# Email: email@kubaandrysek.cz
# Website: https://kubaandrysek.cz
# License: MIT
# GitHub: https://github.com/JakubAndrysek/mkdocs-typedoc
# PyPI: https://pypi.org/project/mkdocs-typedoc/

import os
import zipfile
import hashlib
import logging

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

log: logging.Logger = logging.getLogger("mkdocs")


class ZipFoldersPlugin(BasePlugin):
    config_scheme = (
        ('folders', config_options.Type(list, default=[])),
        ('debug', config_options.Type(bool, default=False)),
        ('hash_extension', config_options.Type(str, default='.zip.hash')),
    )

    def on_post_build(self, config):
        folders = self.config['folders']

        for folder in folders:
            path = os.path.join(config['docs_dir'], folder)
            if not os.path.exists(path):
                print(f"The folder {folder} does not exist.")
                continue

            zip_path = f'{path}.zip'
            hash_path = f'{path}{self.config["hash_extension"]}'

            if os.path.exists(zip_path) and os.path.exists(hash_path):
                with open(hash_path, 'r') as f:
                    old_hash = f.read().strip()

                new_hash = self.hash_file(zip_path)

                if old_hash == new_hash:
                    if self.config['debug']:
                        log.info(f"Skipping {folder} as it has not changed.")
                    continue

            self.zip_folder(path, self.config['debug'])

            # Compute and store new hash
            with open(hash_path, 'w') as f:
                f.write(self.hash_file(zip_path))

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

    @staticmethod
    def hash_file(filepath):
        BUF_SIZE = 65536  # Let's read stuff in 64kb chunks!
        sha256 = hashlib.sha256()

        with open(filepath, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()
