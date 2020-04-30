"""
Main interface for s3 service client

Usage::

    import boto3
    from mypy_boto3.s3 import S3Client

    session = boto3.Session()

    client: S3Client = boto3.client("s3")
    session_client: S3Client = session.client("s3")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from datetime import datetime
import sys
from typing import Any, Callable, Dict, IO, List, TYPE_CHECKING, Type, Union, overload
from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_s3.paginator import (
    ListMultipartUploadsPaginator,
    ListObjectVersionsPaginator,
    ListObjectsPaginator,
    ListObjectsV2Paginator,
    ListPartsPaginator,
)
from mypy_boto3_s3.type_defs import (
    AbortMultipartUploadOutputTypeDef,
    AccelerateConfigurationTypeDef,
    AccessControlPolicyTypeDef,
    AnalyticsConfigurationTypeDef,
    BucketLifecycleConfigurationTypeDef,
    BucketLoggingStatusTypeDef,
    CORSConfigurationTypeDef,
    CompleteMultipartUploadOutputTypeDef,
    CompletedMultipartUploadTypeDef,
    CopyObjectOutputTypeDef,
    CopySourceTypeDef,
    CreateBucketConfigurationTypeDef,
    CreateBucketOutputTypeDef,
    CreateMultipartUploadOutputTypeDef,
    DeleteObjectOutputTypeDef,
    DeleteObjectTaggingOutputTypeDef,
    DeleteObjectsOutputTypeDef,
    DeleteTypeDef,
    GetBucketAccelerateConfigurationOutputTypeDef,
    GetBucketAclOutputTypeDef,
    GetBucketAnalyticsConfigurationOutputTypeDef,
    GetBucketCorsOutputTypeDef,
    GetBucketEncryptionOutputTypeDef,
    GetBucketInventoryConfigurationOutputTypeDef,
    GetBucketLifecycleConfigurationOutputTypeDef,
    GetBucketLifecycleOutputTypeDef,
    GetBucketLocationOutputTypeDef,
    GetBucketLoggingOutputTypeDef,
    GetBucketMetricsConfigurationOutputTypeDef,
    GetBucketPolicyOutputTypeDef,
    GetBucketPolicyStatusOutputTypeDef,
    GetBucketReplicationOutputTypeDef,
    GetBucketRequestPaymentOutputTypeDef,
    GetBucketTaggingOutputTypeDef,
    GetBucketVersioningOutputTypeDef,
    GetBucketWebsiteOutputTypeDef,
    GetObjectAclOutputTypeDef,
    GetObjectLegalHoldOutputTypeDef,
    GetObjectLockConfigurationOutputTypeDef,
    GetObjectOutputTypeDef,
    GetObjectRetentionOutputTypeDef,
    GetObjectTaggingOutputTypeDef,
    GetObjectTorrentOutputTypeDef,
    GetPublicAccessBlockOutputTypeDef,
    HeadObjectOutputTypeDef,
    InputSerializationTypeDef,
    InventoryConfigurationTypeDef,
    LifecycleConfigurationTypeDef,
    ListBucketAnalyticsConfigurationsOutputTypeDef,
    ListBucketInventoryConfigurationsOutputTypeDef,
    ListBucketMetricsConfigurationsOutputTypeDef,
    ListBucketsOutputTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListObjectVersionsOutputTypeDef,
    ListObjectsOutputTypeDef,
    ListObjectsV2OutputTypeDef,
    ListPartsOutputTypeDef,
    MetricsConfigurationTypeDef,
    NotificationConfigurationDeprecatedTypeDef,
    NotificationConfigurationTypeDef,
    ObjectLockConfigurationTypeDef,
    ObjectLockLegalHoldTypeDef,
    ObjectLockRetentionTypeDef,
    OutputSerializationTypeDef,
    PublicAccessBlockConfigurationTypeDef,
    PutObjectAclOutputTypeDef,
    PutObjectLegalHoldOutputTypeDef,
    PutObjectLockConfigurationOutputTypeDef,
    PutObjectOutputTypeDef,
    PutObjectRetentionOutputTypeDef,
    PutObjectTaggingOutputTypeDef,
    ReplicationConfigurationTypeDef,
    RequestPaymentConfigurationTypeDef,
    RequestProgressTypeDef,
    RestoreObjectOutputTypeDef,
    RestoreRequestTypeDef,
    ScanRangeTypeDef,
    SelectObjectContentOutputTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    TaggingTypeDef,
    UploadPartCopyOutputTypeDef,
    UploadPartOutputTypeDef,
    VersioningConfigurationTypeDef,
    WebsiteConfigurationTypeDef,
)
from mypy_boto3_s3.waiter import (
    BucketExistsWaiter,
    BucketNotExistsWaiter,
    ObjectExistsWaiter,
    ObjectNotExistsWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("S3Client",)


class Exceptions:
    BucketAlreadyExists: Type[Boto3ClientError]
    BucketAlreadyOwnedByYou: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    NoSuchBucket: Type[Boto3ClientError]
    NoSuchKey: Type[Boto3ClientError]
    NoSuchUpload: Type[Boto3ClientError]
    ObjectAlreadyInActiveTierError: Type[Boto3ClientError]
    ObjectNotInActiveTierError: Type[Boto3ClientError]


class S3Client:
    """
    [S3.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client)
    """

    exceptions: Exceptions

    def abort_multipart_upload(
        self, Bucket: str, Key: str, UploadId: str, RequestPayer: Literal["requester"] = None
    ) -> AbortMultipartUploadOutputTypeDef:
        """
        [Client.abort_multipart_upload documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.abort_multipart_upload)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.can_paginate)
        """

    def complete_multipart_upload(
        self,
        Bucket: str,
        Key: str,
        UploadId: str,
        MultipartUpload: CompletedMultipartUploadTypeDef = None,
        RequestPayer: Literal["requester"] = None,
    ) -> CompleteMultipartUploadOutputTypeDef:
        """
        [Client.complete_multipart_upload documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.complete_multipart_upload)
        """

    def copy(
        self,
        CopySource: CopySourceTypeDef,
        Bucket: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        SourceClient: BaseClient = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Client.copy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.copy)
        """

    def copy_object(
        self,
        Bucket: str,
        CopySource: Union[str, CopySourceTypeDef],
        Key: str,
        ACL: Literal[
            "private",
            "public-read",
            "public-read-write",
            "authenticated-read",
            "aws-exec-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ] = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentType: str = None,
        CopySourceIfMatch: str = None,
        CopySourceIfModifiedSince: datetime = None,
        CopySourceIfNoneMatch: str = None,
        CopySourceIfUnmodifiedSince: datetime = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        MetadataDirective: Literal["COPY", "REPLACE"] = None,
        TaggingDirective: Literal["COPY", "REPLACE"] = None,
        ServerSideEncryption: Literal["AES256", "aws:kms"] = None,
        StorageClass: Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ] = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        CopySourceSSECustomerAlgorithm: str = None,
        CopySourceSSECustomerKey: str = None,
        CopySourceSSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: Literal["GOVERNANCE", "COMPLIANCE"] = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: Literal["ON", "OFF"] = None,
    ) -> CopyObjectOutputTypeDef:
        """
        [Client.copy_object documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.copy_object)
        """

    def create_bucket(
        self,
        Bucket: str,
        ACL: Literal["private", "public-read", "public-read-write", "authenticated-read"] = None,
        CreateBucketConfiguration: CreateBucketConfigurationTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
        ObjectLockEnabledForBucket: bool = None,
    ) -> CreateBucketOutputTypeDef:
        """
        [Client.create_bucket documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.create_bucket)
        """

    def create_multipart_upload(
        self,
        Bucket: str,
        Key: str,
        ACL: Literal[
            "private",
            "public-read",
            "public-read-write",
            "authenticated-read",
            "aws-exec-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ] = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: Literal["AES256", "aws:kms"] = None,
        StorageClass: Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ] = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: Literal["GOVERNANCE", "COMPLIANCE"] = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: Literal["ON", "OFF"] = None,
    ) -> CreateMultipartUploadOutputTypeDef:
        """
        [Client.create_multipart_upload documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.create_multipart_upload)
        """

    def delete_bucket(self, Bucket: str) -> None:
        """
        [Client.delete_bucket documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket)
        """

    def delete_bucket_analytics_configuration(self, Bucket: str, Id: str) -> None:
        """
        [Client.delete_bucket_analytics_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_analytics_configuration)
        """

    def delete_bucket_cors(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_cors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_cors)
        """

    def delete_bucket_encryption(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_encryption documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_encryption)
        """

    def delete_bucket_inventory_configuration(self, Bucket: str, Id: str) -> None:
        """
        [Client.delete_bucket_inventory_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_inventory_configuration)
        """

    def delete_bucket_lifecycle(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_lifecycle documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_lifecycle)
        """

    def delete_bucket_metrics_configuration(self, Bucket: str, Id: str) -> None:
        """
        [Client.delete_bucket_metrics_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_metrics_configuration)
        """

    def delete_bucket_policy(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_policy)
        """

    def delete_bucket_replication(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_replication documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_replication)
        """

    def delete_bucket_tagging(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_tagging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_tagging)
        """

    def delete_bucket_website(self, Bucket: str) -> None:
        """
        [Client.delete_bucket_website documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_bucket_website)
        """

    def delete_object(
        self,
        Bucket: str,
        Key: str,
        MFA: str = None,
        VersionId: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
    ) -> DeleteObjectOutputTypeDef:
        """
        [Client.delete_object documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_object)
        """

    def delete_object_tagging(
        self, Bucket: str, Key: str, VersionId: str = None
    ) -> DeleteObjectTaggingOutputTypeDef:
        """
        [Client.delete_object_tagging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_object_tagging)
        """

    def delete_objects(
        self,
        Bucket: str,
        Delete: DeleteTypeDef,
        MFA: str = None,
        RequestPayer: Literal["requester"] = None,
        BypassGovernanceRetention: bool = None,
    ) -> DeleteObjectsOutputTypeDef:
        """
        [Client.delete_objects documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_objects)
        """

    def delete_public_access_block(self, Bucket: str) -> None:
        """
        [Client.delete_public_access_block documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.delete_public_access_block)
        """

    def download_file(
        self,
        Bucket: str,
        Key: str,
        Filename: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Client.download_file documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.download_file)
        """

    def download_fileobj(
        self,
        Bucket: str,
        Key: str,
        Fileobj: IO[Any],
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Client.download_fileobj documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.download_fileobj)
        """

    def generate_presigned_post(
        self,
        Bucket: str,
        Key: str,
        Fields: Dict[str, Any] = None,
        Conditions: List[Any] = None,
        ExpiresIn: int = 3600,
    ) -> Dict[str, Any]:
        """
        [Client.generate_presigned_post documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.generate_presigned_post)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.generate_presigned_url)
        """

    def get_bucket_accelerate_configuration(
        self, Bucket: str
    ) -> GetBucketAccelerateConfigurationOutputTypeDef:
        """
        [Client.get_bucket_accelerate_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_accelerate_configuration)
        """

    def get_bucket_acl(self, Bucket: str) -> GetBucketAclOutputTypeDef:
        """
        [Client.get_bucket_acl documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_acl)
        """

    def get_bucket_analytics_configuration(
        self, Bucket: str, Id: str
    ) -> GetBucketAnalyticsConfigurationOutputTypeDef:
        """
        [Client.get_bucket_analytics_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_analytics_configuration)
        """

    def get_bucket_cors(self, Bucket: str) -> GetBucketCorsOutputTypeDef:
        """
        [Client.get_bucket_cors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_cors)
        """

    def get_bucket_encryption(self, Bucket: str) -> GetBucketEncryptionOutputTypeDef:
        """
        [Client.get_bucket_encryption documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_encryption)
        """

    def get_bucket_inventory_configuration(
        self, Bucket: str, Id: str
    ) -> GetBucketInventoryConfigurationOutputTypeDef:
        """
        [Client.get_bucket_inventory_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_inventory_configuration)
        """

    def get_bucket_lifecycle(self, Bucket: str) -> GetBucketLifecycleOutputTypeDef:
        """
        [Client.get_bucket_lifecycle documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_lifecycle)
        """

    def get_bucket_lifecycle_configuration(
        self, Bucket: str
    ) -> GetBucketLifecycleConfigurationOutputTypeDef:
        """
        [Client.get_bucket_lifecycle_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_lifecycle_configuration)
        """

    def get_bucket_location(self, Bucket: str) -> GetBucketLocationOutputTypeDef:
        """
        [Client.get_bucket_location documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_location)
        """

    def get_bucket_logging(self, Bucket: str) -> GetBucketLoggingOutputTypeDef:
        """
        [Client.get_bucket_logging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_logging)
        """

    def get_bucket_metrics_configuration(
        self, Bucket: str, Id: str
    ) -> GetBucketMetricsConfigurationOutputTypeDef:
        """
        [Client.get_bucket_metrics_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_metrics_configuration)
        """

    def get_bucket_notification(self, Bucket: str) -> NotificationConfigurationDeprecatedTypeDef:
        """
        [Client.get_bucket_notification documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_notification)
        """

    def get_bucket_notification_configuration(
        self, Bucket: str
    ) -> NotificationConfigurationTypeDef:
        """
        [Client.get_bucket_notification_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_notification_configuration)
        """

    def get_bucket_policy(self, Bucket: str) -> GetBucketPolicyOutputTypeDef:
        """
        [Client.get_bucket_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_policy)
        """

    def get_bucket_policy_status(self, Bucket: str) -> GetBucketPolicyStatusOutputTypeDef:
        """
        [Client.get_bucket_policy_status documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_policy_status)
        """

    def get_bucket_replication(self, Bucket: str) -> GetBucketReplicationOutputTypeDef:
        """
        [Client.get_bucket_replication documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_replication)
        """

    def get_bucket_request_payment(self, Bucket: str) -> GetBucketRequestPaymentOutputTypeDef:
        """
        [Client.get_bucket_request_payment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_request_payment)
        """

    def get_bucket_tagging(self, Bucket: str) -> GetBucketTaggingOutputTypeDef:
        """
        [Client.get_bucket_tagging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_tagging)
        """

    def get_bucket_versioning(self, Bucket: str) -> GetBucketVersioningOutputTypeDef:
        """
        [Client.get_bucket_versioning documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_versioning)
        """

    def get_bucket_website(self, Bucket: str) -> GetBucketWebsiteOutputTypeDef:
        """
        [Client.get_bucket_website documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_bucket_website)
        """

    def get_object(
        self,
        Bucket: str,
        Key: str,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        ResponseCacheControl: str = None,
        ResponseContentDisposition: str = None,
        ResponseContentEncoding: str = None,
        ResponseContentLanguage: str = None,
        ResponseContentType: str = None,
        ResponseExpires: datetime = None,
        VersionId: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
    ) -> GetObjectOutputTypeDef:
        """
        [Client.get_object documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object)
        """

    def get_object_acl(
        self,
        Bucket: str,
        Key: str,
        VersionId: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> GetObjectAclOutputTypeDef:
        """
        [Client.get_object_acl documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object_acl)
        """

    def get_object_legal_hold(
        self,
        Bucket: str,
        Key: str,
        VersionId: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> GetObjectLegalHoldOutputTypeDef:
        """
        [Client.get_object_legal_hold documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object_legal_hold)
        """

    def get_object_lock_configuration(self, Bucket: str) -> GetObjectLockConfigurationOutputTypeDef:
        """
        [Client.get_object_lock_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object_lock_configuration)
        """

    def get_object_retention(
        self,
        Bucket: str,
        Key: str,
        VersionId: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> GetObjectRetentionOutputTypeDef:
        """
        [Client.get_object_retention documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object_retention)
        """

    def get_object_tagging(
        self, Bucket: str, Key: str, VersionId: str = None
    ) -> GetObjectTaggingOutputTypeDef:
        """
        [Client.get_object_tagging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object_tagging)
        """

    def get_object_torrent(
        self, Bucket: str, Key: str, RequestPayer: Literal["requester"] = None
    ) -> GetObjectTorrentOutputTypeDef:
        """
        [Client.get_object_torrent documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_object_torrent)
        """

    def get_public_access_block(self, Bucket: str) -> GetPublicAccessBlockOutputTypeDef:
        """
        [Client.get_public_access_block documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.get_public_access_block)
        """

    def head_bucket(self, Bucket: str) -> None:
        """
        [Client.head_bucket documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.head_bucket)
        """

    def head_object(
        self,
        Bucket: str,
        Key: str,
        IfMatch: str = None,
        IfModifiedSince: datetime = None,
        IfNoneMatch: str = None,
        IfUnmodifiedSince: datetime = None,
        Range: str = None,
        VersionId: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
        PartNumber: int = None,
    ) -> HeadObjectOutputTypeDef:
        """
        [Client.head_object documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.head_object)
        """

    def list_bucket_analytics_configurations(
        self, Bucket: str, ContinuationToken: str = None
    ) -> ListBucketAnalyticsConfigurationsOutputTypeDef:
        """
        [Client.list_bucket_analytics_configurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_bucket_analytics_configurations)
        """

    def list_bucket_inventory_configurations(
        self, Bucket: str, ContinuationToken: str = None
    ) -> ListBucketInventoryConfigurationsOutputTypeDef:
        """
        [Client.list_bucket_inventory_configurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_bucket_inventory_configurations)
        """

    def list_bucket_metrics_configurations(
        self, Bucket: str, ContinuationToken: str = None
    ) -> ListBucketMetricsConfigurationsOutputTypeDef:
        """
        [Client.list_bucket_metrics_configurations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_bucket_metrics_configurations)
        """

    def list_buckets(self) -> ListBucketsOutputTypeDef:
        """
        [Client.list_buckets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_buckets)
        """

    def list_multipart_uploads(
        self,
        Bucket: str,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        KeyMarker: str = None,
        MaxUploads: int = None,
        Prefix: str = None,
        UploadIdMarker: str = None,
    ) -> ListMultipartUploadsOutputTypeDef:
        """
        [Client.list_multipart_uploads documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_multipart_uploads)
        """

    def list_object_versions(
        self,
        Bucket: str,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        KeyMarker: str = None,
        MaxKeys: int = None,
        Prefix: str = None,
        VersionIdMarker: str = None,
    ) -> ListObjectVersionsOutputTypeDef:
        """
        [Client.list_object_versions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_object_versions)
        """

    def list_objects(
        self,
        Bucket: str,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        Marker: str = None,
        MaxKeys: int = None,
        Prefix: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> ListObjectsOutputTypeDef:
        """
        [Client.list_objects documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_objects)
        """

    def list_objects_v2(
        self,
        Bucket: str,
        Delimiter: str = None,
        EncodingType: Literal["url"] = None,
        MaxKeys: int = None,
        Prefix: str = None,
        ContinuationToken: str = None,
        FetchOwner: bool = None,
        StartAfter: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> ListObjectsV2OutputTypeDef:
        """
        [Client.list_objects_v2 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_objects_v2)
        """

    def list_parts(
        self,
        Bucket: str,
        Key: str,
        UploadId: str,
        MaxParts: int = None,
        PartNumberMarker: int = None,
        RequestPayer: Literal["requester"] = None,
    ) -> ListPartsOutputTypeDef:
        """
        [Client.list_parts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.list_parts)
        """

    def put_bucket_accelerate_configuration(
        self, Bucket: str, AccelerateConfiguration: AccelerateConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_accelerate_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_accelerate_configuration)
        """

    def put_bucket_acl(
        self,
        Bucket: str,
        ACL: Literal["private", "public-read", "public-read-write", "authenticated-read"] = None,
        AccessControlPolicy: AccessControlPolicyTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
    ) -> None:
        """
        [Client.put_bucket_acl documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_acl)
        """

    def put_bucket_analytics_configuration(
        self, Bucket: str, Id: str, AnalyticsConfiguration: AnalyticsConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_analytics_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_analytics_configuration)
        """

    def put_bucket_cors(self, Bucket: str, CORSConfiguration: CORSConfigurationTypeDef) -> None:
        """
        [Client.put_bucket_cors documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_cors)
        """

    def put_bucket_encryption(
        self,
        Bucket: str,
        ServerSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef,
        ContentMD5: str = None,
    ) -> None:
        """
        [Client.put_bucket_encryption documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_encryption)
        """

    def put_bucket_inventory_configuration(
        self, Bucket: str, Id: str, InventoryConfiguration: InventoryConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_inventory_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_inventory_configuration)
        """

    def put_bucket_lifecycle(
        self, Bucket: str, LifecycleConfiguration: LifecycleConfigurationTypeDef = None
    ) -> None:
        """
        [Client.put_bucket_lifecycle documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_lifecycle)
        """

    def put_bucket_lifecycle_configuration(
        self, Bucket: str, LifecycleConfiguration: BucketLifecycleConfigurationTypeDef = None
    ) -> None:
        """
        [Client.put_bucket_lifecycle_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_lifecycle_configuration)
        """

    def put_bucket_logging(
        self, Bucket: str, BucketLoggingStatus: BucketLoggingStatusTypeDef
    ) -> None:
        """
        [Client.put_bucket_logging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_logging)
        """

    def put_bucket_metrics_configuration(
        self, Bucket: str, Id: str, MetricsConfiguration: MetricsConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_metrics_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_metrics_configuration)
        """

    def put_bucket_notification(
        self, Bucket: str, NotificationConfiguration: NotificationConfigurationDeprecatedTypeDef
    ) -> None:
        """
        [Client.put_bucket_notification documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_notification)
        """

    def put_bucket_notification_configuration(
        self, Bucket: str, NotificationConfiguration: NotificationConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_notification_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_notification_configuration)
        """

    def put_bucket_policy(
        self, Bucket: str, Policy: str, ConfirmRemoveSelfBucketAccess: bool = None
    ) -> None:
        """
        [Client.put_bucket_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_policy)
        """

    def put_bucket_replication(
        self,
        Bucket: str,
        ReplicationConfiguration: ReplicationConfigurationTypeDef,
        Token: str = None,
    ) -> None:
        """
        [Client.put_bucket_replication documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_replication)
        """

    def put_bucket_request_payment(
        self, Bucket: str, RequestPaymentConfiguration: RequestPaymentConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_request_payment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_request_payment)
        """

    def put_bucket_tagging(self, Bucket: str, Tagging: TaggingTypeDef) -> None:
        """
        [Client.put_bucket_tagging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_tagging)
        """

    def put_bucket_versioning(
        self, Bucket: str, VersioningConfiguration: VersioningConfigurationTypeDef, MFA: str = None
    ) -> None:
        """
        [Client.put_bucket_versioning documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_versioning)
        """

    def put_bucket_website(
        self, Bucket: str, WebsiteConfiguration: WebsiteConfigurationTypeDef
    ) -> None:
        """
        [Client.put_bucket_website documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_bucket_website)
        """

    def put_object(
        self,
        Bucket: str,
        Key: str,
        ACL: Literal[
            "private",
            "public-read",
            "public-read-write",
            "authenticated-read",
            "aws-exec-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ] = None,
        Body: Union[bytes, IO] = None,
        CacheControl: str = None,
        ContentDisposition: str = None,
        ContentEncoding: str = None,
        ContentLanguage: str = None,
        ContentLength: int = None,
        ContentMD5: str = None,
        ContentType: str = None,
        Expires: datetime = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWriteACP: str = None,
        Metadata: Dict[str, str] = None,
        ServerSideEncryption: Literal["AES256", "aws:kms"] = None,
        StorageClass: Literal[
            "STANDARD",
            "REDUCED_REDUNDANCY",
            "STANDARD_IA",
            "ONEZONE_IA",
            "INTELLIGENT_TIERING",
            "GLACIER",
            "DEEP_ARCHIVE",
        ] = None,
        WebsiteRedirectLocation: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        SSEKMSKeyId: str = None,
        SSEKMSEncryptionContext: str = None,
        RequestPayer: Literal["requester"] = None,
        Tagging: str = None,
        ObjectLockMode: Literal["GOVERNANCE", "COMPLIANCE"] = None,
        ObjectLockRetainUntilDate: datetime = None,
        ObjectLockLegalHoldStatus: Literal["ON", "OFF"] = None,
    ) -> PutObjectOutputTypeDef:
        """
        [Client.put_object documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_object)
        """

    def put_object_acl(
        self,
        Bucket: str,
        Key: str,
        ACL: Literal[
            "private",
            "public-read",
            "public-read-write",
            "authenticated-read",
            "aws-exec-read",
            "bucket-owner-read",
            "bucket-owner-full-control",
        ] = None,
        AccessControlPolicy: AccessControlPolicyTypeDef = None,
        GrantFullControl: str = None,
        GrantRead: str = None,
        GrantReadACP: str = None,
        GrantWrite: str = None,
        GrantWriteACP: str = None,
        RequestPayer: Literal["requester"] = None,
        VersionId: str = None,
    ) -> PutObjectAclOutputTypeDef:
        """
        [Client.put_object_acl documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_object_acl)
        """

    def put_object_legal_hold(
        self,
        Bucket: str,
        Key: str,
        LegalHold: ObjectLockLegalHoldTypeDef = None,
        RequestPayer: Literal["requester"] = None,
        VersionId: str = None,
        ContentMD5: str = None,
    ) -> PutObjectLegalHoldOutputTypeDef:
        """
        [Client.put_object_legal_hold documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_object_legal_hold)
        """

    def put_object_lock_configuration(
        self,
        Bucket: str,
        ObjectLockConfiguration: ObjectLockConfigurationTypeDef = None,
        RequestPayer: Literal["requester"] = None,
        Token: str = None,
        ContentMD5: str = None,
    ) -> PutObjectLockConfigurationOutputTypeDef:
        """
        [Client.put_object_lock_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_object_lock_configuration)
        """

    def put_object_retention(
        self,
        Bucket: str,
        Key: str,
        Retention: ObjectLockRetentionTypeDef = None,
        RequestPayer: Literal["requester"] = None,
        VersionId: str = None,
        BypassGovernanceRetention: bool = None,
        ContentMD5: str = None,
    ) -> PutObjectRetentionOutputTypeDef:
        """
        [Client.put_object_retention documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_object_retention)
        """

    def put_object_tagging(
        self,
        Bucket: str,
        Key: str,
        Tagging: TaggingTypeDef,
        VersionId: str = None,
        ContentMD5: str = None,
    ) -> PutObjectTaggingOutputTypeDef:
        """
        [Client.put_object_tagging documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_object_tagging)
        """

    def put_public_access_block(
        self,
        Bucket: str,
        PublicAccessBlockConfiguration: PublicAccessBlockConfigurationTypeDef,
        ContentMD5: str = None,
    ) -> None:
        """
        [Client.put_public_access_block documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.put_public_access_block)
        """

    def restore_object(
        self,
        Bucket: str,
        Key: str,
        VersionId: str = None,
        RestoreRequest: RestoreRequestTypeDef = None,
        RequestPayer: Literal["requester"] = None,
    ) -> RestoreObjectOutputTypeDef:
        """
        [Client.restore_object documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.restore_object)
        """

    def select_object_content(
        self,
        Bucket: str,
        Key: str,
        Expression: str,
        ExpressionType: Literal["SQL"],
        InputSerialization: InputSerializationTypeDef,
        OutputSerialization: OutputSerializationTypeDef,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestProgress: RequestProgressTypeDef = None,
        ScanRange: ScanRangeTypeDef = None,
    ) -> SelectObjectContentOutputTypeDef:
        """
        [Client.select_object_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.select_object_content)
        """

    def upload_file(
        self,
        Filename: str,
        Bucket: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Client.upload_file documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.upload_file)
        """

    def upload_fileobj(
        self,
        Fileobj: IO[Any],
        Bucket: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = None,
        Callback: Callable[..., Any] = None,
        Config: TransferConfig = None,
    ) -> None:
        """
        [Client.upload_fileobj documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.upload_fileobj)
        """

    def upload_part(
        self,
        Bucket: str,
        Key: str,
        PartNumber: int,
        UploadId: str,
        Body: Union[bytes, IO] = None,
        ContentLength: int = None,
        ContentMD5: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> UploadPartOutputTypeDef:
        """
        [Client.upload_part documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.upload_part)
        """

    def upload_part_copy(
        self,
        Bucket: str,
        CopySource: Union[str, CopySourceTypeDef],
        Key: str,
        PartNumber: int,
        UploadId: str,
        CopySourceIfMatch: str = None,
        CopySourceIfModifiedSince: datetime = None,
        CopySourceIfNoneMatch: str = None,
        CopySourceIfUnmodifiedSince: datetime = None,
        CopySourceRange: str = None,
        SSECustomerAlgorithm: str = None,
        SSECustomerKey: str = None,
        SSECustomerKeyMD5: str = None,
        CopySourceSSECustomerAlgorithm: str = None,
        CopySourceSSECustomerKey: str = None,
        CopySourceSSECustomerKeyMD5: str = None,
        RequestPayer: Literal["requester"] = None,
    ) -> UploadPartCopyOutputTypeDef:
        """
        [Client.upload_part_copy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Client.upload_part_copy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_uploads"]
    ) -> ListMultipartUploadsPaginator:
        """
        [Paginator.ListMultipartUploads documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Paginator.ListMultipartUploads)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_object_versions"]
    ) -> ListObjectVersionsPaginator:
        """
        [Paginator.ListObjectVersions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Paginator.ListObjectVersions)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_objects"]) -> ListObjectsPaginator:
        """
        [Paginator.ListObjects documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Paginator.ListObjects)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_objects_v2"]) -> ListObjectsV2Paginator:
        """
        [Paginator.ListObjectsV2 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Paginator.ListObjectsV2)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_parts"]) -> ListPartsPaginator:
        """
        [Paginator.ListParts documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Paginator.ListParts)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["bucket_exists"]) -> BucketExistsWaiter:
        """
        [Waiter.BucketExists documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Waiter.BucketExists)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["bucket_not_exists"]) -> BucketNotExistsWaiter:
        """
        [Waiter.BucketNotExists documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Waiter.BucketNotExists)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["object_exists"]) -> ObjectExistsWaiter:
        """
        [Waiter.ObjectExists documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Waiter.ObjectExists)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["object_not_exists"]) -> ObjectNotExistsWaiter:
        """
        [Waiter.ObjectNotExists documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.0/reference/services/s3.html#S3.Waiter.ObjectNotExists)
        """
