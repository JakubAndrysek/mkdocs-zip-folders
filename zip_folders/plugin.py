# Author: Jakub Andrýsek
# Email: email@kubaandrysek.cz
# Website: https://kubaandrysek.cz
# License: MIT
# GitHub: https://github.com/JakubAndrysek/mkdocs-typedoc
# PyPI: https://pypi.org/project/mkdocs-typedoc/

import os
import zipfile
import tarfile
import hashlib
import logging

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

log: logging.Logger = logging.getLogger("mkdocs")


class PlaceholderFile(File):
    def copy_file(self, *args, **kwargs):
        pass


class ZipFoldersPlugin(BasePlugin):
    config_scheme = (
        ('folders', config_options.Type(list, default=[])),
        ('debug', config_options.Type(bool, default=False)),
        ('hash_extension', config_options.Type(str, default='.hash')),
        ('formats', config_options.Type(list, default=['zip'])),
    )

    def on_files(self, files, config):
        folders = self.config['folders']
        formats = self.config['formats']

        for folder in folders:
            for format_type in formats:
                if format_type == 'zip':
                    ext = '.zip'
                elif format_type == 'tar.gz':
                    ext = '.tar.gz'
                else:
                    log.warning(f"Unsupported format: {format_type}")
                    continue

                files.append(PlaceholderFile.generated(
                    config,
                    f'{folder}{ext}',
                    abs_src_path=os.path.join(config['site_dir'],
                                              f'{folder}{ext}')
                ))

    def on_post_build(self, config):
        folders = self.config['folders']
        formats = self.config['formats']

        for folder in folders:
            path = os.path.join(config['site_dir'], folder)
            if not os.path.exists(path):
                log.warning(f"The folder {folder} does not exist.")
                continue

            for format_type in formats:
                if format_type == 'zip':
                    ext = '.zip'
                elif format_type == 'tar.gz':
                    ext = '.tar.gz'
                else:
                    log.warning(f"Unsupported format: {format_type}")
                    continue

                archive_path = f'{path}{ext}'
                hash_path = f'{path}{ext}{self.config["hash_extension"]}'

                if os.path.exists(archive_path) and os.path.exists(hash_path):
                    with open(hash_path, 'r') as f:
                        old_hash = f.read().strip()

                    new_hash = self.hash_file(archive_path)

                    if old_hash == new_hash:
                        if self.config['debug']:
                            log.info(f"Skipping {folder}{ext} as it has not "
                                     f"changed.")
                        continue

                self.create_archive(path, format_type, self.config['debug'])

                # Compute and store new hash
                with open(hash_path, 'w') as f:
                    f.write(self.hash_file(archive_path))

        return config

    @staticmethod
    def create_archive(folder, format_type, debug=False):
        if format_type == 'zip':
            ZipFoldersPlugin._create_zip(folder, debug)
        elif format_type == 'tar.gz':
            ZipFoldersPlugin._create_tar_gz(folder, debug)
        else:
            log.warning(f"Unsupported format: {format_type}")

    @staticmethod
    def _create_zip(folder, debug=False):
        zipf = zipfile.ZipFile(f'{folder}.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                # Create the file path relative to the root directory
                relpath = os.path.relpath(dirpath, folder)
                file_path = os.path.join(dirpath, filename)
                arc_path = os.path.join(relpath, filename)
                zipf.write(file_path, arcname=arc_path)
        zipf.close()

        if debug:
            log.info(f"Zipped {folder} into {folder}.zip")

    @staticmethod
    def _create_tar_gz(folder, debug=False):
        tar_path = f'{folder}.tar.gz'
        with tarfile.open(tar_path, 'w:gz') as tar:
            for dirpath, dirnames, filenames in os.walk(folder):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    # Create archive name relative to the folder
                    arcname = os.path.relpath(file_path, folder)
                    tar.add(file_path, arcname=arcname)

        if debug:
            log.info(f"Created tar.gz {folder} into {tar_path}")

    @staticmethod
    def zip_folder(folder, debug=False):
        """Deprecated: Use create_archive instead"""
        ZipFoldersPlugin._create_zip(folder, debug)

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
