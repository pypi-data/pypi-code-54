from canoser import Struct, Uint64
from libra.hasher import gen_hasher, HashValue


class TransactionInfo(Struct):
    """`TransactionInfo` is the object we store in the transaction accumulator.
    It consists of the transaction as well as the execution result of this transaction.
    """
    _fields = [
        ('transaction_hash', HashValue),
        ('state_root_hash', HashValue),
        ('event_root_hash', HashValue),
        ('gas_used', Uint64),
        ('major_status', Uint64)
    ]

    def hash(self):
        shazer = gen_hasher(b"TransactionInfo::libra_types::transaction")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.transaction_hash = proto.transaction_hash
        ret.state_root_hash = proto.state_root_hash
        ret.event_root_hash = proto.event_root_hash
        ret.gas_used = proto.gas_used
        ret.major_status = proto.major_status
        # TODO: StatusCode::try_from(proto_txn_info.major_status).unwrap_or(StatusCode::UNKNOWN_STATUS)
        return ret
