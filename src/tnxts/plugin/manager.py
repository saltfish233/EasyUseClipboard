"""本模块实现插件加载历程"""
import importlib
import pkgutil
import sys
from typing import Optional, Set, Iterable, Dict, List, Sequence, Union
from pathlib import Path
from itertools import chain
from importlib.abc import MetaPathFinder
from importlib.machinery import PathFinder, SourceFileLoader, ModuleSpec
from types import ModuleType
from src.tnxts.util import log
from src.tnxts.plugin import Plugin
from src.tnxts.plugin.plugin import _plugins
from src.tnxts.plugin.utils import (
    _new_plugin,
    _path_to_module_name, _module_name_to_plugin_name
)
from src.tnxts.util.log import _general_logger

_managers: List["PluginManager"] = []


class PluginManager:
    """
    插件管理器

    参数:
        plugins: 插件模块名集合
        search_path: 插件搜索路径
    """

    @_general_logger.logger.catch()
    def __init__(self,
                 plugins: Optional[Iterable[str]] = None,
                 search_path: Optional[str] = None,
                 parent: Optional[Plugin] = None,
                 ):
        # 直接插件
        self.plugins: Set[str] = set(plugins or [])
        self.search_path: str = search_path or ""

        self._parent: Optional[Plugin] = parent

        # 缓存插件
        # str 插件名 str 模块名
        self._third_party_plugins: Dict[str, str] = {}
        # str 已搜索到的插件名 str 模块绝对路径
        # self._searched_plugins: Dict[str, Path] = {}
        self._searched_plugins: Dict[str, str] = {}

        self.prepared_plugins()

    @_general_logger.logger.catch()
    def prepared_plugins(self) -> Set[str]:
        previous_plugins = self._previous_plugins()
        third_party_plugins: Dict[str, str] = {}
        # searched_plugins: Dict[str, Path] = {}
        searched_plugins: Dict[str, str] = {}

        # 检查独立插件
        for plugin in self.plugins:
            name = _module_name_to_plugin_name(parent=self._parent, module= plugin)
            if name in third_party_plugins or name in previous_plugins:
                raise RuntimeError(
                    f"插件{name}已存在，请不要重复引入。如果确定是新插件，请确定您的插件名正确或修改插件名。"
                )
            third_party_plugins[name] = plugin

        self._third_party_plugins = third_party_plugins


        # todo: name待处理
        # 检查搜索路径内的插件
        if self.search_path:
            search_pack = importlib.import_module(self.search_path)
            for module_info in pkgutil.iter_modules(search_pack.__path__,):
                # print(module_info.module_finder.find_spec(module_info.name))
                name = _module_name_to_plugin_name(parent=self._parent, module=module_info.name)
                if name.startswith("_"):
                    continue
                if module_info.ispkg:
                    continue
                if (name in third_party_plugins
                        or name in searched_plugins
                        or name in previous_plugins
                ):
                    raise RuntimeError(
                        f"插件{name}已存在，请不要重复引入。如果确定是新插件，请确定您的插件名正确或修改插件名。"
                    )

                if not (module_spec := module_info.module_finder.find_spec(
                        module_info.name
                )):
                    continue
                if not (module_path := module_spec.origin):
                    continue

                _general_logger.logger.info(f"{name}载入")

                # searched_plugins[name] = Path(module_path).resolve()
                searched_plugins[name] = self.search_path + '.' + module_info.name
                self._searched_plugins = searched_plugins
                self.load_plugin(self.search_path + '.' + module_info.name)

        return self.available_plugins

    @property
    @_general_logger.logger.catch()
    def third_party_plugins(self) -> Set:
        """返回所有独立插件的名称"""
        return set(self._third_party_plugins.keys())

    @property
    @_general_logger.logger.catch()
    def searched_plugins(self) -> Set:
        """返回所有已搜索到的插件名称"""
        return set(self._searched_plugins.keys())

    @property
    @_general_logger.logger.catch()
    def available_plugins(self) -> Set:
        """返回当前插件管理器中所有可用的插件名称"""
        return self.third_party_plugins | self.searched_plugins

    @property
    @_general_logger.logger.catch()
    def main_plugins(self) -> Optional[List]:
        """返回所有的主要插件"""
        main_plugin_list : List = []
        for plugin in _plugins.values():
            if plugin.parent_plugin is None:
                main_plugin_list.append(plugin)

        return main_plugin_list

    @_general_logger.logger.catch()
    def _previous_plugins(self) -> Set:
        """返回当前插件管理器及之前的所有插件管理器中所有可用插件的名称"""
        _pre_managers: List[PluginManager]

        if self in _managers:
            _pre_managers = _managers[:_managers.index(self)]
        else:
            _pre_managers = _managers[:]

        return set(
            chain.from_iterable(manager.available_plugins for manager in _pre_managers)
        )

    @_general_logger.logger.catch()
    def load_plugin(self, module_name: str) -> Plugin:

        try:
            # 模块导入之前先创建plugin
            plugin = _new_plugin(self._parent, module_name=module_name, manager=self)
            plugin_name = _module_name_to_plugin_name(self._parent,module_name)
            if plugin_name in self.plugins:
                module = importlib.import_module(module_name)
            elif plugin_name in self._third_party_plugins:
                module = importlib.import_module(self._third_party_plugins[plugin_name])
            elif plugin_name in self._searched_plugins:
                module = importlib.import_module(
                  self._searched_plugins[plugin_name]
                )
            else:
                raise RuntimeError(f"没有找到插件: {plugin_name}, 请检查你的插件名!")

            # 如果模块没有导入就导入模块
            if plugin.module:
                plugin.set_plugin_module(module)
                if module._metadata:
                    plugin.metadata = module._metadata

            setattr(module,"__plugin__",plugin)

            if (plugin := getattr(module, "__plugin__", None)) is None:
                raise RuntimeError(
                    f"模块{module.__name__} 无法被加载为插件!"
                     "请不要在load之前import插件"
                )
            _general_logger.logger.success(f"插件{plugin_name}加载成功")
            return plugin
        except Exception as ex:
            
            _general_logger.logger.error(f"载入插件{plugin_name}失败 " + str(ex))


# class PluginFinder(MetaPathFinder):
#     def find_spec(
#             self,
#             fullname: str,
#             path: Optional[Sequence[Path]],
#             target: Optional[ModuleType] = None
#     ) -> Optional[ModuleSpec]:
#         if _managers:
#             module_spec = PathFinder.find_spec(fullname, path, target)
#             if not module_spec:
#                 return
#             module_origin = module_spec.origin
#             if not module_origin:
#                 return
#             module_path = Path(module_origin).resolve()
#
#             for manager in _managers:
#                 if (fullname in manager._third_party_plugins.values()
#                         or module_path in manager._searched_plugins.values()
#                 ):
#                     pass
#         module_spec = PathFinder.find_spec(fullname, path, target)
#         print("Importing", fullname, path, target)
#         return None
#
#
# class PluginLoader(SourceFileLoader):
#     def __init__(self, manager: PluginManager, fullname: str, path: Union[str, bytes]) -> None:
#         self.manager = manager
#         self.loaded = False
#         super().__init__(fullname, path)
#
#     def create_module(self, spec: ModuleSpec) -> Optional[ModuleType]:
#         if self.name in sys.modules:
#             self.loaded = True
#             return sys.modules[self.name]
#
#         return super().create_module(spec)
#
#     def exec_module(self, module: ModuleType) -> None:
#         if self.loaded:
#             return
#
#         # 找到当前插件的父插件
#         pre_plugins = _current_plugin_chain.get()
#         for pre_plugin in reversed(pre_plugins):
#             if _managers.index(pre_plugin.manager) < _managers.index(self.manager):
#                 pass
#                 # plugin.parent_plugin =
#
#
#         # 在执行之前创建插件
#         plugin = _new_plugin(self.name, module, self.manager)
#         setattr(module, "__plugin__", plugin)
#
#
# sys.meta_path.insert(0, PluginFinder())
