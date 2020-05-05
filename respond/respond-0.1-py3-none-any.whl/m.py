import httpz
from httpz import HTTPStatusCodeEnum as HTTPStatusCode

from string import Template

t = '''
@classmethod
def {}(
    cls, 
    data: Optional[Union[str, int, float, bool, list, dict, None]] = "", 
    headers: Optional[dict] = None) -> Response:
    """ HTTP {} {} """
    return cls._send_response(HTTPStatusCode.{}.value, data, headers)
'''

t2 = '''
@classmethod
def $meth(
    cls, 
    data: Optional[Union[str, int, float, bool, list, dict, None]] = "", 
    headers: Optional[dict] = None) -> Response:
    """ HTTP $status_code $status_message
    
    $status_description
    """
    return cls._send_response(
        HTTPStatusCode.$enum.value, 
        data, 
        headers)
'''

template = Template(t2)

s = httpz.HTTPStatusCodes()

for code in HTTPStatusCode:
    # print(code.name)
    sc = s.get(code.value)
    print(template.substitute(meth=code.name.lower(),
                              status_code=sc.code,
                              status_message=sc.message,
                              status_description=sc.description,
                              enum=code.name),
          end="")

# for code in HTTPStatusCode:
#     # print(code.name)
#     sc = s.get(code.value)
#     print(t.format(code.name.lower(), sc.code, sc.message, code.name), end="")

# for code in HTTPStatusCode:
#     # print(code.name)
#     sc = s.get(code.value)
#     print(f"| `{code.name.lower()}` | `{sc.code} `|")
