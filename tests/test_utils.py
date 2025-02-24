
import os
import tempfile
import shutil
from contextlib import contextmanager


def _copy_assets(temp_dir, assets):
    for asset in assets:
        shutil.copyfile(
            os.path.join(
                os.path.dirname(__file__),
                asset
            ),
            os.path.join(temp_dir, asset)
        )


@contextmanager
def temp_theme(style_ini_content, assets=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        open(os.path.join(temp_dir, 'style.ini'), 'w').write(style_ini_content)
        if assets:
            _copy_assets(temp_dir, assets)
        yield temp_dir


@contextmanager
def temp_legacy_theme(config_txt_content, assets=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        open(os.path.join(temp_dir, 'config.txt'), 'w').write(config_txt_content)
        if assets:
            _copy_assets(temp_dir, assets)
        yield temp_dir
