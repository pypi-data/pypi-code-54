from enum import IntEnum
from typing import AnyStr, Optional, Any, List

String = AnyStr
# Aliases
Text = OID = ID = Name = Description = IconColor = Image = Email = Website = NameText = String
NameHtml = DescriptionHtml = DescriptionText = Url = Color = OwnerType = Cover = Date = String

OidList = List[OID]
# Aliases
Followers = Assignors = Favorites = OidList

StringList = List[AnyStr]
# Aliases
Assignees = StringList

Integer = int
# Aliases
StatusCode = ActiveCount = TaskCount = RootCount = Value = Length = Type = Integer
RemoveColumn = Status = Priority = Rate = Data = Order = ChildCount = Integer
TaskId = Before = Target = Integer

Boolean = bool
# Aliases
AsUser = Pinned = Peekaboo = Global = Archived = Boolean

QUIRE_API_URL = "https://quire.io/api"


class StatusCodes(IntEnum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

    @property
    def desc(self):
        return self.get_desc(self.value)

    @staticmethod
    def get_desc(status: StatusCode, default: Optional[Any] = None) -> AnyStr:
        __DESCRIPTION = {
            StatusCodes.SUCCESS: "Request successful",
            StatusCodes.BAD_REQUEST: "You're using a wrong parameter, or passing incorrect data.",
            StatusCodes.UNAUTHORIZED: "Invalid or expired token.",
            StatusCodes.FORBIDDEN: "Not authorized to access the resources.",
            StatusCodes.NOT_FOUND: "The specified resources could not be found.",
            StatusCodes.METHOD_NOT_ALLOWED: "Method not allowed or supported.",
            StatusCodes.CONFLICT: "There is already a resources with the same criteria.",
            StatusCodes.TOO_MANY_REQUESTS: "Exceeded the rate limit for API calls",
            StatusCodes.INTERNAL_SERVER_ERROR: "There is an unexpected error.",
            StatusCodes.SERVICE_UNAVAILABLE: "Server is down for maintenance."
        }

        return __DESCRIPTION.get(status, default)
