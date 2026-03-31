from dataclasses import dataclass
from typing import List

from ut_frontend.ftq.ftq_top.env.ftq_bundle import LastStageFtbEntryBundle

# 配置
PredictWidth = 16
numBrSlot = 1

# @dataclass
# class FtbSlot:
#     offset: int    # UInt(log2Ceil(PredictWidth)) → 0~15
#     sharing: bool  # tailSlot 是否共享给分支
#     valid: bool    # 槽是否有效

@dataclass
class FTBEntry:
    isCall : int = 0
    isRet : int = 0
    isJalr : int = 0
    valid : int = 0
    brSlots_0_offset : int = 0
    brSlots_0_sharing : int = 0
    brSlots_0_valid : int = 0
    tailSlot_offset : int = 0
    tailSlot_sharing : int = 0
    tailSlot_valid : int = 0

    @classmethod
    def from_last_stage_ftb_entry(cls, ftb: 'LastStageFtbEntryBundle'):
        """从 LastStageFtbEntryBundle 构造 FTBEntry"""
        return cls(
            isCall = ftb.isCall.value,
            isRet = ftb.isRet.value,
            isJalr = ftb.isJalr.value,
            valid = ftb.valid.value,
            brSlots_0_offset = ftb.brSlots_0_offset.value,
            brSlots_0_sharing = ftb.brSlots_0_sharing.value,
            brSlots_0_valid = ftb.brSlots_0_valid.value,
            tailSlot_offset = ftb.tailSlot_offset.value,
            tailSlot_sharing = ftb.tailSlot_sharing.value,
            tailSlot_valid = ftb.tailSlot_valid.value,
        )

class FTBEntryMem:
    def __init__(self, size: int = 64):
        self.size = size
        self.mem = [FTBEntry() for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: FTBEntry):
        """写入：wen 有效且地址合法时写入"""
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, raddr: int) -> FTBEntry:
        """读取：直接返回地址对应 entry"""
        if 0 <= raddr < self.size:
            return self.mem[raddr]
        else:
            raise IndexError("FTBEntryMem read address out of range")
