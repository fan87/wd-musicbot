import inspect
from typing import OrderedDict

def test(a, b = None,*,c):
    pass

test("a", "b", c="c")
d: OrderedDict[str, inspect.Parameter] = inspect.signature(test).parameters
for dd in d.items():
    param: inspect.Parameter = dd[1]
    print(param.kind)