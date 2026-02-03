from dataclasses import dataclass

from ut_frontend.ftq.ftq_top.ref.ftb_entry_mem import FTBEntry, FTBEntryMem

@dataclass
class Ftq_1R_SRAMEntry:
    meta: int                 # UInt(MaxMetaLength.W) → 用 int 表示
    ftb_entry: FTBEntry  # 复用之前定义的 FTBEntry

    @classmethod
    def default(cls):
        return cls(meta=0, ftb_entry=FTBEntry.default())

class FTQMeta1RSram:
    def __init__(self, size: int = 64):
        self.size = size
        self.mem = [Ftq_1R_SRAMEntry.default() for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: Ftq_1R_SRAMEntry):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, raddr: int) -> Ftq_1R_SRAMEntry:
        if 0 <= raddr < self.size:
            return self.mem[raddr]
        else:
            return Ftq_1R_SRAMEntry.default()