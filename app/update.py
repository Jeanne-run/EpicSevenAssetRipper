from .constants     import VERSION
import json
import re
import os
from pathlib import Path
from urllib.request import urlopen, Request

def github_version_to_float(version: str):
    version = ''.join(version.rsplit('.', 1)) if version.count('.') > 1 else version
    return float( version )

def update_check():
    resp = None
    versions = []

    LOCAL_VERSION = float(VERSION)

    try:
        with urlopen(
            Request( 'https://api.github.com/repos/CeciliaBot/EpicSevenAssetRipper/releases', method='GET')
        ) as f:
            resp = json.loads(f.read())

        if resp:
            for release in resp:
                v = github_version_to_float(release['name'])
                if v > LOCAL_VERSION:
                    versions.append({
                        'version': v,
                        'date': release['published_at'], # release['created_at'],
                        'changelog': release['body'],
                        'url': [ i['browser_download_url'] for i in release['assets'] if re.search(r'\.zip$', i['browser_download_url'], re.IGNORECASE)],
                        'zip_source': release['zipball_url']
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

        with zipfile.ZipFile(file='./.patch.zip', mode='r') as zip:
            filter = zipfile.Path(zip).iterdir()
            root_folders = [ i for i in filter]

            if len(root_folders) == 1:
                filter = root_folders[0].name + '/'
            else:
                filter = ''
            
            for file in zip.namelist():
                if file.startswith(filter):
                    destination_name = file.replace(filter, '') if filter != '' else file
                    dest_path = os.path.join('./', destination_name)
                    print('Extracting', destination_name, '...')
                    info = zip.getinfo(file)
                    if info.is_dir():
                        Path(dest_path).mkdir(parents=True, exist_ok=True)
                    else:
                        with open(dest_path, 'wb') as f:
                            f.write( zip.read( info ) )

        os.remove('./.patch.zip')
        print('Patch complete')
    else:
        pass