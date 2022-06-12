import os
from mmm.management.command import cli


if __name__ == '__main__':
    os.environ.get('MMM_SETTINGS_MODULE', 'settings')
    cli()
