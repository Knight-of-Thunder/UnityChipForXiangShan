import random
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
        "full_pred_3_targets_0": random.randint(0, (1 << 64) - 1),  # 64位
        "full_pred_3_targets_1": random.randint(0, (1 << 64) - 1),
        "full_pred_3_offsets_0": random.randint(0, (1 << 64) - 1),
        "full_pred_3_offsets_1": random.randint(0, (1 << 64) - 1),
        "full_pred_3_fallThroughAddr": random.randint(0, (1 << 64) - 1),
        "full_pred_3_fallThroughErr": random.randint(0, 1),
        "full_pred_3_is_br_sharing": random.randint(0, 1),
        "full_pred_3_hit": random.randint(0, 1),
        # s2/s3 阶段专用信号
        "valid_3": random.randint(0, 1),
        "hasRedirect_3": random.randint(0, 1),
        "ftq_idx_flag": random.randint(0, 1),
        "ftq_idx_value": random.randint(0, (1 << 6) - 1),  # 6位
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

# def set_enq_fire(dut):

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




