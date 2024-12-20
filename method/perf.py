from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.perf.GDT_Perf import GDT_Perf


class perf(Method):

    def gdo_trigger(self) -> str:
        return 'perf'

    async def gdo_execute(self) -> GDT:
        return GDT_Perf()
