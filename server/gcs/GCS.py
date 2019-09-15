from google.cloud import storage

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('./gcs/realtalk-c580fb239c1b.json')

    #print(buckets = list(storage_client.list_buckets())
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    #returns a public url
    return blob.public_url

def upload_stream_to_bucket(blob_name, stream, bucket_name):
    chunk_size = 256 * 1024
    # Create a Resumable Upload
