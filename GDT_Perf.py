import threading

import psutil

from gdo.base.Application import Application
from gdo.base.Cache import Cache
from gdo.base.Database import Database
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
from gdo.ui.GDT_Bar import GDT_Bar
from gdo.ui.GDT_Divider import GDT_Divider
from gdo.ui.GDT_Panel import GDT_Panel


class GDT_Perf(GDT_Panel):

    def __init__(self):
        super().__init__()

    def get_perf(self):
        user = GDO_User.current()
        mem = psutil.Process().memory_info()
        app = Application
        loader = ModuleLoader.instance()
        me = sum(1 for _ in loader.enabled())
        ml = len(loader._cache)
        return GDT_Container().add_field(
            GDT_String('version').text('perf_version', (GDO_Module.CORE_REV,)),
            GDT_Divider(),
            GDT_String('user').text('perf_user', (user.render_name(), user.get_id())),
            GDT_Divider(),
            GDT_String('cpu').text('perf_cpu', (str(psutil.cpu_percent()), threading.active_count())),
            GDT_Divider(),
            GDT_String('mem').text('perf_mem', (Files.human_file_size(mem.rss),)),
            GDT_Divider(),
            GDT_String('db').text('perf_db', (str(app.DB_READS), str(app.DB_WRITES), str(app.DB_READS + app.DB_WRITES), round(app.DB_TRANSACTIONS, 2))),
            GDT_Divider(),
            GDT_String('log').text('perf_log', (str(Logger.LINES_WRITTEN),)),
            GDT_Divider(),
            GDT_String('events').text('perf_events', (str(app.EVENT_COUNT),)),
            GDT_Divider(),
            GDT_String('code').text('perf_code', (GDT.GDT_COUNT, GDT.GDT_MAX, GDO.GDO_COUNT, GDO.GDO_MAX, me, ml)),
            GDT_Divider(),
            GDT_String('cache').text('perf_cache', (Cache.HITS, Cache.MISS, Cache.UPDATES, Cache.REMOVES)),
            GDT_Divider(),
            GDT_Duration('time').initial_value(Application.request_time()),
        )

    def render(self, mode: Mode = Mode.HTML):
        self.text_raw(self.get_perf().render(mode), False)
        return super().render(mode)
