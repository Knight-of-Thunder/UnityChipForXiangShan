import random
import toffee_test
from ut_frontend.ftq.ftq_top.test.ftq_cover_points2 import *
from ..env import FtqBundle
from ..env import FtqEnv 
import toffee

from dut.FtqTop import DUTFtqTop
import toffee.funcov as fc
from toffee.funcov import CovGroup
from .ftq_cover_points import ftq_cover_points

from .utils import *
from .utils2 import *

class NewDUTFtqTop(DUTFtqTop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newest_entry_target = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_target")
        self.newest_entry_ptr_value = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_ptr_value")
        self.newest_entry_ptr_flag = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_ptr_flag")
        self.newest_entry_target_modified = self.GetInternalSignal("FtqTop_top.Ftq.newest_entry_target_modified")
        self.has_false_hit = self.GetInternalSignal("FtqTop_top.Ftq.has_false_hit")
        self.ifu_redirect_valid = self.GetInternalSignal("FtqTop_top.Ftq.fromIfuRedirect_valid_probe")
        self.ifu_redirect_pc = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_pc")
        self.ifu_redirect_pd_valid = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_pd_valid")
        self.ifu_redirect_pd_isRet = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_pd_isRet")
        self.ifu_redirect_target = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_target")
        self.ifu_redirect_taken = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_cfiUpdate_taken")
        self.ifu_flush = self.GetInternalSignal("FtqTop_top.Ftq.ifuFlush")
        self.ifu_redirect_ftq_idx = self.GetInternalSignal("FtqTop_top.Ftq.__Vtogcov__ifuRedirectReg_next_bits_r_ftqIdx_value")
        self.ifu_redirect_ftq_offset = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_bits_r_ftqOffset")
        self.tobackend_newest_entry_en = self.GetInternalSignal("FtqTop_top.io_toBackend_newest_entry_en")
        self.tobackend_newest_entry_ptr = self.GetInternalSignal("FtqTop_top.io_toBackend_newest_entry_ptr_value")
        self.tobackend_newest_target = self.GetInternalSignal("FtqTop_top.io_toBackend_newest_entry_target")
        self.tobackend_pc_mem_wen = self.GetInternalSignal("FtqTop_top.io_toBackend_pc_mem_wen")
        self.tobackend_pc_mem_waddr = self.GetInternalSignal("FtqTop_top.io_toBackend_pc_mem_waddr")
        self.tobackend_pc_mem_wdata_start = self.GetInternalSignal("FtqTop_top.io_toBackend_pc_mem_wdata_startAddr")
        self.icache_flush = self.GetInternalSignal("FtqTop_top.io_icacheFlush")
        self.toBpu_redirect_bits_cfiUpdate_br_hit = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_br_hit")
        self.toBpu_redirect_bits_cfiUpdate_jr_hit = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_jr_hit")
        self.toBpu_redirect_bits_cfiUpdate_shift = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_shift")
        self.toBpu_redirect_bits_cfiUpdate_addIntoHist = self.GetInternalSignal("FtqTop_top.io_toBpu_redirect_bits_cfiUpdate_addIntoHist")
        self.bpu_ptr = self.GetInternalSignal("FtqTop_top.Ftq.bpuPtr_value")
        self.bpu_ptr_flag = self.GetInternalSignal("FtqTop_top.Ftq.bpuPtr_flag")
        self.ifu_ptr = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtr_value")
        self.ifu_ptr_flag = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtr_flag")
        self.pf_ptr = self.GetInternalSignal("FtqTop_top.Ftq.pfPtr_value")
        self.pf_ptr_flag = self.GetInternalSignal("FtqTop_top.Ftq.pfPtr_flag")
        self.ifu_ptr_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtr_write_value")
        self.ifu_wb_ptr_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuWbPtr_value")
        self.ifu_ptr_plus1_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtrPlus1_value")
        self.ifu_ptr_plus2_write = self.GetInternalSignal("FtqTop_top.Ftq.ifuPtrPlus2_value")
        self.pf_ptr_write = self.GetInternalSignal("FtqTop_top.Ftq.pfPtr_value")
        self.pf_ptr_plus1_write = self.GetInternalSignal("FtqTop_top.Ftq.pfPtrPlus1_value")
        self.topdown_redirect_valid = self.GetInternalSignal("FtqTop_top.io_toIfu_topdown_redirect_valid")
        self.topdown_redirect_debugIsCtrl = self.GetInternalSignal("FtqTop_top.io_toIfu_topdown_redirect_bits_debugIsCtrl")
        self.topdown_redirect_debugIsMemVio = self.GetInternalSignal("FtqTop_top.io_toIfu_topdown_redirect_bits_debugIsMemVio")
        self.toifu_redirect_valid = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_valid")
        self.toifu_redirect_ftqIdx_value = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_bits_ftqIdx_value")
        self.toifu_redirect_ftqOffset = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_bits_ftqOffset")
        self.toifu_redirect_level = self.GetInternalSignal("FtqTop_top.io_toIfu_redirect_bits_level")

        # bins added
        self.canCommit = self.GetInternalSignal("FtqTop_top.Ftq.__Vtogcov__canCommit")
        self.comm_ptr = self.GetInternalSignal("FtqTop_top.Ftq.commPtr_value")
        self.comm_ptr_flag = self.GetInternalSignal("FtqTop_top.Ftq.commPtr_flag")
        # self.fromBackend_redirect_valid = self.GetInternalSignal("FtqTop_top.Ftq.fromBackend_redirect_valid")
        # self.backendRedirectReg_valid_REG = self.GetInternalSignal("FtqTop_top.Ftq.backendRedirectReg_valid_REG")
        self.backendRedirect = self.GetInternalSignal("FtqTop_top.io_fromBackend_redirect_valid")
        self.backendRedirectReg = self.GetInternalSignal("FtqTop_top.Ftq.backendRedirectReg_valid_REG")
        self.allowBpuIn = self.GetInternalSignal("FtqTop_top.Ftq.allowBpuIn")
        self.bpu_in_fire = self.GetInternalSignal("FtqTop_top.Ftq.bpu_in_fire")
        self.bpu_in_stage = self.GetInternalSignal("FtqTop_top.Ftq.bpu_in_stage")
        # self.io_fromBpu_resp_bits_s3_hasRedirect_3 = self.GetInternalSignal("FtqTop_top.io_fromBpu_resp_bits_s3_hasRedirect_3")
        # self.io_fromBpu_resp_bits_s2_hasRedirect_3 = self.GetInternalSignal("FtqTop_top.io_fromBpu_resp_bits_s2_hasRedirect_3")
        # self.io_fromBpu_resp_bits_s2_valid_3 = self.GetInternalSignal("FtqTop_top.io_fromBpu_resp_bits_s2_valid_3")
        # self.io_fromBpu_resp_bits_s3_valid_3 = self.GetInternalSignal("FtqTop_top.io_fromBpu_resp_bits_s3_valid_3")
        self.ifuRedirectToBpu_valid = self.GetInternalSignal("FtqTop_top.Ftq.ifuRedirectReg_next_valid_last_REG") 
        self.ifu_wb_ptr = self.GetInternalSignal("FtqTop_top.Ftq.ifuWbPtr_value")      
        self.ifu_wb_ptr_flag = self.GetInternalSignal("FtqTop_top.Ftq.ifuWbPtr_flag") 
        self.robCommPtr_flag = self.GetInternalSignal("FtqTop_top.Ftq.robCommPtr_flag")
        self.robCommPtr_value = self.GetInternalSignal("FtqTop_top.Ftq.robCommPtr_value")

        self.mmioFtqPtr_flag = self.GetInternalSignal("FtqTop_top.io_mmioCommitRead_mmioFtqPtr_flag")
        self.mmioFtqPtr_value = self.GetInternalSignal("FtqTop_top.io_mmioCommitRead_mmioFtqPtr_value")
        self.mmioLastCommit = self.GetInternalSignal("FtqTop_top.io_mmioCommitRead_mmioLastCommit")
        self.bpu_ftb_update_stall = self.GetInternalSignal("FtqTop_top.Ftq.bpu_ftb_update_stall")
        self.validInstructions = [None] * 16
        for i in range(15):
            self.validInstructions[i + 1] = self.GetInternalSignal(f"FtqTop_top.Ftq.validInstructions_{i + 1}")
        def get_update_target(idx):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.update_target_{idx}")
            
        def get_cfi_index_bits(idx):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.cfiIndex_vec_{idx}_bits")
            
        def get_cfi_index_valid(idx):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.cfiIndex_vec_{idx}_valid")
            
        def get_mispredict_vec(idx, offset):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.mispredict_vec_{idx}_{offset}")

        def get_commit_state_queue_reg(ftq_idx, offset):
            return self.GetInternalSignal(f"FtqTop_top.Ftq.commitStateQueueReg_{ftq_idx}_{offset}")    

        self.get_update_target = get_update_target
        self.get_cfi_index_bits = get_cfi_index_bits
        self.get_cfi_index_valid = get_cfi_index_valid
        self.get_mispredict_vec = get_mispredict_vec
        self.get_commit_state_queue_reg = get_commit_state_queue_reg

        self.ftq_pc_mem_io_commPtrPlus1_rdata_startAddr = self.GetInternalSignal("FtqTop_top.Ftq._ftq_pc_mem_io_commPtrPlus1_rdata_startAddr")
        self.ftq_pc_mem_io_commPtr_rdata_startAddr = self.GetInternalSignal("FtqTop_top.Ftq._ftq_pc_mem_io_commPtr_rdata_startAddr")
  

         
        ################################ Connected to FTQ SUB QUEUES ##############################################
        # ftq_pc_mem
        self.ftq_pc_mem = [
            {} for _ in range(64)
        ]
        fields = ["fallThruError", "nextLineAddr", "startAddr"]
        for waddr in range(64):
            bank = waddr // 16 
            entry = waddr % 16

            for field in fields:
                sig = (
                    f"FtqTop_top.Ftq.ftq_pc_mem.mem."
                    f"dataBanks_{bank}.data_{entry}_{field}"
                )
                self.ftq_pc_mem[waddr][field] = self.GetInternalSignal(sig)

        # ftq_redirect_mem
        self.ftq_redirect_mem = [
            {} for _ in range(64)
        ]
        fields = [
            "NOS_flag",
            "NOS_value",
            "TOSR_flag",
            "TOSR_value",
            "TOSW_flag",
            "TOSW_value",
            "histPtr_flag",
            "histPtr_value",
            "sc_disagree_0",
            "sc_disagree_1",
            "sctr",
            "ssp",
            "topAddr",
        ]
        for waddr in range(64):
            bank = waddr // 16 
            entry = waddr % 16

            for field in fields:
                sig = (
                    f"FtqTop_top.Ftq.ftq_redirect_mem."
                    f"dataBanks_{bank}.data_{entry}_{field}"
                )
                self.ftq_redirect_mem[waddr][field] = self.GetInternalSignal(sig)

        # ftb_entry_mem
        self.ftb_entry_mem = [
            {} for _ in range(64)
        ]
        fields = [        
            "isCall",
            "isRet",
            "isJalr",
            "brSlots_0_offset",         # 4 bits
            "brSlots_0_valid",
            "tailSlot_offset",         # 4 bits
            "tailSlot_sharing",
            "tailSlot_valid",
        ]

        
        for waddr in range(64):
            bank = waddr // 16 
            entry = waddr % 16

            for field in fields:
                sig = (
                    f"FtqTop_top.Ftq.ftb_entry_mem."
                    f"dataBanks_{bank}.data_{entry}_{field}"
                )
                self.ftb_entry_mem[waddr][field] = self.GetInternalSignal(sig)

            # # ---------- brSlots ----------
            # self.ftb_entry_mem[waddr]["brSlots_0"]["offset"] = \
            #     self.GetInternalSignal(f"{base}_brSlots_0_offset")

            # self.ftb_entry_mem[waddr]["brSlots_0"]["valid"] = \
            #     self.GetInternalSignal(f"{base}_brSlots_0_valid")

            # # ---------- entry flags ----------
            # self.ftb_entry_mem[waddr]["isCall"] = \
            #     self.GetInternalSignal(f"{base}_isCall")

            # self.ftb_entry_mem[waddr]["isJalr"] = \
            #     self.GetInternalSignal(f"{base}_isJalr")

            # self.ftb_entry_mem[waddr]["isRet"] = \
            #     self.GetInternalSignal(f"{base}_isRet")

            # # ---------- tailSlot ----------
            # self.ftb_entry_mem[waddr]["tailSlot"] = {}

            # self.ftb_entry_mem[waddr]["tailSlot"]["offset"] = \
            #     self.GetInternalSignal(f"{base}_tailSlot_offset")

            # self.ftb_entry_mem[waddr]["tailSlot"]["sharing"] = \
            #     self.GetInternalSignal(f"{base}_tailSlot_sharing")

            # self.ftb_entry_mem[waddr]["tailSlot"]["valid"] = \
            #     self.GetInternalSignal(f"{base}_tailSlot_valid")

        # ftq_meta_mem
        # 64 x 576 flatten ram， each 576 bit entry holds meta and ftb_entry info
        # ram = self.GetInternalSignal(
        #     "FtqTop_top.Ftq.ftq_meta_1r_sram.sram.array.array.array_8_ext.ram"
        # )
        # print(f"DEBUG: RAM total bits = {ram.value.bit_length()}")
        # self.ftq_meta_mem = [ FtqMetaEntry() for _ in range(64)]

        # # for i in range(64):
        # #     raw_entry = get_entry(ram, i)
        # #     self.ftq_meta_mem[i] = unpack_ftq_meta(raw_entry)
        # ram_path = "FtqTop_top.Ftq.ftq_meta_1r_sram.sram.array.array.array_8_ext.ram"
        # for i in range(64):
        #     # 核心修改：在路径字符串里加上索引 [{i}]
        #     line_signal = self.GetInternalSignal(f"{ram_path}[{i}]")
        #     if line_signal is not None:
        #         raw_val = line_signal.value
        #         self.ftq_meta_mem[i] = unpack_ftq_meta(raw_val)
        #     else:
        #         # 如果这种写法报错，说明接口需要不同的数组访问方式
        #         print(f"Error: Cannot access index {i}")

        # ################################ Connected to FTQ STATUS QUEUES ##############################################
        self.update_targets = [None] * 64
        for i in range(64): 
            self.update_targets[i] = self.GetInternalSignal(f"FtqTop_top.Ftq.update_target_{i}")
        
        self.cfiIndex_vec = [{} for _ in range(64)]
        fields = [
            "bits",
            "valid",
        ]
        for i in range(64):
            for field in fields:
                sig = f"FtqTop_top.Ftq.cfiIndex_vec_{i}_{field}"
                self.cfiIndex_vec[i][field] = self.GetInternalSignal(sig)
        
        self.mispredict_vecs = [[None for _ in range(16)] for _ in range(64)]
        for i in range(64):
            for j in range(16):
                sig = f"FtqTop_top.Ftq.mispredict_vec_{i}_{j}"
                self.mispredict_vecs[i][j] = self.GetInternalSignal(sig)

        self.pred_stages = [ None for _ in range(64)]
        for i in range(64):
            sig = f"FtqTop_top.Ftq.pred_stage_{i}"
            self.pred_stages[i] = self.GetInternalSignal(sig)
        
        self.commitStateQueue = [[None for _ in range(16)] for _ in range(64)]
        for i in range(64):
            for j in range(16):
                sig = f"FtqTop_top.Ftq.commitStateQueueReg_{i}_{j}"
                self.commitStateQueue[i][j] = self.GetInternalSignal(sig)

        self.entry_fetch_status = [ None for _ in range(64)]
        for i in range(64):
            sig = f"FtqTop_top.Ftq.entry_fetch_status_{i}"
            self.entry_fetch_status[i] = self.GetInternalSignal(sig)
        
        self.entry_hit_status = [ None for _ in range(64)]
        for i in range(64):
            sig = f"FtqTop_top.Ftq.entry_hit_status_{i}"
            self.entry_hit_status[i] = self.GetInternalSignal(sig)

        
        fields = [
            "isCall",
            "isRet",
            "isJalr",
            "valid",
            "brSlots_0_offset",
            "brSlots_0_sharing",
            "brSlots_0_valid",
            "brSlots_0_lower",
            "brSlots_0_tarStat",
            "tailSlot_offset",
            "tailSlot_sharing",
            "tailSlot_valid",
            "tailSlot_lower",
            "tailSlot_tarStat",
            "pftAddr",
            "carry",
            "last_may_be_rvi_call",
            "strong_bias_1",
            "strong_bias_0",
        ]
        self.ftq_meta_1r_sram_io_rdata_0_ftb_entry = {
            field: self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_meta_1r_sram.__Vtogcov__io_rdata_0_ftb_entry_{field}")
            for field in fields
        }


        self.ftq_pd_mem_io_rdata_1 = {}
        self.ftq_pd_mem_io_rdata_1["brMask"] = [self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_pd_mem.__Vtogcov__io_rdata_1_brMask_{i}")  for i in range(16)]
        self.ftq_pd_mem_io_rdata_1["rvcMask"] =[self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_pd_mem.__Vtogcov__io_rdata_1_rvcMask_{i}") for i in range(16)]
        self.ftq_pd_mem_io_rdata_1["jmpInfo_bits"] =[self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_pd_mem.__Vtogcov__io_rdata_1_jmpInfo_bits_{i}") for i in range(3)]
        self.ftq_pd_mem_io_rdata_1["jmpInfo_valid"] = self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_pd_mem.__Vtogcov__io_rdata_1_jmpInfo_valid")
        self.ftq_pd_mem_io_rdata_1["jmpOffset"] = self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_pd_mem.__Vtogcov__io_rdata_1_jmpOffset")
        self.ftq_pd_mem_io_rdata_1["jalTarget"] = self.GetInternalSignal(f"FtqTop_top.Ftq.ftq_pd_mem.__Vtogcov__io_rdata_1_jalTarget")
        self._ftq_pd_mem_io_rdata_1_jalTarget = self.GetInternalSignal(f"FtqTop_top.Ftq._ftq_pd_mem_io_rdata_1_jalTarget")


    # def distance_between_bpu_and_commit(self):
    #     return distance_between(enq_flag = self.bpu_ptr_flag.value, enq_value = self.bpu_ptr.value, deq_flag = self.comm_ptr_flag.value, deq_value = self.comm_ptr.value)
    
        # The pins need in cover_points
        self.fromIfuRedirect_valid_probe = self.GetInternalSignal("FtqTop_top.Ftq.fromIfuRedirect_valid_probe")
        
        self.realAhdValid = self.GetInternalSignal("FtqTop_top.Ftq.realAhdValid")
        # self.io_fromBackend_redirect_valid = self.backendRedirect.value
        # self.backendRedirectReg_valid_REG = self.GetInternalSignal("FtqTop_top.Ftq.backendRedirectReg_valid_REG").value
        self.ftb_entry_gen_io_is_br_full = self.GetInternalSignal("FtqTop_top.Ftq._FTBEntryGen_io_is_br_full")
        self.ftb_entry_gen_io_is_jalr_target_modified = self.GetInternalSignal("FtqTop_top.Ftq._FTBEntryGen_io_is_jalr_target_modified")
        self.ftb_entry_gen_io_is_new_br = self.GetInternalSignal("FtqTop_top.Ftq._FTBEntryGen_io_is_new_br")
        self.ftb_entry_gen_io_is_strong_bias_modified = self.GetInternalSignal("FtqTop_top.Ftq._FTBEntryGen_io_is_strong_bias_modified")


    def gen_bpu_ptr(self) -> CircularQueuePtr:
        """生成一个BPU指针"""
        return CircularQueuePtr(FTQSIZE, self.bpu_ptr_flag.value, self.bpu_ptr.value)
    
    def gen_ifu_ptr(self) -> CircularQueuePtr:
        """生成一个IFU指针"""
        return CircularQueuePtr(FTQSIZE, self.ifu_ptr_flag.value, self.ifu_ptr.value)
    
    def gen_pf_ptr(self) -> CircularQueuePtr:
        """生成一个PF指针"""
        return CircularQueuePtr(FTQSIZE, self.pf_ptr_flag.value, self.pf_ptr.value)
    
    def gen_comm_ptr(self) -> CircularQueuePtr:
        """生成一个COMM指针"""
        return CircularQueuePtr(FTQSIZE, self.comm_ptr_flag.value, self.comm_ptr.value)
    
    def gen_ifu_wb_ptr(self) -> CircularQueuePtr:
        """生成一个IFU写回指针"""
        return CircularQueuePtr(FTQSIZE, self.ifu_wb_ptr_flag.value, self.ifu_wb_ptr.value)
    
    def gen_rob_comm_ptr(self) -> CircularQueuePtr:
        """生成一个ROB提交指针"""
        return CircularQueuePtr(FTQSIZE, self.robCommPtr_flag.value, self.robCommPtr_value.value)
    
    def gen_mmio_ftq_ptr(self) -> CircularQueuePtr:
        """生成一个MMIO FTQ指针"""
        return CircularQueuePtr(FTQSIZE, self.mmioFtqPtr_flag.value, self.mmioFtqPtr_value.value)

    def gen_newest_entry_ptr(self) -> CircularQueuePtr:
        """生成一个指向最新条目的指针"""
        return CircularQueuePtr(FTQSIZE, self.newest_entry_ptr_value.value, self.newest_entry_ptr_flag.value)  # 假设最新条目指针没有flag位

    def valid_entries(self) -> int:
        """计算FTQ中有效条目数"""
        return distance_between(self.gen_bpu_ptr(), self.gen_comm_ptr())
    
    # def fromBpu_resp_ready(self) -> bool:
    #     """判断从BPU获取响应是否就绪"""
    #     return self.GetInternalSignal("FtqTop_top.Ftq.fromBpu_resp_ready").value

    # def verify_allow_bpu_in(self) -> bool:
    #     """判断是否允许BPU入队"""
    #     return (not self.ifu_flush.value) and (not self.backendRedirectReg_valid_REG.value) or (not self.toBackend_redirect_valid.value)

    # def verify_bpu_in_fire(self) -> bool:
    #     """判断BPU入队是否触发"""
    #     return self.bpu_in_fire.value

    # allow_to_ifu = allow_bpu_in
    
    def gen_ftq_meta_1r_sram_io_rdata_0_ftb_entry_value(self):
        ftq_meta_1r_sram_io_rdata_0_ftb_entry_value = {
            k: v.value for k, v in self.ftq_meta_1r_sram_io_rdata_0_ftb_entry.items()
        }
        return ftq_meta_1r_sram_io_rdata_0_ftb_entry_value
    
    def gen_ftq_pd_mem_io_rdata_1_value(self):
        ftq_pd_mem_io_rdata_1_value = {
            k: [x.value for x in v] if isinstance(v, list) else v.value
            for k, v in self.ftq_pd_mem_io_rdata_1.items()
        }
        return ftq_pd_mem_io_rdata_1_value



@toffee_test.fixture
async def ftq_env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(NewDUTFtqTop,"clock")  
    toffee.start_clock(dut)
    ftq_bundle = FtqBundle.from_prefix('io_')
    ftq_bundle.bind(dut)  
    toffee_request.add_cov_groups(ftq_cover_points(dut, ftq_bundle))  
    # add cov groups for test_ftq_top10, which is related to ftq commit
    toffee_request.add_cov_groups([
        to_bpu_redirect(dut),
        update_stall(dut),
        can_commit(dut),
        can_move_commit_ptr(dut),
        update_rob_commit_ptr(ftq_bundle.fromBackend),
        mmio_last_commit(dut),
        ftb_entry_gen_modify_old(dut),
        update_ftb_entry(dut)
    ])
    yield FtqEnv(ftq_bundle, dut=dut)  
   