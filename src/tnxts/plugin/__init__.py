from typing import Tuple
from .plugin import Plugin
from .manager import PluginManager
from contextvars import ContextVar

from src.tnxts.plugin.plugin import _plugins,PluginMetadata
from src.tnxts.plugin.manager import _managers
from src.tnxts.plugin.utils import _module_name_to_plugin


_current_plugin_chain: ContextVar[Tuple["Plugin",...]] = ContextVar(
    "_current_plugin_chain", default=tuple()
)











