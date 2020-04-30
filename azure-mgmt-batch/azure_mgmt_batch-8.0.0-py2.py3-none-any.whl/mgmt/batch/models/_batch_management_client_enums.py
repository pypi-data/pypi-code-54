# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from enum import Enum


class KeySource(str, Enum):

    microsoft_batch = "Microsoft.Batch"  #: Batch creates and manages the encryption keys used to protect the account data.
    microsoft_key_vault = "Microsoft.KeyVault"  #: The encryption keys used to protect the account data are stored in an external key vault.


class PoolAllocationMode(str, Enum):

    batch_service = "BatchService"  #: Pools will be allocated in subscriptions owned by the Batch service.
    user_subscription = "UserSubscription"  #: Pools will be allocated in a subscription owned by the user.


class PublicNetworkAccessType(str, Enum):

    enabled = "Enabled"  #: Enables connectivity to Azure Batch through public DNS.
    disabled = "Disabled"  #: Disables public connectivity and enables private connectivity to Azure Batch Service through private endpoint resource.


class ProvisioningState(str, Enum):

    invalid = "Invalid"  #: The account is in an invalid state.
    creating = "Creating"  #: The account is being created.
    deleting = "Deleting"  #: The account is being deleted.
    succeeded = "Succeeded"  #: The account has been created and is ready for use.
    failed = "Failed"  #: The last operation for the account is failed.
    cancelled = "Cancelled"  #: The last operation for the account is cancelled.


class PrivateEndpointConnectionProvisioningState(str, Enum):

    succeeded = "Succeeded"  #: The connection status is final and is ready for use if Status is Approved.
    updating = "Updating"  #: The user has requested that the connection status be updated, but the update operation has not yet completed. You may not reference the connection when connecting the Batch account.
    failed = "Failed"  #: The user requested that the connection be updated and it failed. You may retry the update operation.


class PrivateLinkServiceConnectionStatus(str, Enum):

    approved = "Approved"  #: The private endpoint connection is approved and can be used to access Batch account
    pending = "Pending"  #: The private endpoint connection is pending and cannot be used to access Batch account
    rejected = "Rejected"  #: The private endpoint connection is rejected and cannot be used to access Batch account
    disconnected = "Disconnected"  #: The private endpoint connection is disconnected and cannot be used to access Batch account


class AccountKeyType(str, Enum):

    primary = "Primary"  #: The primary account key.
    secondary = "Secondary"  #: The secondary account key.


class PackageState(str, Enum):

    pending = "Pending"  #: The application package has been created but has not yet been activated.
    active = "Active"  #: The application package is ready for use.


class CertificateFormat(str, Enum):

    pfx = "Pfx"  #: The certificate is a PFX (PKCS#12) formatted certificate or certificate chain.
    cer = "Cer"  #: The certificate is a base64-encoded X.509 certificate.


class CertificateProvisioningState(str, Enum):

    succeeded = "Succeeded"  #: The certificate is available for use in pools.
    deleting = "Deleting"  #: The user has requested that the certificate be deleted, but the delete operation has not yet completed. You may not reference the certificate when creating or updating pools.
    failed = "Failed"  #: The user requested that the certificate be deleted, but there are pools that still have references to the certificate, or it is still installed on one or more compute nodes. (The latter can occur if the certificate has been removed from the pool, but the node has not yet restarted. Nodes refresh their certificates only when they restart.) You may use the cancel certificate delete operation to cancel the delete, or the delete certificate operation to retry the delete.


class PoolProvisioningState(str, Enum):

    succeeded = "Succeeded"  #: The pool is available to run tasks subject to the availability of compute nodes.
    deleting = "Deleting"  #: The user has requested that the pool be deleted, but the delete operation has not yet completed.


class AllocationState(str, Enum):

    steady = "Steady"  #: The pool is not resizing. There are no changes to the number of nodes in the pool in progress. A pool enters this state when it is created and when no operations are being performed on the pool to change the number of nodes.
    resizing = "Resizing"  #: The pool is resizing; that is, compute nodes are being added to or removed from the pool.
    stopping = "Stopping"  #: The pool was resizing, but the user has requested that the resize be stopped, but the stop request has not yet been completed.


class CachingType(str, Enum):

    none = "None"  #: The caching mode for the disk is not enabled.
    read_only = "ReadOnly"  #: The caching mode for the disk is read only.
    read_write = "ReadWrite"  #: The caching mode for the disk is read and write.


class StorageAccountType(str, Enum):

    standard_lrs = "Standard_LRS"  #: The data disk should use standard locally redundant storage.
    premium_lrs = "Premium_LRS"  #: The data disk should use premium locally redundant storage.


class DiskEncryptionTarget(str, Enum):

    os_disk = "OsDisk"  #: The OS Disk on the compute node is encrypted.
    temporary_disk = "TemporaryDisk"  #: The temporary disk on the compute node is encrypted. On Linux this encryption applies to other partitions (such as those on mounted data disks) when encryption occurs at boot time.


class ComputeNodeDeallocationOption(str, Enum):

    requeue = "Requeue"  #: Terminate running task processes and requeue the tasks. The tasks will run again when a node is available. Remove nodes as soon as tasks have been terminated.
    terminate = "Terminate"  #: Terminate running tasks. The tasks will be completed with failureInfo indicating that they were terminated, and will not run again. Remove nodes as soon as tasks have been terminated.
    task_completion = "TaskCompletion"  #: Allow currently running tasks to complete. Schedule no new tasks while waiting. Remove nodes when all tasks have completed.
    retained_data = "RetainedData"  #: Allow currently running tasks to complete, then wait for all task data retention periods to expire. Schedule no new tasks while waiting. Remove nodes when all task retention periods have expired.


class InterNodeCommunicationState(str, Enum):

    enabled = "Enabled"  #: Enable network communication between virtual machines.
    disabled = "Disabled"  #: Disable network communication between virtual machines.


class InboundEndpointProtocol(str, Enum):

    tcp = "TCP"  #: Use TCP for the endpoint.
    udp = "UDP"  #: Use UDP for the endpoint.


class NetworkSecurityGroupRuleAccess(str, Enum):

    allow = "Allow"  #: Allow access.
    deny = "Deny"  #: Deny access.


class IPAddressProvisioningType(str, Enum):

    batch_managed = "BatchManaged"  #: A public IP will be created and managed by Batch. There may be multiple public IPs depending on the size of the Pool.
    user_managed = "UserManaged"  #: Public IPs are provided by the user and will be used to provision the Compute Nodes.
    no_public_ip_addresses = "NoPublicIPAddresses"  #: No public IP Address will be created for the Compute Nodes in the Pool.


class ComputeNodeFillType(str, Enum):

    spread = "Spread"  #: Tasks should be assigned evenly across all nodes in the pool.
    pack = "Pack"  #: As many tasks as possible (maxTasksPerNode) should be assigned to each node in the pool before any tasks are assigned to the next node in the pool.


class ElevationLevel(str, Enum):

    non_admin = "NonAdmin"  #: The user is a standard user without elevated access.
    admin = "Admin"  #: The user is a user with elevated access and operates with full Administrator permissions.


class LoginMode(str, Enum):

    batch = "Batch"  #: The LOGON32_LOGON_BATCH Win32 login mode. The batch login mode is recommended for long running parallel processes.
    interactive = "Interactive"  #: The LOGON32_LOGON_INTERACTIVE Win32 login mode. Some applications require having permissions associated with the interactive login mode. If this is the case for an application used in your task, then this option is recommended.


class AutoUserScope(str, Enum):

    task = "Task"  #: Specifies that the service should create a new user for the task.
    pool = "Pool"  #: Specifies that the task runs as the common auto user account which is created on every node in a pool.


class ContainerWorkingDirectory(str, Enum):

    task_working_directory = "TaskWorkingDirectory"  #: Use the standard Batch service task working directory, which will contain the Task resource files populated by Batch.
    container_image_default = "ContainerImageDefault"  #: Using container image defined working directory. Beware that this directory will not contain the resource files downloaded by Batch.


class CertificateStoreLocation(str, Enum):

    current_user = "CurrentUser"  #: Certificates should be installed to the CurrentUser certificate store.
    local_machine = "LocalMachine"  #: Certificates should be installed to the LocalMachine certificate store.


class CertificateVisibility(str, Enum):

    start_task = "StartTask"  #: The certificate should be visible to the user account under which the start task is run. Note that if AutoUser Scope is Pool for both the StartTask and a Task, this certificate will be visible to the Task as well.
    task = "Task"  #: The certificate should be visible to the user accounts under which job tasks are run.
    remote_user = "RemoteUser"  #: The certificate should be visible to the user accounts under which users remotely access the node.


class ContainerType(str, Enum):

    docker_compatible = "DockerCompatible"  #: A Docker compatible container technology will be used to launch the containers.


class ResourceType(str, Enum):

    batch_accounts = "Microsoft.Batch/batchAccounts"  #: The Batch account resource type.


class NameAvailabilityReason(str, Enum):

    invalid = "Invalid"  #: The requested name is invalid.
    already_exists = "AlreadyExists"  #: The requested name is already in use.
