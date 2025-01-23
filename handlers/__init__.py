from .inline import routers as inline_routers
from .message import routers as message_routers

ROUTERS = message_routers + inline_routers
