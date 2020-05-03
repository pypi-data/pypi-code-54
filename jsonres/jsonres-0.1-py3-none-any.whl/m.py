import httpz
from httpz import HTTPStatusCodeEnum as HTTPStatusCode

template = '''
@classmethod
def {}(
    cls, 
    data: Optional[Union[str, int, float, bool, list, dict, None]] = "", 
    headers: Optional[dict] = None) -> Response:
    """ HTTP {} {} """
    return cls._send_response(HTTPStatusCode.{}.value, data, headers)
'''


s = httpz.HTTPStatusCodes()


# for code in HTTPStatusCode:
#     # print(code.name)
#     sc = s.get(code.value)
#     print(template.format(code.name.lower(), sc.code, sc.message, code.name), end="")

for code in HTTPStatusCode:
    # print(code.name)
    sc = s.get(code.value)
    print(f"| `{code.name.lower()}` | `{sc.code} `|")