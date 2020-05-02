import minio
import rados

class ObjStoreConn():
    def conn(self):
        pass

    def disconn(self):
        pass

    def upload(self, ad_video, ad_video_name):
        pass

class CephConn(ObjStoreConn):
    def __init__(self, ceph_conf_path, ioctx_name):
        self.ceph_conf_path = ceph_conf_path
        self.ioctx_name = ioctx_name
        self.conn = None

    def conn(self):
        self.conn = rados.Rados(conffile=self.ceph_conf_path)
        conn.connect()
        return self

    def disconn(self):
        self.conn.shutdown()
        self.conn = None
        return self

    def upload(self, ad_video, ad_video_name):
        ioctx = cluster.open_ioctx(self.ioctx_name)
        key = hashlib.md5(ad_video_name.encode()).digest()
        ioctx.write_full(key, ad_video)
        ioctx.close()

class MinioConn(ObjStoreConn):
    def __init__(self, host, access_key, secret_key, secure, bucket):
        self.host = host
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.bucket = bucket
        self.conn = None

    def conn(self):
        self.conn = minio.Minio(self.host, self.access_key, self.secret_key, minio_secure)
        return self

    def disconn(self):
        self.conn = None
        return self

    def upload(self, ad_video, ad_video_name):
        self.conn.put_object(self.bucket, ad_video_name, ad_video, ad_video.length)
        return self.conn.presigned_get_object(self.bucket, ad_video_name)
