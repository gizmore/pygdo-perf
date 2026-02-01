import threading

import psutil

from gdo.base.IPC import IPC
from gdo.base.ACache import ACache
from gdo.base.Application import Application
from gdo.base.Cache import Cache
from gdo.base.GDO import GDO
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.base.Logger import Logger
from gdo.base.ModuleLoader import ModuleLoader
from gdo.base.Render import Mode
from gdo.base.Util import Files
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Container import GDT_Container
from gdo.core.GDT_String import GDT_String
from gdo.date.GDT_Duration import GDT_Duration
from gdo.ui.GDT_Divider import GDT_Divider
from gdo.ui.GDT_Link import GDT_Link
from gdo.ui.GDT_Panel import GDT_Panel


class GDT_Perf(GDT_Panel):

    _perf_mode: str

    def __init__(self):
        super().__init__()
        self._perf_mode = 'full'

    def mode(self, mode: str):
        self._perf_mode = mode
        return self

    def get_perf(self):
        return self.get_perf_method()()

    def get_perf_method(self):
        return getattr(self, f'get_perf_{self._perf_mode}')

    def get_perf_min(self):
        cont = GDT_Container().add_field(
            GDT_Duration('time').units(2, True).initial_value(Application.request_time()),
        )
        if Application.config('core.profile') == '1':
            cont.add_fields(
                GDT_Divider(),
                GDT_Link().href(Application.get_page()._method.href('&__yappi=1')).text('perf_yappi',('1',)),
            )
        return cont

    def get_perf_full(self):
        user = GDO_User.current()
        mem = psutil.Process().memory_info()
        app = Application
        loader = ModuleLoader.instance()
        me = len(loader._enabled)
        ml = len(loader._cache)
        c = Cache
        return GDT_Container().add_fields(
            GDT_String('version').text('perf_version', (GDO_Module.CORE_REV,)),
            GDT_Divider(),
            GDT_String('user').text('perf_user', (user.render_name(), user.get_id())),
            GDT_Divider(),
            GDT_String('mem').text('perf_mem', (Files.human_file_size(mem.rss),)),
            GDT_Duration('time').units(2, True).initial_value(app.request_time()),
            GDT_Divider(),
            GDT_Link().href(Application.get_page()._method.href('&__yappi=1')).text('perf_yappi', (Application.config('core.profile', '0'),))
        )

    def render(self, mode: Mode = Mode.render_html):
        self.text_raw(self.get_perf().render(mode), False)
        return super().render(mode)
