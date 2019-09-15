import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity


class GCS:
    def __init__(self):

        return

    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_.name())

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Demo GCS Application running from Version: ' + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')

    def create_file(self, filename):
        """Create a file.

        The retry_params specified in the open call will override the default
        retry params for this particular file handle.

        Args:
          filename: filename.
        """
        self.response.write('Creating file %s\n' % filename)

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename, 'w', content_type='text/plain', options={'x-goog-meta-foo': 'foo','x-goog-meta-bar': 'bar'}, retry_params=write_retry_params)
        gcs_file.write('abcde\n')
        gcs_file.write('f'*1024*4 + '\n')
        gcs_file.close()
        self.tmp_filenames_to_clean_up.append(filename)


    def read_file(self, filename):
        self.response.write('Reading the full file contents:\n')

        gcs_file = gcs.open(filename)
        contents = gcs_file.read()
        gcs_file.close()
        self.response.write(contents)
    def list_bucket(self, bucket):
        """Create several files and paginate through them.

        Production apps should set page_size to a practical value.

        Args:
            bucket: bucket.
        """
        self.response.write('Listbucket result:\n')

        page_size = 1
        stats = gcs.listbucket(bucket + '/foo', max_keys=page_size)
        while True:
            count = 0
            for stat in stats:
                count += 1
                self.response.write(repr(stat))
                self.response.write('\n')

            if count != page_size or count == 0:
                break
            stats = gcs.listbucket(bucket + '/foo', max_keys=page_size, marker=stat.filename)




