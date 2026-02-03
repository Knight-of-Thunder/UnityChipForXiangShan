from .FtqPtr import *
# from .status_queue import *
# from .ftb_entry_mem import *
from .ftq_pc_mem import *
# from .ftq_pd_mem import *
# from .ftq_meta_mem import *
from .ftq_redirect_mem import *

FTQSIZE = 64
class FTQ:
    def __init__(self, size=FTQSIZE):
        self.size = size
        # FTQ ptrs
        self.bpu_ptr = CircularQueuePtr(flag=False, value=0)
        self.ifu_ptr = CircularQueuePtr(flag=False, value=0)
        self.ifu_wb_ptr = CircularQueuePtr(flag=False, value=0)
        self.comm_ptr = CircularQueuePtr(flag=False, value=0)
        self.rob_comm_ptr = CircularQueuePtr(flag=False, value=0)
        self.pf_ptr = CircularQueuePtr(flag=False, value=0)

        # FTQ Sub Queue
        # self.ftb_entry_mem = FTBEntryMem(size)
        self.ftq_pc_mem = FTQPCMem(size)
        # self.ftq_pd_mem = FTQPDMem(size)
        # self.meta_mem = FTQMeta1RSram(size)
        self.ftq_redirect_mem = FTQRedirectMem(size)

        # Status Queue
        # self.fetch_status = EntryFetchStatusQueue(size)
        # self.update_targets = UpdateTargetQueue(size)
        # self.cfi_indexes = CfiIndexVec(size)
        # self.mis_predicts = MispredictVec(size)
        # self.pred_stages = PredStageQueue(size)
        # self.commit_states = CommitStateQueue(size)
        # self.entry_hits = EntryHitStatusQueue(size)
        # self.entry_fetch_status = EntryFetchStatusQueue(size)

    # def write_from_bpu(self, wen: bool, waddr: int, pc_data, meta_data, redirect_data):
    #     if wen:
    #         self.ftq_pc_mem.write(True, waddr, pc_data)
    #         self.meta_mem.write(True, waddr, meta_data)
    #         self.redirect_mem.write(True, waddr, redirect_data)

    # def enqueue_from_bpu(self, pred):
    #     if self.can_enqueue():
    #         idx = self.bpu_ptr % self.size
    #         self.ftq_pc_mem[idx] = pred.pc_info
    #         self.ftq_pd_mem[idx] = None  # 待写回
    #         self.meta_mem[idx] = pred.meta
    #         self.redirect_mem[idx] = pred.redirect_info
    #         self.fetch_status[idx] = Status.TO_SEND
    #         self.bpu_ptr += 1

    # def generate_ifu_request(self):
    #     if self.ifu_ptr != self.bpu_ptr and self.fetch_status[self.ifu_ptr % self.size] == Status.TO_SEND:
    #         idx = self.ifu_ptr % self.size
    #         req = {
    #             'nextStartAddr': self.ftq_pc_mem[idx].next_line_addr,
    #             'ftqOffset': self.ftq_pc_mem[idx].branch_offset
    #         }
    #         return req
    #     return None

    # def handle_pd_writeback(self, wb_data):
    #     idx = wb_data.ftq_idx % self.size
    #     self.ftq_pd_mem[idx] = wb_data.pd_info
    #     self.ifu_wb_ptr += 1

    # def handle_redirect(self, target_pc, redirect_idx):
    #     # 重置所有指针到 redirect_idx + 1
    #     next_ptr = redirect_idx + 1
    #     self.bpu_ptr = next_ptr
    #     self.ifu_ptr = next_ptr
    #     self.pf_ptr = next_ptr
    #     # 清空相关状态...
    #     self.icache_flush()

    # def commit_and_update_bpu(self):
    #     if self.can_commit():
    #         idx = self.comm_ptr % self.size
    #         pc = self.ftq_pc_mem[idx]
    #         pd = self.ftq_pd_mem[idx]       
    #         meta = self.meta_mem[idx]
    #         new_ftb_entry = self.ftb_entry_gen(pc, pd, meta)
    #         self.send_to_bpu(new_ftb_entry)
    #         self.comm_ptr += 1