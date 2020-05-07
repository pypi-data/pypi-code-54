from tldextract import extract
from tldextract.tldextract import ExtractResult
from typing import Union


def is_toplevel_domain(args: Union[str, ExtractResult]) -> bool:
    # If the user provided a FQDN then we first need to break it into its parts
    if isinstance(args, str):
        args = extract(args)
    
    if not args.subdomain and args.domain and args.suffix:
        return True

    return False
