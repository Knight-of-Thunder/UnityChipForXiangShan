import random

from ut_frontend.ftq.ftq_top.env.ftq_bundle import BranchPredictionBundle, FromBackendBundle
from ut_frontend.ftq.ftq_top.ref.FtqRef import FTQ
# from .top_test_fixture import NewDUTFtqTop
####################
# Utils for ftqPtr #
####################
from ..ref.FtqPtr import CircularQueuePtr, distance_between
FTQSIZE = 64
# 生成用于端口赋值的随机字典
def gen_bpu_branch_resp_dict() -> dict:
    """根据端口字段生成随机赋值字典"""
    return {
        # 3 stages 阶段共享信号
        "valid": random.randint(0, 1),
        "pc_3": random.randint(0, (1 << 50) - 1),  # 50位
        "full_pred_3_br_taken_mask_0": random.randint(0, 1),
        "full_pred_3_br_taken_mask_1": random.randint(0, 1),
        "full_pred_3_slot_valids_0": random.randint(0, 1),
        "full_pred_3_slot_valids_1": random.randint(0, 1),
        "full_pred_3_targets_0": random.randint(0, (1 << 50) - 1),  # 50位
        "full_pred_3_targets_1": random.randint(0, (1 << 50) - 1),
        "full_pred_3_offsets_0": random.randint(0, (1 << 4) - 1),
        "full_pred_3_offsets_1": random.randint(0, (1 << 4) - 1),
        "full_pred_3_fallThroughAddr": random.randint(0, (1 << 50) - 1),
        "full_pred_3_fallThroughErr": random.randint(0, 1),
        "full_pred_3_is_br_sharing": random.randint(0, 1),
        "full_pred_3_hit": random.randint(0, 1),
        # s2/s3 阶段专用信号
        "valid_3": random.randint(0, 1),
        "hasRedirect_3": random.randint(0, 1),
        "ftq_idx_flag": random.randint(0, 1),
        "ftq_idx_value": random.randint(0, (1 << 6) - 1),  # 6位
    }

def gen_last_stage_ftb_entry_dict() -> dict:
    """根据端口字段生成随机赋值字典"""
    return {
        "isCall": random.randint(0, 1),
        "isRet": random.randint(0, 1),
        "isJalr": random.randint(0, 1),
        "valid": random.randint(0, 1),
        "last_may_be_rvi_call": random.randint(0, 1),
        "carry": random.randint(0, 1),
        "pftAddr": random.randint(0, 15),          # 4 bits
        "brSlots_0_offset": random.randint(0, 15),         # 4 bits
        "brSlots_0_sharing": random.randint(0, 1),
        "brSlots_0_valid": random.randint(0, 1),
        "tailSlot_offset": random.randint(0, 15),         # 4 bits
        "tailSlot_sharing": random.randint(0, 1),
        "tailSlot_valid": random.randint(0, 1),
    }

def gen_last_stage_spec_info_dict() -> dict:
    """根据端口字段生成随机赋值字典"""
    return {
            "histPtr_flag": random.randint(0, 1),
            "histPtr_value": random.randint(0, (1 << 8) - 1),   # 8 bits
            "ssp": random.randint(0, (1 << 4) - 1),             # 4 bits
            "sctr": random.randint(0, (1 << 3) - 1),            # 3 bits
            "TOSW_flag": random.randint(0, 1),
            "TOSW_value": random.randint(0, (1 << 5) - 1),      # 5 bits
            "TOSR_flag": random.randint(0, 1),
            "TOSR_value": random.randint(0, (1 << 5) - 1),      # 5 bits
            "NOS_flag": random.randint(0, 1),
            "NOS_value": random.randint(0, (1 << 5) - 1),       # 5 bits
            "topAddr": random.randint(0, (1 << 50) - 1),        # 50 bits
            "sc_disagree_0": random.randint(0, 1),
            "sc_disagree_1": random.randint(0, 1)
    }

# 一点未满足的输入约束：s1下一个周期的pc： 应该为它预测的跳转目标，如果在预测为不跳转的情况下，又应该为多少
# 其次，s2阶段的pc应该为上一周期s1的pc，s3阶段的pc应该为上一周期s2的pc
# 但是我们在FTQ这里主要以验证FTQ的正确性为主，故减少了对输入约束的考虑，后续可以考虑添加
def gen_bpu_resp(bpu_ptr: CircularQueuePtr = None):
    port_dict_s1 = gen_bpu_branch_resp_dict()
    if(bpu_ptr is not None):
        bpuPtr = bpu_ptr
        port_dict_s1["ftq_idx_flag"] = bpuPtr.flag
        port_dict_s1["ftq_idx_value"] = bpuPtr.value
    else:
        bpuPtr = CircularQueuePtr(FTQSIZE, flag=port_dict_s1["ftq_idx_flag"], value=port_dict_s1["ftq_idx_value"])
    bpuPtr_sub1 = bpuPtr - 1
    bpuPtr_sub2 = bpuPtr_sub1 - 1
    port_dict_s2 = gen_bpu_branch_resp_dict()
    port_dict_s3 = gen_bpu_branch_resp_dict()

    # Set constraint signals
    port_dict_s2["ftq_idx_flag"] = bpuPtr_sub1.flag
    port_dict_s2["ftq_idx_value"] = bpuPtr_sub1.value
    port_dict_s3["ftq_idx_flag"] = bpuPtr_sub2.flag
    port_dict_s3["ftq_idx_value"] = bpuPtr_sub2.value

    # Set redirect info not totally random
    if random.random() < 0.5:
        port_dict_s2["valid_3"] = 1
        port_dict_s2["hasRedirect_3"] = 1
    else:
        port_dict_s2["valid_3"] = 0
        port_dict_s2["hasRedirect_3"] = 0
    
    if random.random() < 0.5:
        port_dict_s3["valid_3"] = 1
        port_dict_s3["hasRedirect_3"] = 1
    else:
        port_dict_s3["valid_3"] = 0
        port_dict_s3["hasRedirect_3"] = 0

    return port_dict_s1, port_dict_s2, port_dict_s3

def gen_backend_inputs_dict():
    """生成 backend -> ftq 的输入字典（随机）"""
    return {
        "io_fromBackend_redirect_valid": random.randint(0, 1),
        "io_fromBackend_redirect_bits_ftqIdx_flag": random.randint(0, 1),
        "io_fromBackend_redirect_bits_ftqIdx_value": random.randint(0, (1 << 6) - 1),
        "io_fromBackend_redirect_bits_ftqOffset": random.randint(0, (1 << 4) - 1),
        "io_fromBackend_redirect_bits_level": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_pc": random.randint(0, (1 << 50) - 1),
        "io_fromBackend_redirect_bits_cfiUpdate_target": random.randint(0, (1 << 50) - 1),
        "io_fromBackend_redirect_bits_cfiUpdate_taken": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_isMisPred": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_backendIGPF": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_backendIPF": random.randint(0, 1),
        "io_fromBackend_redirect_bits_cfiUpdate_backendIAF": random.randint(0, 1),
        "io_fromBackend_redirect_bits_debugIsCtrl": random.randint(0, 1),
        "io_fromBackend_redirect_bits_debugIsMemVio": random.randint(0, 1),
        "io_fromBackend_ftqIdxAhead_0_valid": random.randint(0, 1),
        "io_fromBackend_ftqIdxAhead_0_bits_value": random.randint(0, (1 << 6) - 1),
        "io_fromBackend_ftqIdxSelOH_bits": random.randint(0, (1 << 3) - 1),
    }

def gen_rob_commits_dict():
    """生成单个 rob_commit 字段字典（用于 0..7 个 commit 槽）"""
    return {
        "valid": random.randint(0, 1),
        "commitType": random.randint(0, (1 << 3) - 1),
        "ftqIdx_flag": random.randint(0, 1),
        "ftqIdx_value": random.randint(0, (1 << 6) - 1),
        "ftqOffset": random.randint(0, (1 << 4) - 1),
    }

def gen_ifu_inputs_dict():
    """生成 ifu -> ftq 的输入字典（随机）"""
    d = {}
    d["io_fromIfu_pdWb_valid"] = random.randint(0, 1)
    # PCs
    for i in range(16):
        d[f"io_fromIfu_pdWb_bits_pc_{i}"] = random.randint(0, (1 << 50) - 1)
    # pd fields for 16 lanes
    for i in range(16):
        d[f"io_fromIfu_pdWb_bits_pd_{i}_valid"] = random.randint(0, 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_isRVC"] = random.randint(0, 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_brType"] = random.randint(0, (1 << 2) - 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_isCall"] = random.randint(0, 1)
        d[f"io_fromIfu_pdWb_bits_pd_{i}_isRet"] = random.randint(0, 1)
    # ftq idx / misc
    d["io_fromIfu_pdWb_bits_ftqIdx_flag"] = random.randint(0, 1)
    d["io_fromIfu_pdWb_bits_ftqIdx_value"] = random.randint(0, (1 << 6) - 1)
    d["io_fromIfu_pdWb_bits_misOffset_valid"] = random.randint(0, 1)
    d["io_fromIfu_pdWb_bits_misOffset_bits"] = random.randint(0, (1 << 4) - 1)
    d["io_fromIfu_pdWb_bits_cfiOffset_valid"] = random.randint(0, 1)
    d["io_fromIfu_pdWb_bits_target"] = random.randint(0, (1 << 50) - 1)
    d["io_fromIfu_pdWb_bits_jalTarget"] = random.randint(0, (1 << 50) - 1)
    # instrRange bits
    for i in range(16):
        d[f"io_fromIfu_pdWb_bits_instrRange_{i}"] = random.randint(0, 1)
    return d

def gen_ifu_inputs_dict_full() -> dict:
    """生成 ifu -> ftq 的完整输入字典（随机），包含 IFU 字段和若干 backend rob_commits 字段以便驱动器使用"""
    d = gen_ifu_inputs_dict()
    # add 8 backend rob_commits entries (io_fromBackend_rob_commits_0..7_<field>)
    # for i in range(8):
    #     rc = gen_rob_commits_dict()
    #     prefix = f"io_fromBackend_rob_commits_{i}_"
    #     for k, v in rc.items():
    #         d[prefix + k] = v
    return d | gen_rob_commits_dict_full()

def gen_rob_commits_dict_full() -> dict:
    """生成完整的 8 个 rob_commit 字段字典（随机），用于驱动器使用"""
    d = {}
    for i in range(8):
        rc = gen_rob_commits_dict()
        prefix = f"io_fromBackend_rob_commits_{i}_"
        for k, v in rc.items():
            if k != "valid":
                d[prefix + "bits_" + k] = v
            else:
                d[prefix + k] = v
    return d

# This method do not make sure receive resp ready, need ready first
def set_bpu_resp_fire(dut):
    dut.io_fromBpu_resp_valid.value = 1
    # Will fire if ready at the same time

# allowBpuIn := !ifuFlush && !backendRedirect.valid && !backendRedirectReg.valid
# ifuFlush := fromIfuRedirect.valid || ifuRedirectToBpu.valid, 
# 其中ifuRedirectToBpu实际上是前者的寄存器版本，保留上一周期前者的值，所以ifuFlush实际是将来自ifu的flush保留两个周期
# fromIfuRedirect.valid              := pdWb.valid && pdWb.bits.misOffset.valid && !backendFlush
# backendRedirect.valid := io.fromBackend.redirect.valid, backendFlush将backendRedirect保存两个周期
# involved input pins:
# io_fromIfu_pdWb_valid
# io_fromIfu_pdWb_bits_misOffset_valid
# io_fromBackend_redirect_valid
# def set_allow_bpu_in(dut):

# # This input will make ifuFlush, keep 2 cycles
# ifuFlush_input_dict ={
#     "io_fromBackend_redirect_valid":0,
#     "io_fromIfu_pdWb_bits_misOffset_valid":1,
#     "io_fromIfu_pdWb_valid":1,
# }
# # This input will make backendRedirect, keep 2 cycles
# backendRedirect_input_dict={
#     "io_fromBackend_redirect_valid":1,
# }





# The set will keep 2 cycles
def set_ifuFlush(dut, dict):
    dut.io_fromBackend_redirect_valid.value = dict.get("io_fromBackend_redirect_valid", 0)
    dut.io_fromIfu_pdWb_bits_misOffset_valid.value = dict.get("io_fromIfu_pdWb_bits_misOffset_valid", 0)
    dut.io_fromIfu_pdWb_valid.value = dict.get("io_fromIfu_pdWb_valid", 0)


def bpu_resp_ready_ref(dut):
    if dut.canCommit.value == 1 or dut.valid_entries() < FTQSIZE:
        assert dut.io_fromBpu_resp_ready.value == 1
        return 1
    else:
        assert dut.io_fromBpu_resp_ready.value == 0
        return 0

# resp_ready & resp_valid will make resp_fire, but it need call dut.RefreshComb() to refresh the circuit 
# and then resp_fire will actually be true
def bpu_resp_fire_ref(dut):
    resp_ready = bpu_resp_ready_ref(dut)
    resp_valid = dut.io_fromBpu_resp_valid.value
    resp_fire = resp_ready & resp_valid
    return resp_fire


# from BPU S1 result
def enq_fire_ref(dut):
    resp_fire = bpu_resp_fire_ref(dut)
    allow_bpu_in = allow_bpu_in_ref(dut)
    enq_fire = resp_fire & allow_bpu_in
    return enq_fire

# S2 redirect
def S2_redirect_ref(dut):
    S2_redirect_valid = dut.io_fromBpu_resp_bits_s2_valid_3.value
    S2_redirect_hasRedirect = dut.io_fromBpu_resp_bits_s2_hasRedirect_3.value
    return S2_redirect_valid and S2_redirect_hasRedirect

# S3 redirect
def S3_redirect_ref(dut):
    S3_redirect_valid = dut.io_fromBpu_resp_bits_s3_valid_3.value
    S3_redirect_hasRedirect = dut.io_fromBpu_resp_bits_s3_hasRedirect_3.value
    return S3_redirect_valid and S3_redirect_hasRedirect

# from BPU result
def bpu_in_fire_ref(dut):
    resp_fire = bpu_resp_fire_ref(dut)
    allow_bpu_in = allow_bpu_in_ref(dut)
    S2_redirect = S2_redirect_ref(dut)
    S3_redirect = S3_redirect_ref(dut)
    return allow_bpu_in and (S2_redirect or S3_redirect or resp_fire)

def allow_bpu_in_ref(dut):
    ifuFlush = dut.ifu_flush.value
    backendRedirect = dut.backendRedirect.value
    backendRedirectReg = dut.backendRedirectReg.value
    return not ifuFlush and not backendRedirect and not backendRedirectReg

def selected_stage_ref(dut):
    S2_redirect = S2_redirect_ref(dut)
    S3_redirect = S3_redirect_ref(dut)
    if S3_redirect:
        return 2
    elif S2_redirect:
        return 1
    else:
        return 0 

def get_idx_of_selected_stage_ref(selectedResp: BranchPredictionBundle, selected_stage: int, ref: FTQ):
    if selected_stage == 0:
        ftq_idx_value = ref.bpu_ptr.value
    else:
        ftq_idx_value = selectedResp.ftq_idx_value.value
    return ftq_idx_value

# jiexi selectedResp
def getTaget_ref(selectedResp: BranchPredictionBundle):
    hit = selectedResp.full_pred_3_hit.value
    fallThroughErr = selectedResp.full_pred_3_fallThroughErr.value
    if hit and not fallThroughErr:
        # taken
        # get first taken target
        if selectedResp.full_pred_3_br_taken_mask_0.value == 1 and selectedResp.full_pred_3_slot_valids_0.value == 1:
            return selectedResp.full_pred_3_targets_0.value
        elif selectedResp.full_pred_3_is_br_sharing.value:
            if selectedResp.full_pred_3_br_taken_mask_1.value == 1 and selectedResp.full_pred_3_slot_valids_1.value == 1:
                return selectedResp.full_pred_3_targets_1.value
            return selectedResp.full_pred_3_fallThroughAddr.value
        elif selectedResp.full_pred_3_slot_valids_1.value == 1:
            return selectedResp.full_pred_3_targets_1.value
        return selectedResp.full_pred_3_fallThroughAddr.value
    else:
        # not taken
        return selectedResp.pc_3.value + 32

def getCfi_ref(selectedResp: BranchPredictionBundle):
    hit = selectedResp.full_pred_3_hit.value
    if hit:
        if selectedResp.full_pred_3_slot_valids_0.value == 1 and selectedResp.full_pred_3_br_taken_mask_0.value == 1:
            valid = 1
            offset = selectedResp.full_pred_3_offsets_0.value
        elif selectedResp.full_pred_3_is_br_sharing.value:
            if selectedResp.full_pred_3_slot_valids_1.value == 1 and selectedResp.full_pred_3_br_taken_mask_1.value == 1:
                valid = 1
                offset = selectedResp.full_pred_3_offsets_1.value
            else:
                valid = 0
                offset = 15 # when no takens, set cfiIndex to PredictWidth-1
        elif selectedResp.full_pred_3_slot_valids_1.value == 1:
            valid = 1
            offset = selectedResp.full_pred_3_offsets_1.value
        else:
            valid = 0
            offset = 15
    else:
        valid = 0
        offset = 15
    return {"valid":valid, "bits": offset}

h_not_hit, h_false_hit,  h_hit = range(3)

c_empty     = 0
c_toCommit  = 1
c_committed = 2
c_flushed   = 3

def validInstructions_ref(dut):

    # canCommit = dut.gen_rob_comm_ptr() != dut.gen_ifu_wb_ptr() and not dut.bpu_ftb_update_stall.value == 0
    commPtr = dut.gen_comm_ptr()
    row = [i.value for i in dut.commitStateQueue[commPtr.value]]
    validInstructions = [
        (s == c_toCommit or s == c_committed)
        for s in row
    ]
    # validInstructions = (inst.value for inst in dut.validInstructions)
    # indices = [i for i, v in enumerate(validInstructions) if v]
    # idx = indices[-1] if indices else -1
    # lastInstructionStatus = dut.instructionStatus[idx].value if idx >= 0 else None
    # canCommit = canCommit and (dut.gen_rob_comm_ptr() > dut.gen_ifu_wb_ptr() or \
    #                            (any(validInstructions) and lastInstructionStatus == c_committed))
    return validInstructions

def lastInstructionStatus_ref(dut, validInstructions):
    commPtr = dut.gen_comm_ptr()
    row = [i.value for i in dut.commitStateQueue[commPtr.value]]
    indices = [i for i, v in enumerate(validInstructions) if v]
    idx = indices[-1] if indices else -1
    if idx >= 0:
        return row[idx]
    else:
        return None

def firstInstructionFlushed_ref(row):
    firstInstructionFlushed = (
    row[0] == c_flushed or (row[0] == c_empty and row[1] == c_flushed))
    return firstInstructionFlushed

def canCommit_ref(dut, validInstructions):
    has_valid = any(validInstructions)
    commPtr = dut.gen_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    robCommPtr = dut.gen_rob_comm_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions)
    print("lastInstructionStatus: ", lastInstructionStatus)
    print("commPtr: ", commPtr.value)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canCommit = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
            (robCommPtr > commPtr)
            or (
                has_valid
                and lastInstructionStatus == c_committed
            )
        )
    )
    return canCommit

def canMoveCommPtr_ref(dut, validInstructions):
    has_valid = any(validInstructions)
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions)
    commPtr = dut.gen_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    robCommPtr = dut.gen_rob_comm_ptr()
    commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
    firstInstructionFlushed = firstInstructionFlushed_ref(commit_state)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canMoveCommPtr = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
                (robCommPtr > commPtr)
                or (
                    has_valid
                    and lastInstructionStatus == c_committed
                )
                or firstInstructionFlushed
        )
    )
    return canMoveCommPtr

def last_valid_rob_commit_ref(fromBackend: FromBackendBundle):
    rob_commits = []
    # for i in range(8):
    #     rb = getattr(fromBackend, f"rob_commits_{i}", None)
    #     if rb is None:
    #         print(f"rob_commits_{i} not found")
    #     else:
    #         print(f"rob_commits_{i}.valid = {rb.valid.value}")
    for i in range(8):
        rob_commit = getattr(fromBackend, f"rob_commits_{i}")
        rob_commits.append(rob_commit)

    valid_commits = [commit for commit in rob_commits if commit.valid.value == 1]

    return valid_commits[-1] if valid_commits else None


def mmioLastCommit_ref(dut):
    commPtr = dut.gen_comm_ptr()
    # mmioReadValid = dut.mmioReadValid.value
    mmioReadValid = 1
    mmioReadPtr = dut.gen_mmio_ftq_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions_ref(dut))
    has_valid = any(validInstructions_ref(dut))
    mmioLastCommit = (
        mmioReadValid
        and (
            (commPtr > mmioReadPtr)
            or (
                commPtr == mmioReadPtr
                and has_valid
                and lastInstructionStatus == c_committed
            )
        )
    )
    return mmioLastCommit

TAR_OVF = 1
TAR_UDF = 2
TAR_FIT = 0
BR_OFFSET_LEN  = 12
JMP_OFFSET_LEN = 20

class FtbSlot:
    def __init__(self, offsetLen, subOffsetLen=None):
        if subOffsetLen is not None:
            assert subOffsetLen <= offsetLen

        self.offsetLen = offsetLen
        self.subOffsetLen = subOffsetLen

        self.valid = False
        self.offset = 0

        self.lower = 0
        self.tarStat = TAR_FIT
        self.sharing = False


    def set_lower_stat_by_target(self, pc, target, is_share):
        offLen = self.subOffsetLen if is_share else self.offsetLen
        VAddrBits = 50
        shift_amt = offLen + 1
        higher_mask = (1 << (VAddrBits - shift_amt)) - 1
        
        pc_higher = (pc >> shift_amt) & higher_mask
        target_higher = (target >> shift_amt) & higher_mask

        if target_higher > pc_higher:
            stat = TAR_OVF
        elif target_higher < pc_higher:
            stat = TAR_UDF
        else:
            stat = TAR_FIT

        lower_mask = (1 << offLen) - 1
        raw_lower = (target >> 1) & lower_mask

        self.lower = raw_lower & ((1 << self.offsetLen) - 1)
        
        self.tarStat = stat
        self.sharing = int(is_share)

    # def set_lower_stat_by_target(self, pc, target, is_share):
    #     # 1. 确定 offLen
    #     offLen = self.subOffsetLen if is_share else self.offsetLen
    #     VAddrBits = 50
    #     shift_amt = offLen + 1
        
    #     # 2. 提取 Higher 部分 (对应 pc(VAddrBits-1, offLen+1))
    #     # 这里的 mask 位数必须严格等于 VAddrBits - 1 - (offLen + 1) + 1
    #     higher_len = VAddrBits - shift_amt
    #     higher_mask = (1 << higher_len) - 1
        
    #     pc_higher = (pc >> shift_amt) & higher_mask
    #     target_higher = (target >> shift_amt) & higher_mask

    #     # 3. 比较状态
    #     if target_higher > pc_higher:
    #         stat = TAR_OVF
    #     elif target_higher < pc_higher:
    #         stat = TAR_UDF
    #     else:
    #         stat = TAR_FIT

    #     # 4. 提取 Lower 部分 (对应 target(offLen, 1))
    #     # 注意：Chisel 的 (msb, lsb) 是包含边界的
    #     # target(offLen, 1) 表示提取 offLen - 1 + 1 = offLen 位
    #     lower_mask = (1 << offLen) - 1
    #     raw_lower = (target >> 1) & lower_mask

    #     # 5. ZeroExt 扩展到 self.offsetLen 位
    #     # 确保 raw_lower 放入 self.lower 时符合硬件位宽
    #     self.lower = raw_lower & ((1 << self.offsetLen) - 1)# Python 整数不限位宽，但在对比信号时需要注意 mask
    #     self.tarStat = stat
    #     self.sharing = int(is_share)
    
    # --------------------------------------
    # getTarget 
    # --------------------------------------
    def get_target(self, pc):
        offLen = self.subOffsetLen if self.sharing else self.offsetLen
        assert offLen is not None and offLen > 0

        pc_higher = pc >> (offLen + 1)

        if self.tarStat == TAR_OVF:
            higher = pc_higher + 1
        elif self.tarStat == TAR_UDF:
            higher = pc_higher - 1
        else:
            higher = pc_higher

        target = (
            (higher << (offLen + 1))
            | (self.lower << 1)
        )

        return target

    # --------------------------------------
    # fromAnotherSlot
    # --------------------------------------
    def from_another_slot(self, that):
        if self.offsetLen > that.offsetLen:
            assert self.subOffsetLen == that.offsetLen
            self.sharing = True
        else:
            assert self.offsetLen == that.offsetLen
            self.sharing = False

        self.offset = that.offset
        self.tarStat = that.tarStat
        self.valid = that.valid

        # ZeroExt 
        self.lower = that.lower

from copy import deepcopy


# class BrSlot:
#     def __init__(self):
#         self.valid = False
#         self.offset = 0
#         self.lower = 0
#         self.sharing = False  # 是否和其他slot共享

#     def set_lower_by_target(self, start_addr, target, is_share):
#         self.lower = target  # 行为级直接存完整target
#         self.sharing = is_share

#     def from_another_slot(self, other):
#         self.valid = other.valid
#         self.offset = other.offset
#         self.lower = other.lower
#         self.sharing = other.sharing


class TailSlot(FtbSlot):
    def set_by_jmp_target(self, pc, target):
        self.set_lower_stat_by_target(pc, target, False)

class FTBEntry:
    def __init__(self, numBrSlot, dict=None):
        self.numBrSlot = numBrSlot
        self.numBr = numBrSlot + 1
        self.valid = False
        numBr = self.numBr

        self.brSlots = [
            FtbSlot(offsetLen=BR_OFFSET_LEN)
            for _ in range(numBrSlot)
        ]

        self.strong_bias = [False] * numBr

        self.tailSlot = TailSlot(offsetLen=JMP_OFFSET_LEN, subOffsetLen=BR_OFFSET_LEN)
        self.allSlots = [*self.brSlots, self.tailSlot]

        self.pftAddr = 0
        self.carry = False

        self.isJalr = False  
        self.isCall = False
        self.isRet = False
        self.last_may_be_rvi_call = False
        if dict is not None:
            self.valid = dict.get("valid", False)
            self.pftAddr = dict.get("pftAddr", 0)
            self.carry = dict.get("carry", False)
            self.isJalr = dict.get("isJalr", False)
            self.isCall = dict.get("isCall", False)
            self.isRet = dict.get("isRet", False)
            self.last_may_be_rvi_call = dict.get("last_may_be_rvi_call", False)

            for i in range(numBrSlot):
                slot_dict = {
                    "valid": dict.get(f"brSlots_{i}_valid", False),
                    "offset": dict.get(f"brSlots_{i}_offset", 0),
                    "lower": dict.get(f"brSlots_{i}_lower", 0),
                    "tarStat": dict.get(f"brSlots_{i}_tarStat", TAR_FIT),
                    "sharing": dict.get(f"brSlots_{i}_sharing", False),
                }
                self.brSlots[i].valid = slot_dict["valid"]
                self.brSlots[i].offset = slot_dict["offset"]
                self.brSlots[i].lower = slot_dict["lower"]
                self.brSlots[i].tarStat = slot_dict["tarStat"]
                self.brSlots[i].sharing = slot_dict["sharing"]
            
            for i in range(numBr):
                self.strong_bias[i] = dict.get(f"strong_bias_{i}", False)

            tail_dict = {
                "valid": dict.get("tailSlot_valid", False),
                "offset": dict.get("tailSlot_offset", 0),
                "lower": dict.get("tailSlot_lower", 0),
                "tarStat": dict.get("tailSlot_tarStat", TAR_FIT),
                "sharing": dict.get("tailSlot_sharing", False),
            }
            self.tailSlot.valid = tail_dict["valid"]
            self.tailSlot.offset = tail_dict["offset"]
            self.tailSlot.lower = tail_dict["lower"]
            self.tailSlot.tarStat = tail_dict["tarStat"]
            self.tailSlot.sharing = tail_dict["sharing"]

    # ---------------------------
    # helper functions
    # ---------------------------

    def get_br_recorded_vec(self, offset):
        return [
            slot.valid and slot.offset == offset
            for slot in self.brSlots
        ] + [
            self.tailSlot.valid and self.tailSlot.offset == offset and self.tailSlot.sharing
        ]

    @property
    def brValids(self):
        return [s.valid for s in self.brSlots] + [
            self.tailSlot.valid and self.tailSlot.sharing
        ]

    @property
    def brOffset(self):
        return [s.offset for s in self.brSlots] + [
            self.tailSlot.offset
        ]

    @property
    def jmpValid(self):
        return self.tailSlot.valid and not self.tailSlot.sharing

    @property
    def noEmptySlotForNewBr(self):
        return all(s.valid for s in self.allSlots)

    def as_dict(self):
        d = {
            "valid": self.valid,
            "pftAddr": self.pftAddr,
            "carry": self.carry,
            "isJalr": self.isJalr,
            "isCall": self.isCall,
            "isRet": self.isRet,
            "last_may_be_rvi_call": self.last_may_be_rvi_call,
        }
        for i in range(self.numBrSlot):
            d.update({
                f"brSlots_{i}_valid": self.brSlots[i].valid,
                f"brSlots_{i}_offset": self.brSlots[i].offset,
                f"brSlots_{i}_lower": self.brSlots[i].lower,
                f"brSlots_{i}_tarStat": self.brSlots[i].tarStat,
                f"brSlots_{i}_sharing": self.brSlots[i].sharing,
            })
        for i in range(self.numBr):
            d.update({
                f"strong_bias_{i}": self.strong_bias[i],
            })
        d.update({
            "tailSlot_valid": self.tailSlot.valid,
            "tailSlot_offset": self.tailSlot.offset,
            "tailSlot_lower": self.tailSlot.lower,
            "tailSlot_tarStat": self.tailSlot.tarStat,
            "tailSlot_sharing": self.tailSlot.sharing,
        })
        return d

    # ---------------------------
    # debug helper
    # ---------------------------
    def dump(self):
        print("FTBEntry:")
        print(" valid:", self.valid)
        for i, s in enumerate(self.brSlots):
            print(
                f"  BR[{i}] valid={s.valid} "
                f"offset={s.offset} lower={s.lower} "
                f"tarStat={s.tarStat} sharing={s.sharing} "
                f"bias={self.strong_bias[i]}"
            )
        print("  Tail:",
              "valid=", self.tailSlot.valid,
              "offset=", self.tailSlot.offset,
              "lower=", self.tailSlot.lower,
              "tarStat=", self.tailSlot.tarStat,
              "sharing=", self.tailSlot.sharing)
        print(" pftAddr:", self.pftAddr,
              "carry:", self.carry)

def ftb_entry_gen(
    start_addr,
    old_entry: FTBEntry,
    pd,
    cfiIndex_valid,
    cfiIndex_bits,
    target,
    hit, 
    mispredict_vec,
    numBrSlot=1,
    PredictWidth=16,
):
    numBr = numBrSlot + 1
    instOffsetBits = 1

    carryPos = (PredictWidth - 1).bit_length() + instOffsetBits  # log2Ceil 

    def get_lower(pc):
        # move instOffsetBits bit right ，then take  (carryPos - instOffsetBits) bits
        return (pc >> instOffsetBits) & ((1 << (carryPos - instOffsetBits)) - 1)

    # ------------------------------------------------
    # 1 init entry
    # ------------------------------------------------

    init_entry = FTBEntry(numBrSlot=1)
    init_entry.valid = True

    cfi_is_br = pd["brMask"][cfiIndex_bits] and cfiIndex_valid

    entry_has_jmp = pd["jmpInfo_valid"]

    new_jmp_is_jal = entry_has_jmp and not pd["jmpInfo_bits"][0] and cfiIndex_valid
    new_jmp_is_jalr = entry_has_jmp and pd["jmpInfo_bits"][0] and cfiIndex_valid
    new_jmp_is_call = entry_has_jmp and pd["jmpInfo_bits"][1] and cfiIndex_valid
    new_jmp_is_ret = entry_has_jmp and pd["jmpInfo_bits"][2] and cfiIndex_valid

    cfi_is_jal = cfiIndex_bits == pd["jmpOffset"] and new_jmp_is_jal
    cfi_is_jalr = cfiIndex_bits == pd["jmpOffset"] and new_jmp_is_jalr
    
    # ---- case br ----
    if cfi_is_br:
        print("cfi is br")
        slot = init_entry.brSlots[0]
        slot.valid = True
        slot.offset = cfiIndex_bits
        # slot.set_lower_stat_by_target(start_addr, target, numBr == 1)
        slot.set_lower_stat_by_target(start_addr, target, numBr == 1)

        init_entry.strong_bias[0] = True

    print("cfiindex valid:", cfiIndex_valid)

    # ---- case jmp ----
    if entry_has_jmp:
        print("entry_has_jmp")
        init_entry.tailSlot.offset = pd["jmpOffset"]
        init_entry.tailSlot.valid = new_jmp_is_jal or new_jmp_is_jalr
        print("DEBUG: start_addr = ", start_addr)
        print("DEBUG: target = ", target)
        print("DEBUG: jalTarget = ", pd["jalTarget"])
        init_entry.tailSlot.set_lower_stat_by_target(
            start_addr,
            target if cfi_is_jalr else pd["jalTarget"],
            False,
        )
        print("DEBUG: tailSlot_lower = ", init_entry.tailSlot.lower)
        init_entry.strong_bias[-1] = new_jmp_is_jalr

    # last_jmp_rvi
    last_jmp_rvi = entry_has_jmp and pd["jmpOffset"] == (PredictWidth - 1) and not pd["rvcMask"][-1]

    # jmpPft
    jmp_inst_len = 1 if pd["rvcMask"][pd["jmpOffset"]] else 2
    jmp_pft = get_lower(start_addr) + pd["jmpOffset"] + jmp_inst_len
    print("jmp_pft: ", jmp_pft)
    print("lower start addr: ", get_lower(start_addr))
    print("entry has jmp: ", entry_has_jmp)
    print("last jmp rvi:", last_jmp_rvi)
    print("jmpOffset: ", pd["jmpOffset"])
    print("last rvc mask:",pd["rvcMask"][-1])

    if entry_has_jmp and not last_jmp_rvi:
        init_entry.pftAddr = jmp_pft & 0b1111
        init_entry.carry = (jmp_pft >> (carryPos - instOffsetBits)) & 1
    else:
        init_entry.pftAddr = get_lower(start_addr)
        init_entry.carry = True

    # last_may_be_rvi_call
    init_entry.last_may_be_rvi_call = (
        pd["jmpOffset"] == PredictWidth - 1 and not pd["rvcMask"][pd["jmpOffset"]]
    )

    init_entry.isJalr = new_jmp_is_jalr
    init_entry.isCall = new_jmp_is_call
    init_entry.isRet = new_jmp_is_ret

    # ------------------------------------------------
    # 2 hit check：check if it is new br
    # ------------------------------------------------

    oe = old_entry
    br_recorded_vec = oe.get_br_recorded_vec(cfiIndex_bits)
    br_recorded = any(br_recorded_vec)

    is_new_br = cfi_is_br and not br_recorded
    new_br_offset = cfiIndex_bits

    # insert position
    new_br_insert_onehot = []
    # for i in range(numBr):
    #     if i == 0:
    #         cond = (not oe.brSlots[0].valid) or new_br_offset < oe.brSlots[0].offset
    #     else:
    #         cond = (
    #             oe.brSlots[i - 1].valid
    #             and new_br_offset > oe.brSlots[i - 1].offset
    #             and (
    #                 not oe.brSlots[i].valid
    #                 or new_br_offset < oe.brSlots[i].offset
    #             )
    #         )
    #     new_br_insert_onehot.append(cond)
    for i in range(numBr):
        if i == 0:
            cond = (not oe.brSlots[0].valid) or new_br_offset < oe.brSlots[0].offset
        else:
            cond = (
                oe.allSlots[i - 1].valid
                and new_br_offset > oe.allSlots[i - 1].offset
                and (
                    not oe.allSlots[i].valid
                    or new_br_offset < oe.allSlots[i].offset
                )
            )
        new_br_insert_onehot.append(cond)

    old_entry_modified = deepcopy(oe)

    # insert logic
    for i in range(numBr):
        slot = old_entry_modified.allSlots[i]

        if new_br_insert_onehot[i]:
            slot.valid = True
            slot.offset = new_br_offset
            slot.set_lower_stat_by_target(start_addr, target, i == numBr - 1)
            # slot.set_lower_stat_by_target(start_addr, target, False)
            old_entry_modified.strong_bias[i] = True

        elif new_br_offset > oe.allSlots[i].offset:
            old_entry_modified.strong_bias[i] = False

        else:
            if i != 0:
                noNeedToMoveFromFormerSlot = (i == numBr - 1) and not oe.brSlots[numBrSlot-1].valid
                if not noNeedToMoveFromFormerSlot:
                    slot.from_another_slot(oe.allSlots[i - 1])
                    old_entry_modified.strong_bias[i] = oe.strong_bias[i]
    
    may_have_to_replace = oe.noEmptySlotForNewBr  # 所有br槽都满了
    pft_need_to_change = is_new_br and may_have_to_replace

    ############### notice ###########################
    # if pft_need_to_change:
    #     print("pft need to change", pft_need_to_change)
    #     #  new_pft_offset
    #     # Chisel: Mux(!new_br_insert_onehot.asUInt.orR, new_br_offset, oe.allSlotsForBr.last.offset)
    #     if not any(new_br_insert_onehot):
    #         # 新br应该插入到所有现有br之后 → pft用新br的offset
    #         new_pft_offset = new_br_offset
    #     else:
    #         # 新br插入到某个现有br之前 → pft用原来最后一个br的offset
    #         new_pft_offset = oe.brSlots[-1].offset
        
    #     # ── 更新 pftAddr 和 carry ──
    #     base_lower = get_lower(start_addr)
    #     new_pft_addr = base_lower + new_pft_offset
    #     print("new_pft_addr:", new_pft_addr)
    #     old_entry_modified.pftAddr = new_pft_addr
        
    #     # carry = (base_lower +& new_pft_offset) 的最高位
    #     # 即检查加法结果是否超出了 (carryPos - instOffsetBits) 位表示范围
    #     addr_bits = carryPos - instOffsetBits
    #     old_entry_modified.carry = (new_pft_addr >> addr_bits) & 1 != 0
        
    #     # ── 清空 jmp 相关标志（因为pft现在指向branch而非jmp）─
    #     old_entry_modified.last_may_be_rvi_call = False
    #     old_entry_modified.isCall = False
    #     old_entry_modified.isRet = False
    #     old_entry_modified.isJalr = False

    if pft_need_to_change:
        print(f"[DEBUG] pft_need_to_change triggered: {pft_need_to_change}")

        # 1. 选择 new_pft_offset (对应 Chisel 的 Mux 逻辑)
        # 如果 new_br_insert_onehot 全为 0 (orR 为 false)，说明新分支插入在末尾
        if not any(new_br_insert_onehot):
            new_pft_offset = new_br_offset
        else:
            # 否则，PFT 指向原本的最后一个分支
            new_pft_offset = oe.brSlots[-1].offset

        # 2. 模拟硬件位宽截断 (Crucial for Bit-level Accuracy)
        # 在 FTQ 中，pftAddr 的位宽通常由 carryPos - instOffsetBits 决定
        lower_width = carryPos - instOffsetBits
        mask = (1 << lower_width) - 1

        # 获取 base_lower 并确保它符合硬件截断后的位宽
        base_lower = get_lower(start_addr) & mask
        
        # 确保 offset 也在有效范围内 (通常 offset 位宽较小)
        pft_off = new_pft_offset & mask

        # 3. 模拟 Chisel 的 +& 操作 (带有进位的加法)
        # Chisel: (getLower +& new_pft_offset)
        # 结果会比输入多 1 位，最高位即为 carry
        full_sum = base_lower + pft_off
        
        # 提取低位作为 pftAddr
        new_pft_addr = full_sum & mask
        
        # 提取第 lower_width 位作为进位 (MSB)
        # 例如 lower_width=12，则检查第 12 位 (从0开始数) 是否为 1
        carry_bit = (full_sum >> lower_width) & 1

        # 4. 更新 Entry 状态
        old_entry_modified.pftAddr = new_pft_addr
        old_entry_modified.carry = bool(carry_bit)

        # 5. 清空 JMP 相关标志位 (PFT 现在指向的是 Branch 后的地址)
        old_entry_modified.last_may_be_rvi_call = False
        old_entry_modified.isCall = False
        old_entry_modified.isRet = False
        old_entry_modified.isJalr = False

        print(f"[DEBUG] New PFT Addr: {hex(new_pft_addr)}, Carry: {old_entry_modified.carry}")
    # ------------------------------------------------
    # 3 jalr target modify
    # ------------------------------------------------

    old_target = oe.tailSlot.get_target(start_addr)
    old_tail_is_jmp = not oe.tailSlot.sharing

    jalr_target_modified = (
        new_jmp_is_jalr
        and old_target != target
        and old_tail_is_jmp
    )

    old_entry_jmp_target_modified = deepcopy(oe)

    if jalr_target_modified:
        old_entry_jmp_target_modified.tailSlot.set_lower_stat_by_target(
            start_addr, target, False
        )
        old_entry_jmp_target_modified.strong_bias = [False] * numBr

    # ------------------------------------------------
    # 4 strong bias modify
    # ------------------------------------------------

    old_entry_strong_bias = deepcopy(oe)
    strong_bias_modified = False

    # for i in range(numBr):
    #     if br_recorded_vec[i]:
    #         old_entry_strong_bias.strong_bias[i] = (
    #             oe.strong_bias[i]
    #             and cfiIndex_valid
    #             and oe.brSlots[i].valid
    #             and cfiIndex_bits == oe.brSlots[i].offset
    #         )
    #         if oe.strong_bias[i] and not old_entry_strong_bias.strong_bias[i]:
    #             strong_bias_modified = True
    if br_recorded_vec[0]:
        old_entry_strong_bias.strong_bias[0] = (
            oe.strong_bias[0] and cfiIndex_valid and oe.brSlots[0].valid 
            and cfiIndex_bits == oe.brSlots[0].offset
        )
    elif br_recorded_vec[numBr - 1]:
        old_entry_strong_bias.strong_bias[0] = False
        old_entry_strong_bias.strong_bias[numBr - 1] = (
            oe.strong_bias[numBr - 1] and cfiIndex_valid and oe.brValids[numBr - 1]
            and cfiIndex_bits == oe.brOffset[numBr - 1]
        )
    # strong_bias_modified
    for i in range(numBr):
        if oe.strong_bias[i] and oe.brValids[i] and not old_entry_strong_bias.strong_bias[i]:
            strong_bias_modified = True
            break
    # ------------------------------------------------
    # 5 choose final entry
    # ------------------------------------------------

    if not hit:
        new_entry = init_entry
    else:
        if is_new_br:
            new_entry = old_entry_modified
            print("use old_entry_modified")
        elif jalr_target_modified:
            new_entry = old_entry_jmp_target_modified
            print("use old_entry_jmp_target_modified")
        else:
            new_entry = old_entry_strong_bias
            print("use old_entry_strong_bias")

    # ------------------------------------------------
    # 6 out put signal
    # ------------------------------------------------

    taken_mask = [
        cfiIndex_valid and new_entry.brValids[i] and
        new_entry.brOffset[i] == cfiIndex_bits
        for i in range(numBr)
    ]

    jmp_taken = (
        new_entry.jmpValid
        and new_entry.tailSlot.offset == cfiIndex_bits
    )

    mispred_mask = [
        new_entry.brValids[i]
        and mispredict_vec[new_entry.brOffset[i]]
        for i in range(numBr)
    ]

    mispred_mask.append(
        new_entry.jmpValid
        and mispredict_vec[pd["jmpOffset"]]
    )

    if hit and not is_new_br and not jalr_target_modified and not strong_bias_modified:
        print("is old")
    else:
        print("is new")
    print("hit" if hit else "not hit")
    return {
        "new_entry": new_entry,
        "new_br_insert_pos": new_br_insert_onehot,
        "taken_mask": taken_mask,
        "jmp_taken": jmp_taken,
        "mispred_mask": mispred_mask,
        "is_init_entry": not hit,
        "is_old_entry": hit and not is_new_br and not jalr_target_modified and not strong_bias_modified,
        "is_new_br": hit and is_new_br,
        "is_jalr_target_modified": hit and jalr_target_modified,
        "is_strong_bias_modified": hit and strong_bias_modified,
        "is_br_full": hit and is_new_br and oe.noEmptySlotForNewBr,
        "cfi_is_br": cfi_is_br
    }

def commit_mispredict(
    mis,
    commit_state,
):

    return [
        m and (state == c_committed)
        for m, state in zip(mis, commit_state)
    ]

# # We need 2 cycles to get the correct inputs for ftb_entry_gen
# async def get_ftb_entry_gen_input(dut, newest_entry_target_reg):
#     commPtr = dut.gen_comm_ptr()
#     # Cycle 1
#     start_addr = dut.ftq_pc_mem_io_commPtr_rdata_startAddr.value
#     use_newest = dut.gen_comm_ptr() == dut.gen_newest_entry_ptr()
#     print("commit ptr:", dut.gen_comm_ptr())
#     print("newest entry ptr:", dut.gen_newest_entry_ptr())
#     commPtrPlus1_rdata_startAddr = dut.ftq_pc_mem_io_commPtrPlus1_rdata_startAddr.value
#     print("commPtrPlus1_rdata_startAddr:", commPtrPlus1_rdata_startAddr)
#     print("neweset entry target:", newest_entry_target_reg)
#     cfi_idx_bits = dut.cfiIndex_vec[commPtr.value]["bits"].value
#     cfi_idx_valid = dut.cfiIndex_vec[commPtr.value]["valid"].value
    
#     mispredict_vec = [i.value for i in dut.mispredict_vecs[commPtr.value]]
#     commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
#     mispredict_vec = commit_mispredict(mispredict_vec,commit_state)
#     await dut.AStep(1)
#     # Cycle 2
#     old_entry = FTBEntry(numBrSlot=1, dict=dut.gen_ftq_meta_1r_sram_io_rdata_0_ftb_entry_value())
#     pd = dut.gen_ftq_pd_mem_io_rdata_1_value()
#     # cfi_idx_bits = dut.cfiIndex_vec[commPtr.value]["bits"].value
#     # cfi_idx_valid = dut.cfiIndex_vec[commPtr.value]["valid"].value
#     target = newest_entry_target_reg if use_newest else commPtrPlus1_rdata_startAddr
#     hit  = dut.entry_hit_status[commPtr.value].value == h_hit
#     # mispredict_vec = [i.value for i in dut.mispredict_vecs[commPtr.value]]
#     # commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
#     # mispredict_vec = commit_mispredict(mispredict_vec,commit_state)
#     print("DEBUG for input result:")
#     for name in ["start_addr", "old_entry", "pd", "cfi_idx_valid", "cfi_idx_bits", "target", "hit", "mispredict_vec"]:
#         print(f"{name}: {locals()[name]}")
        
#     return start_addr, old_entry, pd, cfi_idx_valid, cfi_idx_bits, target, hit, mispredict_vec