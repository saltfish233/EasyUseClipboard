import os
import sys
import inspect
from src.tnxts.plugin import Plugin
from typing import Optional,Union, Set
from pathlib import Path
from types import ModuleType
from src.tnxts.plugin.manager import(
    PluginManager,
    _managers
)
from src.tnxts.plugin.utils import (
    _module_name_to_plugin_name,
    _path_to_module_name,
    _plugin_manager,
    _parent_plugin
)
from src.tnxts.util.log import _general_logger

@_general_logger.logger.catch()
def load_plugin(module_path: Union[str, Path]) -> Optional[Plugin]:
    """加载单个插件

        参数:
            module_path: 插件名称 `插件路径`
    """
    parent_plugin: Optional[Plugin] = _parent_plugin()
    module_name: str
    manager: PluginManager

    module_path = _path_to_module_name(module_path)
    if parent_plugin:
        # 找到兄弟插件的manager
        if sub_plugins := parent_plugin.sub_plugins:
            manager = _plugin_manager(list(sub_plugins)[0])
        else:
            manager = PluginManager([module_path],parent=parent_plugin)
            _managers.append(manager)
    else:
        manager = PluginManager([module_path])
        _managers.append(manager)

    return manager.load_plugin(module_path)

@_general_logger.logger.catch()
def load_plugins(plugin_dir : Union[str, Path]) -> Set[Plugin]:
    parent_plugin: Optional[Plugin] = _parent_plugin()
    manager: PluginManager

    if parent_plugin:
        # 找到兄弟插件的manager
        if sub_plugins := parent_plugin.sub_plugins:
            manager = _plugin_manager(list(sub_plugins)[0])
        else:
            manager = PluginManager(search_path=plugin_dir, parent=parent_plugin)
            _managers.append(manager)
    else:
        manager = PluginManager(search_path=plugin_dir)
        _managers.append(manager)
    return set()