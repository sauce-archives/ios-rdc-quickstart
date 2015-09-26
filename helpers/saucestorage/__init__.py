# Copyright 2015 Sauce Labs.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# http://www.apache.org/licenses/LICENSE-2.0


# -----------------
# Based on sauceclient by Corey Goldberg
# https://github.com/cgoldberg/sauceclient
# ----------------


# Sauce Labs REST API documentation:
# http://saucelabs.com/docs/rest


import base64
import hashlib
import json
import logging
import os.path
import sys
import urllib

__version__ = '0.1'

is_py2 = sys.version_info.major is 2
log = logging.getLogger(__name__)

if is_py2:
    import httplib as http_client
else:
    import http.client as http_client

SAUCE_API_ENDPOINT = "saucelabs.com"


def json_loads(json_data):
    if not is_py2:
        json_data = json_data.decode(encoding='UTF-8')
    return json.loads(json_data)


class SauceException(Exception):
    pass


class SauceStorageClient(object):
    def __init__(self, username, access_key, api_endpoint=SAUCE_API_ENDPOINT):
        self.api_endpoint = api_endpoint
        self.access_key = access_key
        self.username = username

    def get_method_url(self, group, path=None, query=None):
        url = '/rest/v1/%s/%s' % (group, self.username)
        if path is not None:
            url = url + '/' + path
        if query is not None:
            url = url + '?' + urllib.urlencode(query)
        return url

    def get_headers(self, content_type):
        base64string = self.get_encoded_auth_string()
        headers = {
            'Authorization': 'Basic %s' % base64string
        }
        headers['Content-Type'] = content_type
        return headers

    def request(self, method, url, body=None, content_type='application/json'):
        connection = http_client.HTTPSConnection(self.api_endpoint)
        headers = self.get_headers(content_type)
        log.debug("{}ing {}...".format(method, url))
        connection.request(method, url, body, headers=headers)
        response = connection.getresponse()
        json_data = response.read()
        connection.close()
        if response.status != 200:
            raise SauceException('%s: %s.\nSauce Status NOT OK' %
                                 (response.status, response.reason))
        return json_data

    def get_encoded_auth_string(self):
        auth_info = '%s:%s' % (self.username, self.access_key)
        if is_py2:
            base64string = base64.encodestring(auth_info)[:-1]
        else:
            base64string = base64.b64encode(auth_info.encode(encoding='UTF-8')).decode(encoding='UTF-8')
        return base64string

    def get_file_md5(self, file_path, block_size=2**20):
        digest = hashlib.md5()
        with open(os.path.join(file_path), "rb") as f:
            while True:
                buf = f.read(block_size)
                if not buf:
                    break
                digest.update(buf)
        return digest.hexdigest()

    #
    # API METHODS
    #

    def list(self):
        """ List all files in storage """
        url = self.get_method_url('storage')
        json_data = self.request('GET', url)
        result = json_loads(json_data)
        return result['files']

    def put(self, file_path, file_name=None, overwrite=True, verify=False):
        """ Upload a file to storage """
        if file_name is None:
            file_name = os.path.basename(file_path)
        query = None
        if overwrite:
            query = {'overwrite': 'true'}
        url = self.get_method_url('storage', path=file_name, query=query)
        with open(file_path, 'r') as body:
            json_data = self.request('POST',
                                     url,
                                     body=body,
                                     content_type='application/octet-stream')
        result = json_loads(json_data)
        if verify:
            local_hash = self.get_file_md5(file_path)
            remote_hash = result['md5']
            if local_hash != remote_hash:
                msg = "Uploaded, but md5 hashes differ. Expected {}, upload server returned {}"
                raise Exception(msg.format(local_hash, remote_hash))
        # add the sauce-storage URL
        result['url'] = 'sauce-storage:' + result['filename']
        return result
