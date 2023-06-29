from typing import Optional, TYPE_CHECKING, Dict, List,Tuple, Union
from pathlib import Path
from types import ModuleType
import inspect

from src.tnxts.plugin.plugin import (
    Plugin,
    _plugins
)

if TYPE_CHECKING:
    from src.tnxts.plugin.manager import (
        PluginManager,
        _managers
    )

def _module_name_to_plugin_name(parent: Optional[Plugin], module: str):
    if parent:
        if parent_name := parent.name:
            return parent_name + "." + module.rsplit(".",1)[-1]
    else:
        return module.rsplit(".",1)[-1]
    return module

def _path_to_module_name(path: Union[str,Path]) -> str:
    # todo: Path解析
    if isinstance(path, Path):
        module_name = path.resolve().name.rsplit(".",1)[0]
    else:
        module_name = path.rsplit(".",1)[0]
    return module_name

def _new_plugin(parent: "Plugin", module_name: str, manager: "PluginManager", module: Optional[ModuleType] = None, ) -> Plugin:
    plugin_name = _module_name_to_plugin_name(parent, module_name)
    if plugin_name in _plugins:
        raise  RuntimeError("插件已存在！请检查你的插件名")
    plugin = Plugin(name=plugin_name,
                    module= module if module is not None else module_name,
                    manager=manager,
                    parent_plugin=parent,
                    metadata=module._metadata if module else None
                    )

    _plugins[plugin_name] = plugin
    if parent:
        parent.sub_plugins.add(plugin)
    return plugin

def _parent_plugin() -> Optional[Plugin]:
    """获取父插件"""

    parent_module : Optional[ModuleType] = inspect.getmodule(inspect.currentframe().f_back.f_back)
    parent_plugin : Optional[Plugin] = None
    plugin_name: str

    try:
        for plugin in _plugins.values():
            if plugin.module == parent_module.__name__:
                parent_plugin = plugin
                break
    except:
        pass
    finally:
        return parent_plugin

def _plugin_manager(plugin: Plugin) -> Optional["PluginManager"]:
    """返回当前插件所在的插件管理器"""

    for manager in reversed(_managers):
        if plugin.name in manager.available_plugins:
            return manager

    return None

def _module_name_to_plugin(module_name: str) -> Optional[Plugin]:
    for plugin in _plugins.values():
        if module_name == plugin.module.__name__:
            return plugin

    return  None


# def _module_name_to_plugin(module_name: str):
