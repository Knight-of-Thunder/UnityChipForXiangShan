from dataclasses import dataclass


@dataclass
class Ftq_Redirect_SRAMEntry:
    # RAS 相关状态（用于重定向时恢复 RAS 栈）
    ssp: int          # UInt(log2Up(RasSize)) → [0, RasSize)
    sctr: int         # RasCtrSize.W → 0 ~ (2^RasCtrSize - 1)
    TOSW: RASPtr      # RAS 写指针
    TOSR: RASPtr      # RAS 读指针
    NOS: RASPtr       # Next of Stack (RAS)
    topAddr: int      # RAS 栈顶返回地址 (VAddrBits)

    # 全局分支历史指针
    histPtr: CGHPtr

    # SC 预测器不同意信号（Option 类型）
    # - 在 FPGA 平台：为 None
    # - 在 ASIC/仿真平台：为 List[bool]（长度 = numBr）
    sc_disagree: Optional[List[bool]] = None

    @classmethod
    def from_spec_info(cls, spec: 'spec_info'):
        """
        从 spec_info 构造 Ftq_Redirect_SRAMEntry
        注意：实际字段需从 spec 的 s3 阶段结果中提取（香山中 s3 才有完整 speculative info）
        """
        return cls(
            ssp=spec.ras_ssp,
            sctr=spec.ras_sctr,
            TOSW=spec.ras_TOSW,
            TOSR=spec.ras_TOSR,
            NOS=spec.ras_NOS,
            topAddr=spec.ras_topAddr,
            histPtr=spec.histPtr,
            sc_disagree=spec.sc_disagree  # 可能为 None
        )

class FTQRedirectMem:
    def __init__(self, size: int = FtqSize):
        self.size = size
        # 初始化默认 entry
        self.mem = [
            Ftq_Redirect_SRAMEntry(
                ssp=0, sctr=0, TOSW=0, TOSR=0, NOS=0,
                topAddr=0, histPtr=0, sc_disagree=None
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
            # 地址无效：返回默认值（或可抛异常，根据需求）
            return Ftq_Redirect_SRAMEntry(0, 0, 0, 0, 0, 0, 0, None)