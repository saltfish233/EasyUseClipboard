"""本模块定义插件元信息。
"""

from dataclasses import dataclass, field
from typing import Optional, Type, TYPE_CHECKING, Set, Dict, Union
from types import ModuleType
from pydantic import BaseModel

_plugins: Dict[str, "Plugin"] = {}

if TYPE_CHECKING:
    from .manager import PluginManager

@dataclass(eq=False)
class PluginMetadata:
    """插件元信息，由插件开发者提供"""

    name: str
    """插件名称"""
    author: str
    """插件作者"""
    description: str
    """插件功能介绍"""
    usage: str
    """插件使用方法"""
    type: Optional[str] = None
    """插件类型，用于确定使用位置"""
    homepage: Optional[str] = None
    """插件主页"""
    config: Optional[Type[BaseModel]] = None

@dataclass(eq=False)
class Plugin:
    """存储插件信息"""

    name: str
    """插件索引标识，使用 文件/文件夹 名称作为标识"""
    manager: "PluginManager"
    """插件所在的插件管理器"""
    module: Union[ModuleType, str] = None
    """插件模块对象"""
    parent_plugin: Union["Plugin"] = None
    """父插件"""
    sub_plugins: Set["Plugin"] = field(default_factory=set)
    """子插件的集合"""
    metadata: Optional[PluginMetadata] = None
    """插件元信息"""
    enable: bool = False
    """插件是否启用"""

    @property
    def full_name(self):
        if parent_name := self.parent_plugin.full_name:
            return f"{parent_name}.{self.name}"
        return self.name

    def set_plugin_module(self, module: "ModuleType"):
        self.module = module

