from dataclasses import dataclass
from typing import List

# 配置
PredictWidth = 16
numBrSlot = 1

@dataclass
class FtbSlot:
    offset: int    # UInt(log2Ceil(PredictWidth)) → 0~15
    sharing: bool  # tailSlot 是否共享给分支
    valid: bool    # 槽是否有效

@dataclass
class FTBEntry:
    brSlots: List[FtbSlot]  # Vec(numBrSlot, ...)
    tailSlot: FtbSlot
    isCall: bool
    isRet: bool
    isJalr: bool

    @classmethod
    def default(cls):
        """返回默认无效 entry"""
        slots = [FtbSlot(0, False, False) for _ in range(numBrSlot)]
        tail = FtbSlot(0, False, False)
        return cls(slots, tail, False, False, False)

class FTBEntryMem:
    def __init__(self, size: int = 64):
        self.size = size
        self.mem = [FTBEntry.default() for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: FTBEntry):
        """写入：wen 有效且地址合法时写入"""
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, raddr: int) -> FTBEntry:
        """读取：直接返回地址对应 entry"""
        if 0 <= raddr < self.size:
            return self.mem[raddr]
        else:
            return FTBEntry.default()
