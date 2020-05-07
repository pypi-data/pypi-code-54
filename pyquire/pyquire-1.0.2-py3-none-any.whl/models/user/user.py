from typing import List

from attr import attrs

from pyquire.models.identity_x import IdentityX

__all__ = ["User", "Users"]


@attrs
class User(IdentityX):
    # for privacy, we don't output fdCreatedAt and fdCreatedBy
    pass


Users = List[User]
