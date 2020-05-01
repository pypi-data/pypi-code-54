import os
from magma.bit import Bit
from magma.bits import Bits
from magma.array import Array
from magma.config import get_compile_dir, set_compile_dir
from magma.digital import Digital
from magma.passes.passes import CircuitPass
from magma.tuple import Tuple
from magma.verilog_utils import value_to_verilog_name
from magma.t import Direction
from magma.conversions import from_bits, as_bits
from magma.t import Direction


def _gen_bind_port(cls, mon_arg, bind_arg, insert_temporary=False):
    if isinstance(mon_arg, Tuple) or isinstance(mon_arg, Array) and \
            not issubclass(mon_arg.T, Digital):
        result = []
        for child1, child2 in zip(mon_arg, bind_arg):
            result += _gen_bind_port(cls, child1, child2)
        return result
    port = value_to_verilog_name(mon_arg)
    if insert_temporary:
        with cls.open():
            name = f"_magma_bind_wire_{cls.num_bind_wires}"
            cls.num_bind_wires += 1
            temp = type(bind_arg).qualify(Direction.Undirected)(name=name)
            if bind_arg.is_input():
                bind_arg = bind_arg.value()
                if bind_arg is None:
                    raise ValueError("Cannot bind undriven input")
            temp @= bind_arg
            temp.unused()
            arg = name
    else:
        arg = value_to_verilog_name(bind_arg)
    return [(f".{port}({arg})")]


def _bind(cls, monitor, compile_fn, *args):
    cls.num_bind_wires = 0
    bind_str = monitor.verilogFile
    ports = []
    for mon_arg, cls_arg in zip(monitor.interface.ports.values(),
                                cls.interface.ports.values()):
        if str(mon_arg.name) != str(cls_arg.name):
            error_str = f"""
Bind monitor interface does not match circuit interface
    Monitor Ports: {list(monitor.interface.ports)}
    Circuit Ports: {list(cls.interface.ports)}
"""
            raise TypeError(error_str)
        ports += _gen_bind_port(cls, mon_arg, cls_arg)
    extra_mon_args = list(
        monitor.interface.ports.values()
    )[len(cls.interface):]
    with cls.open():
        for mon_arg, bind_arg in zip(extra_mon_args, args):
            ports += _gen_bind_port(cls, mon_arg, bind_arg,
                                    insert_temporary=True)
    ports_str = ",\n    ".join(ports)
    bind_str = f"bind {cls.name} {monitor.name} {monitor.name}_inst (\n    {ports_str}\n);"  # noqa
    if not os.path.isdir(".magma"):
        os.mkdir(".magma")
    curr_compile_dir = get_compile_dir()
    set_compile_dir("normal")
    # Circular dependency, need coreir backend to compile, backend imports
    # circuit (for wrap casts logic, we might be able to factor that out).
    compile_fn(f".magma/{monitor.name}", monitor, inline=True)
    set_compile_dir(curr_compile_dir)
    with open(f".magma/{monitor.name}.v", "r") as f:
        content = "\n".join((f.read(), bind_str))
    cls.bind_modules[monitor.name] = content


class BindPass(CircuitPass):
    def __init__(self, main, compile_fn):
        super().__init__(main)
        self._compile_fn = compile_fn

    def __call__(self, cls):
        if cls.bind_modules_bound:
            return
        bind_modules = cls.bind_modules.copy()
        cls.bind_modules = {}
        for monitor, args in bind_modules.items():
            _bind(cls, monitor, self._compile_fn, *args)
        cls.bind_modules_bound = True
