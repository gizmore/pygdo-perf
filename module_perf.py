from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Enum import GDT_Enum
from gdo.ui.GDT_Page import GDT_Page


class module_perf(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 205

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Enum('show_perf').not_null().choices({"never": "Never", "always": "Always", "staff": "Staff"}).initial('always'),
        ]

    def cfg_show_perf(self) -> str:
        return self.get_config_val('show_perf')

    def should_show_perf(self) -> bool:
        perf = self.cfg_show_perf()
        if perf == 'always':
            return True
        elif perf == 'never':
            return False
        else:
            return GDO_User.current().is_staff()

    def gdo_init_sidebar(self, page: 'GDT_Page'):
        if self.should_show_perf():
            from gdo.perf.GDT_Perf import GDT_Perf
            page._bottom_bar.add_field(GDT_Perf())
