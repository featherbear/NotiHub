DEBUG = False
import builtins
builtins.dprint = lambda *args: print(*args) if DEBUG else None
import NotiHub.services
import NotiHub.web