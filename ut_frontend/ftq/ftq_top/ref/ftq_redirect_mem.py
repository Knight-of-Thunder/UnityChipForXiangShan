from dataclasses import dataclass

from ut_frontend.ftq.ftq_top.env.ftq_bundle import LastStageSpecInfoBundle
FTQSIZE = 64
from typing import List, Optional

@dataclass
class Ftq_Redirect_SRAMEntry:
    # # RAS 相关状态（用于重定向时恢复 RAS 栈）
    # ssp: int          # UInt(log2Up(RasSize)) → [0, RasSize)
    # sctr: int         # RasCtrSize.W → 0 ~ (2^RasCtrSize - 1)
    # TOSW: RASPtr      # RAS 写指针
    # TOSR: RASPtr      # RAS 读指针
    # NOS: RASPtr       # Next of Stack (RAS)
    # topAddr: int      # RAS 栈顶返回地址 (VAddrBits)

    # # 全局分支历史指针
    # histPtr: CGHPtr

    # # SC 预测器不同意信号（Option 类型）
    # # - 在 FPGA 平台：为 None
    # # - 在 ASIC/仿真平台：为 List[bool]（长度 = numBr）
    # sc_disagree: Optional[List[bool]] = None
    histPtr_flag: int
    histPtr_value: int
    ssp: int
    sctr: int
    TOSW_flag: int
    TOSW_value: int
    TOSR_flag: int
    TOSR_value:int
    NOS_flag: int
    NOS_value:int
    topAddr: int
    sc_disagree_0: int
    sc_disagree_1: int

    @classmethod
    def from_spec_info(cls, spec: LastStageSpecInfoBundle):
        """
        从 spec_info 构造 Ftq_Redirect_SRAMEntry
        注意：实际字段需从 spec 的 s3 阶段结果中提取（香山中 s3 才有完整 speculative info）
        """
        return cls(
            histPtr_flag = spec.histPtr_flag.value,
            histPtr_value = spec.histPtr_value.value,
            ssp = spec.ssp.value,
            sctr = spec.sctr.value,
            TOSW_flag = spec.TOSW_flag.value,
            TOSW_value = spec.TOSW_value.value,
            TOSR_flag = spec.TOSR_flag.value,
            TOSR_value = spec.TOSR_value.value,
            NOS_flag = spec.NOS_flag.value,
            NOS_value = spec.NOS_value.value,
            topAddr = spec.topAddr.value,
            sc_disagree_0 = spec.sc_disagree_0.value,
            sc_disagree_1 = spec.sc_disagree_1.value
        )

class FTQRedirectMem:
    def __init__(self, size: int = FTQSIZE):
        self.size = size
        # 初始化默认 entry
        self.mem = [
            Ftq_Redirect_SRAMEntry(
                histPtr_flag = 0,
                histPtr_value = 0,
                ssp = 0,
                sctr = 0,
                TOSW_flag = 0,
                TOSW_value = 0,
                TOSR_flag = 0,
                TOSR_value = 0,
                NOS_flag = 0,
                NOS_value = 0,
                topAddr = 0,
                sc_disagree_0 = 0,
                sc_disagree_1 = 0
            )
            for _ in range(size)
        ]

    def write(self, wen: bool, waddr: int, wdata: Ftq_Redirect_SRAMEntry):
        """写入：只有 wen=True 且地址有效时才写"""
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, raddr: int) -> Ftq_Redirect_SRAMEntry:
        """读取：直接返回地址对应的数据（组合逻辑）"""
        if 0 <= raddr < self.size:
            return self.mem[raddr]
        else:
            raise IndexError("FTQRedirectMem read address out of range")