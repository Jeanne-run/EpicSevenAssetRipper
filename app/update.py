from .constants     import VERSION
import json
import re
import os
from urllib.request import urlopen, Request

def github_version_to_float(version: str):
    version = ''.join(version.rsplit('.', 1))
    return float( version )

def update_check():
    resp = None
    versions = []

    LOCAL_VERSION = float(VERSION)

    try:
        with urlopen(
            Request(
                #'https://raw.githubusercontent.com/CeciliaBot/EpicSevenAssetRipper/refs/heads/main/requirements.txt',
                'https://api.github.com/repos/CeciliaBot/EpicSevenAssetRipper/releases',
                method='GET'
            )
        ) as f:
            resp = json.loads(f.read())

        if resp:
            for release in resp:
                v = github_version_to_float(release['name'])
                if v < LOCAL_VERSION:
                    versions.append({
                        'version': v,
                        'date': release['published_at'], # release['created_at'],
                        'changelog': release['body'],
                        'url': [ i['browser_download_url'] for i in release['assets'] if re.search(r'\.zip$', i['browser_download_url'], re.IGNORECASE)]
                    })

        return versions

    except Exception as e:
        print('Error in update checker')
        print(e)

def download_update(url: str):
        with urlopen(
            Request(
                url,
                method='GET'
            )
        ) as r:
            with open('.patch.zip', 'wb') as f:
                f.write(r.read())

def unpack_update():
    '''
        Unpack an update for this tool if found in the local path
    '''
    if os.path.isfile('./.patch.zip'):
        print('Applying patch')
        import zipfile
        f = zipfile.ZipFile(file='./.patch.zip', mode='r')
        f.extractall('./test/', f.namelist())
        f.close()
        os.remove('./.patch.zip')
        print('Patch complete')
    else:
        pass