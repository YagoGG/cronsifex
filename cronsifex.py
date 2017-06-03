import os
import tempfile

import requests
from requests.auth import HTTPBasicAuth
import six.moves.configparser as configparser


config = configparser.ConfigParser()
config.read('conf.ini')

tfx_user = config.get('transifex', 'username')
tfx_pass = config.get('transifex', 'password')
project = config.get('transifex', 'project_slug')

TFX_API_BASE = 'https://www.transifex.com/api/2'
auth = HTTPBasicAuth(tfx_user, tfx_pass)


def download_file(url):
    """Download a remote file, and return the OS-level handle of a local
    temporary file, with the contents of the remote file.
    """
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise RuntimeError(('Couldn\'t fetch the remote file from "%s" '
                            '(Reason: %s).') % (url, r.text.strip()))

    file = tempfile.NamedTemporaryFile(delete=False)

    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)

    file.seek(0)
    return file


def update_resource(project, slug, file):
    """Upload an already existing resource to Transifex, to upldate its
    contents.
    """
    f = {'file': (file.name, file, 'multipart/form-data')}
    r = requests.put(TFX_API_BASE +
                     ('/project/%s/resource/%s/content' % (project, slug)),
                     auth=auth, files=f)

    if r.status_code != 200:
        raise RuntimeError('Couldn\'t update the resource "%s" (Reason: %s).' %
                           (slug, r.text.strip()))


if __name__ == '__main__':
    resources = config.items('resources')

    for (slug, url) in resources:
        print('Uploading resource "%s"...' % slug)

        print('> Download new file from "%s"' % url)
        remote_file = download_file(url)

        print('> Upload new file to the project "%s" in Transifex' % project)
        update_resource(project, slug, remote_file)

        remote_file.close()
        os.remove(remote_file.name)  # Delete the temporary file
