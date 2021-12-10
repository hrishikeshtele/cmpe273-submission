import collections
import hashlib

from abc import ABCMeta
from abc import abstractmethod
from bisect import bisect, bisect_right

Node = collections.namedtuple('Node', [
    'name', 'host', 'port', 'hrw_weight', 'keys'
])


class HashingInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(self, subclass: type) -> bool:
        return (
                hasattr(subclass, 'hash_key') and callable(subclass.hash_key) and
                hasattr(subclass, 'get_node') and callable(subclass.get)
                or NotImplemented
        )

    @abstractmethod
    def hash_key(self, key: str) -> int:
        """generates an integer index value for the given key"""
        raise NotImplementedError

    @abstractmethod
    def get_node(self, key: str) -> Node:
        """lookup a node for the given key"""
        raise NotImplementedError


class DefaultHash(HashingInterface):
    def __init__(self, nodes) -> None:
        super().__init__()
        self.nodes = nodes
        self.num_buckets = len(self.nodes)

    def hash_key(self, key: str) -> int:
        byte_sum = 0
        for b in bytearray(key.encode()):
            byte_sum += b
        return byte_sum % self.num_buckets

    def get_node(self, key: str) -> Node:
        index = self.hash_key(key)
        return self.nodes[index]


class HRWHash(HashingInterface):
    def __init__(self, nodes) -> None:
        super().__init__()
        self.nodes = nodes
        self.num_buckets = len(self.nodes)

    def compute_weighted_score(self, key, seed, weight):
        encoded_string = (key + seed).encode()
        sha256 = hashlib.sha256(encoded_string)
        return int(sha256.hexdigest(), 16) * weight

    def hash_key(self, key: str) -> Node:
        max_weight = 0
        max_node = None
        for i in range(len(self.nodes)):
            temp_weight = self.compute_weighted_score(key, self.nodes[i].host, self.nodes[i].hrw_weight)
            if temp_weight > max_weight:
                max_weight = temp_weight
                max_node = self.nodes[i]
        return max_node

    def get_node(self, key: str) -> Node:
        heighest_weight_node = self.hash_key(key)
        return heighest_weight_node


class ConsistentHash(HashingInterface):
    def __init__(self, nodes) -> None:
        super().__init__()
        self.num_buckets = pow(2, 256)
        self.keys = []
        self.nodes = []
        for n in nodes:
            key = self.hash_key(n.host)
            node_index = bisect(self.keys, key)
            self.nodes.insert(node_index, n)
            self.keys.insert(node_index, key)

    def hash_key(self, key: str) -> int:
        sha256 = hashlib.sha256(key.encode())
        return int(sha256.hexdigest(), 16) % self.num_buckets

    def get_node(self, key: str) -> Node:
        bucket_index = self.hash_key(key)
        node_index = bisect_right(self.keys, bucket_index) % len(self.keys)
        return self.nodes[node_index]
