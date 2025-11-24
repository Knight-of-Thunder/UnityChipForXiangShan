from dataclasses import dataclass
from typing import List
FTQSIZE = 64
@dataclass
class Ftq_RF_Components:
    startAddr: int
    nextLineAddr: int
    fallThruError: bool

    @classmethod
    def from_branch_prediction(cls, bp: BranchPredictionBundle):
        """从 BranchPredictionBundle 构造"""
        return cls(
            startAddr=bp.pc,
            nextLineAddr=bp.pc + 64,  # Cache line = 64 bytes
            fallThruError=bp.fallThruError
        )

class FTQPCMem:
    def __init__(self, size: int = FTQSIZE):
        self.size = size
        self.mem = [Ftq_RF_Components(0, 64, False) for _ in range(size)]

    def write(self, wen: bool, waddr: int, wdata: Ftq_RF_Components):
        if wen and 0 <= waddr < self.size:
            self.mem[waddr] = wdata

    def read(self, ren: bool, raddr: int,) -> List[Ftq_RF_Components]:
        if ren and 0 <= raddr < self.size:
            return mem[raddr]