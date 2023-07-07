# ZipFolders MkDocs Plugin

The `ZipFolders` plugin is used to zip specified folders in your MkDocs project after the site build process. This can be helpful if you need to distribute or backup parts of your documentation.

![Plugin](https://raw.githubusercontent.com/JakubAndrysek/mkdocs-zip-folders/main/docs/assets/plugin.png)

## Installation

Install the plugin using pip from [PyPI](https://pypi.org/project/mkdocs-zip-folders/):

```bash
pip install mkdocs-zip-folders
```

## Configuration

To use the `ZipFolders` plugin, you need to add it to your `mkdocs.yml` configuration file.

Here is a sample configuration:

```yaml
plugins:
  - search
  - zip_folders:
      folders:
        - myCode
        - toShare
        - folderX/thisWillBeZipped
      hash_extension: ".zip.hash" # default extension
      debug: true # optional - default is false
```

- `folders` - A list of folders to zip. The folders are relative to the root of the MkDocs documentation project - docs_dir (default is `docs`).
- `debug` - Optional. If set to `true`, the plugin will print debug messages to the console. Default is `false`.
- `hash_extension` - The extension to use for hashing folders. Default is `.zip.hash`.


## Git configuration

It is highly recommended to add the `*.zip`, `*.zip.hash` filses to your `.gitignore` file. This will prevent you from accidentally committing the zip files to your repository.

Zip files will be generated automatically after each build.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Do You Enjoy My Work?
Then definitely consider:

- supporting me on GitHub Sponsors: [![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/jakubandrysek)

## License

[MIT](https://choosealicense.com/licenses/mit/)
