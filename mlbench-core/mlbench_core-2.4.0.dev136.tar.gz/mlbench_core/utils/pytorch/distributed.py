import torch
import torch.distributed as dist

# TODO: those 3 funtions are never used, maybe delete them ?


def broadcast(tensor, src):
    return dist.broadcast(tensor, src=src)


def elementwise_min(tensor):
    dist.all_reduce(tensor, op=dist.ReduceOp.MIN)
    return tensor


def aggregate_gradients(model, world_size, average_models=False):
    """Average gradients of models across all processes."""
    # all_reduce the gradients.
    for ind, param in enumerate(model.parameters()):
        # all reduce.
        dist.all_reduce(param.grad.data, op=dist.ReduceOp.SUM)

        if average_models:
            param.grad.data /= world_size


def global_average(sum, count):
    def helper(array):
        array = get_backend_tensor(torch.Tensor(array))

        dist.all_reduce(array, op=dist.ReduceOp.SUM)
        return array[0] / array[1]

    avg = helper([sum, count])
    return avg


def pack_tensors(tensors, use_cuda=False):
    """
    Packs a list of tensors into one 1-dimensional tensor.

    Args:
        tensors (list[torch.Tensor]): The tensors to pack
        use_cuda (bool): Whether the resulting tensor should be on cuda

    Returns:
        (torch.Tensor, list[int], list[(int, int)]):
            The flattened tensors, the list start indices of each packed tensor,
            and the original shape of each tensor.

            Those values are used to then unpack the tensor
    """
    indices = [0]
    for tensor in tensors:
        new_end = indices[-1] + tensor.nelement()
        indices.append(new_end)

    tensor_sizes = [t.size() for t in tensors]

    vec = torch.empty(
        indices[-1],
        device=tensors[0].device if tensors[0].is_cuda and use_cuda else "cpu",
    )

    for tensor, start_idx, end_idx in zip(tensors, indices[:-1], indices[1:]):
        vec[start_idx:end_idx] = tensor.data.view(-1)

    return vec, indices, tensor_sizes


def unpack_tensors(aggregated, indices, sizes):
    """
    Unpacks a 1-dimensional tensor into a list of tensors

    Args:
        aggregated (torch.Tensor): The 1-dimensional tensor
        indices (List[Int]): The start index of each tensor
        sizes (List[(Int, Int)]): The size of each resulting tensor

    Returns:
        List[torch.Tensor]: The unpacked tensors
    """
    start_index = indices[:-1]
    end_index = indices[1:]

    tensors = []
    for i, (start, end) in enumerate(zip(start_index, end_index)):
        tensors.append(aggregated[start:end].view(sizes[i]))

    return tensors


##########################################################################################


class Aggregation(object):
    """Aggregate udpates / models from different processes."""

    def __init__(self, use_cuda=False):
        """

        Args:
            use_cuda (bool): Whether to use CUDA tensors for communication
        """
        self.use_cuda = use_cuda

    def _agg(self, data, op):
        """Aggregate data using `op` operation.

        Args:
            data (:obj:`torch.Tensor`): A Tensor to be aggragated.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.

        Returns:
            :obj:`torch.Tensor`: An aggregated tensor.
        """
        raise NotImplementedError

    def _agg_weights_by_model(self, model, op):
        """Aggregate models by model weight, all layers at once

        Args:
            model (:obj:`torch.Module`): Models to be averaged.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.
        """
        # Pack all layers
        packed, indices, sizes = pack_tensors(
            [t.data for t in model.parameters()], use_cuda=self.use_cuda
        )
        aggregated = self._agg(packed, op=op)

        tensors = unpack_tensors(aggregated, indices, sizes)
        # Unpack
        for i, param in enumerate(model.parameters()):
            param.data = tensors[i]

    def _agg_gradients_by_model(self, model, op):
        """Aggregate models gradients, all layers at once

        Args:
            model (:obj:`torch.Module`): Models to be averaged.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.
        """
        # Pack all layers

        packed, indices, sizes = pack_tensors(
            [t.grad.data for t in model.parameters()], use_cuda=self.use_cuda
        )
        aggregated = self._agg(packed, op=op)

        # Unpack
        tensors = unpack_tensors(aggregated, indices, sizes)
        for i, param in enumerate(model.parameters()):
            param.grad.data = tensors[i]

    def _agg_weights_by_layer(self, model, op):
        """Aggregate models by model weight, for each layer individually

        Args:
            model (:obj:`torch.Module`): Models to be averaged.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.
        """
        # Aggregate layer by layer
        for _, param in enumerate(model.parameters()):
            grad = self._agg(param.data, op=op)
            param.data = grad

    def _agg_gradients_by_layer(self, model, op):
        """Aggregate models gradients each layer individually

        Args:
            model (:obj:`torch.Module`): Models to be averaged.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.
        """
        # Aggregate layer by layer
        for _, param in enumerate(model.parameters()):
            grad = self._agg(param.grad.data, op=op)
            param.grad.data = grad

    def agg_model(self, by_layer=False):
        if by_layer:
            return self._agg_weights_by_layer
        else:
            return self._agg_weights_by_model

    def agg_grad(self, by_layer=False):
        if by_layer:
            return self._agg_gradients_by_layer
        else:
            return self._agg_gradients_by_model


class AllReduceAggregation(Aggregation):
    """Aggregate udpates / models from different processes."""

    def __init__(self, world_size, use_cuda=False):
        self.world_size = world_size
        super(AllReduceAggregation, self).__init__(use_cuda=use_cuda)

    def _agg(self, data, op):
        """Aggregate data using `op` operation.

        Args:
            data (:obj:`torch.Tensor`): A Tensor to be aggragated.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.

        Returns:
            :obj:`torch.Tensor`: An aggregated tensor.
        """
        if op == "avg":
            dist.all_reduce(data, op=dist.ReduceOp.SUM)
            data /= self.world_size
        else:
            raise NotImplementedError
        return data


class DecentralizedAggregation(Aggregation):
    """Aggregate updates in a decentralized manner."""

    def __init__(self, rank, neighbors, use_cuda=False):
        """
        Args:
            rank (int): Rank of the current process
            neighbors (list): A list of ranks of its neighbors.
        """
        assert rank not in neighbors
        self.rank = rank
        self.neighbors = neighbors
        super(DecentralizedAggregation, self).__init__(use_cuda=use_cuda)

    def _agg(self, data, op):
        """Aggregate data using `op` operation.

        Args:
            data (:obj:`torch.Tensor`): A Tensor to be aggragated.
            op (str): Aggregation methods like `avg`, `sum`, `min`, `max`, etc.

        Returns:
            :obj:`torch.Tensor`: An aggregated tensor.
        """
        # Create some tensors to host the values from neighborhood.
        local_data = {i: torch.zeros_like(data) for i in self.neighbors}
        local_data[self.rank] = data

        reqs = []
        for node in self.neighbors:
            reqs.append(dist.isend(tensor=local_data[self.rank], dst=node))
            reqs.append(dist.irecv(tensor=local_data[node], src=node))

        for req in reqs:
            req.wait()

        # Aggregate local_data
        if op == "avg":
            output = sum(local_data.values()) / (len(self.neighbors) + 1)
        else:
            raise NotImplementedError("op {} is not supported yet.".format(op))

        return output


class SparsifiedAggregation(Aggregation):
    """Aggregate sparsified updates."""

    def __init__(self, model, use_cuda=False):
        super(SparsifiedAggregation, self).__init__(use_cuda=use_cuda)
        pass

    def _agg(self, data, op):
        pass


def get_backend_tensor(tensor):
    if dist.is_initialized() and dist.get_backend() == dist.Backend.NCCL:
        return tensor.cuda()
    return tensor
