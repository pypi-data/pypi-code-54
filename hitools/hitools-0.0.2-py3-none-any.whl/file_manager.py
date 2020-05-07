import os
import gzip
import time
import sys
import boto3
import ujson as json

class FileManager():
    """
    Utility function which receives market data, stores in temporary
    files and then uploads to s3
    """

    def __init__(self,
                 market,
                 msg_queue,
                 write_time=3600,
                 data_dir='data',
                 bucket=None
                 ):
        """
        :param market: the market name our queue subscribes to
        :param msg_queue: queue from which events will come
        :param write_time: time after files will be uploaded to s3
        :param data_dir: directory to store temporary files
        :param bucket: s3 bucket name
        """
        self.market = market
        self.msg_queue = msg_queue
        self.write_time = write_time
        self.data_dir = data_dir
        self.bucket = bucket
        self.uploading_files = []

    def _next_file(self):
        if self.write_time == 3600:
            file_dir = time.strftime("%Y/%m/%d-%H")
        else:
            file_dir = time.strftime("%Y/%m/%d-%H-%M")
        self.next_upload = int(time.time()) + self.write_time
        self.file_name = os.path.join(self.data_dir, self.market,
                                      '%s.txt.gz' % file_dir)
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
        self.file = gzip.open(self.file_name, 'a')

    def _upload(self, bucket):
        try_later_queue = []


        for uploading in self.uploading_files:
            try:
                response = (bucket
                            .Object(uploading.name)
                            .put(Body=open(uploading.name, 'rb')))
                if (response.get('ResponseMetadata', {})
                            .get('HTTPStatusCode') == 200):
                    print("Uploaded %s, size: %d byte" %
                          (uploading.name, os.path.getsize(uploading.name)))

                    sys.stdout.flush()

                    os.remove(uploading.name)
            except Exception as e:
                print(e)
                sys.stdout.flush()

                try_later_queue.append(uploading)
        self.uploading_files = try_later_queue

    def start(self, run_time_seconds=None):
        """
        starts creating files and dumping jsons
        :param run_time_seconds: seconds to run the file manager,
                                 pass 0 if forever
        """


        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket)

        prefix = os.path.join(self.data_dir, self.market)

        print('There are already {} objects in the directory.'
              .format(len(list(bucket.objects.filter(Prefix=prefix)))))

        sys.stdout.flush()
        self._next_file()
        start = time.time()
        while True:
            while not self.msg_queue.empty():
                self.file.write((json.dumps(self.msg_queue.get()) + '\n')
                                .encode())


            if int(time.time()) > self.next_upload:


                uploading = self.file
                self._next_file()

                uploading.close()
                self.uploading_files.append(uploading)
                self._upload(bucket=bucket)
            if run_time_seconds:
                if time.time() - start > run_time_seconds:
                    break

            time.sleep(1)
