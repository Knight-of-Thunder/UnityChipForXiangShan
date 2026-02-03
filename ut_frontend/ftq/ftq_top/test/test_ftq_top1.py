import random
from this import d
import toffee_test
import pytest
from collections import namedtuple

# from ut_frontend.bpu.tagesc.bundle.port import BranchPredictionBundle
from ut_frontend.ftq.ftq_top.env.ftq_bundle import BranchPredictionResp, BranchPredictionBundle, BranchPredictionBundleforS23
from ut_frontend.ftq.ftq_top.ref.ftq_pc_mem import Ftq_RF_Components
from ..ref.ftq_ref import FtqAccurateRef, BpuPacket, FtqPointer, get_random_ptr_before_bpu
from .top_test_fixture import ftq_env
from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 
from .utils import *
from ..ref.FtqPtr import FTQSIZE, CircularQueuePtr
from ..ref.FtqRef import FTQ

# baseline test: only normal enq without redirect or flush
@toffee_test.testcase
async def test_bpu_enq_normal(ftq_env):
    # Get DUT and Ref, reset DUT
    dut = ftq_env.dut
    ref = FTQ()
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()
    fallThruErrors_before = []
    for i in range(64):
        fallThruErrors_before.append(dut.ftq_pc_mem[i]["fallThruError"].value)
    print("bpuptr_dut after reset: ", dut.gen_bpu_ptr())

    for i in range(3):
        print(f"----------------------- warm up --------------------------")
        bpu_ptr = ref.bpu_ptr
        port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)
        port_dict_s1["valid"] = 1
        port_dict_s2["valid_3"] = 0
        port_dict_s3["valid_3"] = 0
        await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
        await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
        await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
        dut.RefreshComb()
        bpu_in_fire = check_with_ref_before_write(dut)
        selected_resp = ftq_env.ftq_agent.bundle.fromBpuNew.selected_resp()
        selected_stage = check_bpu_in_stage(dut)
        update_ftq_ref_state(bpu_in_fire, selected_stage, selected_resp, ref)
        dut.Step()
        if i == 0:
            dut.Step()
        # Check bpuPtr update
        print("bpuptr_ref: ", ref.bpu_ptr)
        print("bpuptr_dut: ", dut.gen_bpu_ptr())
        assert ref.bpu_ptr == dut.gen_bpu_ptr()
    
    for i in range(10640):
        print(f"----------------------- Cycle {i} --------------------------")
        bpu_ptr = ref.bpu_ptr
        port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)

        await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
        await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
        await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
        # ftq_bundle = ftq_env.ftq_agent.bundle.fromBpuNew.selected_resp()
        # print(ftq_bundle)
        dut.RefreshComb()
        bpu_in_fire = check_with_ref_before_write(dut)
        selected_resp = ftq_env.ftq_agent.bundle.fromBpuNew.selected_resp()
        print("selected_resp: ", hex(selected_resp.pc_3.value), selected_resp.full_pred_3_fallThroughErr.value, selected_resp.full_pred_3_hit.value)
        selected_stage = check_bpu_in_stage(dut)
        update_ftq_ref_state(bpu_in_fire, selected_stage, selected_resp, ref)
        dut.Step()
        # Check bpuPtr update
        print("bpuptr_ref: ", ref.bpu_ptr)
        print("bpuptr_dut: ", dut.gen_bpu_ptr())
        assert ref.bpu_ptr == dut.gen_bpu_ptr()
    bpu_ptr = ref.bpu_ptr
    port_dict_s1, port_dict_s2, port_dict_s3 = gen_bpu_resp(bpu_ptr)
    port_dict_s1["valid"] = 0
    port_dict_s2["valid_3"] = 0
    port_dict_s3["valid_3"] = 0
    await ftq_env.ftq_agent.drive_s1_full_signals(port_dict_s1)
    await ftq_env.ftq_agent.drive_s2_full_signals(port_dict_s2)
    await ftq_env.ftq_agent.drive_s3_full_signals(port_dict_s3)
    dut.Step(10)
    # Check FTQ PC memory
    errors = check_with_ref_after_write(dut, ref)
    for i in errors:
        print(i)
    # for i in range(64):
    #     if(fallThruErrors_before[i] != dut.ftq_pc_mem[i]["fallThruError"].value):
    #         print(f"entry{i}  before: {fallThruErrors_before[i]}, after: {dut.ftq_pc_mem[i]["fallThruError"].value}")
        

def check_with_ref_before_write(dut):
    dut.RefreshComb()
    check_resp_ready(dut)
    resp_fire = bpu_resp_fire_ref(dut)
    allow_bpu_in = check_allow_bpu_in(dut)
    bpu_in_fire = check_bpu_in_fire(dut)
    return bpu_in_fire


def check_ftq_pc_entry(ref_entry, dut_entry, idx):
    errors = []

    if ref_entry.startAddr != dut_entry["startAddr"].value:
        errors.append(
            f"[FTQ_PC][{idx}] startAddr mismatch: "
            f"ref={ref_entry.startAddr:#x}, dut={dut_entry['startAddr'].value:#x}"
        )

    if ref_entry.nextLineAddr != dut_entry["nextLineAddr"].value:
        errors.append(
            f"[FTQ_PC][{idx}] nextLineAddr mismatch: "
            f"ref={ref_entry.nextLineAddr:#x}, dut={dut_entry['nextLineAddr'].value:#x}"
        )

    if (ref_entry.fallThruError) != (dut_entry["fallThruError"].value):
        errors.append(
            f"[FTQ_PC][{idx}] fallThruError mismatch: "
            f"ref={ref_entry.fallThruError}, dut={dut_entry['fallThruError'].value}"
        )

    return errors

def check_ftq_pc_mem(ref_mem:FTQ, dut_ftq_pc_mem):
    all_errors = []

    for i in range(FTQSIZE):
        ref_entry = ref_mem.ftq_pc_mem.read(True, i)
        dut_entry = dut_ftq_pc_mem[i]

        errs = check_ftq_pc_entry(ref_entry, dut_entry, i)
        all_errors.extend(errs)

    return all_errors

def check_with_ref_after_write(dut, ref):
    return check_ftq_pc_mem(ref, dut.ftq_pc_mem)


def write_into_ftq_pc_mem(bpu_in_fire, selected_stage, selected_resp, ref: FTQ):
    if selected_stage == 0:
        ftq_idx_value = ref.bpu_ptr.value
    else:
        ftq_idx_value = selected_resp.ftq_idx_value.value
    print("write into ftq pc mem at idx:", ftq_idx_value)
    ref.ftq_pc_mem.write(bpu_in_fire, ftq_idx_value, Ftq_RF_Components.from_branch_prediction(selected_resp))


def update_ftq_ref_state(bpu_in_fire, selected_stage, selected_resp: BranchPredictionBundle, ref: FTQ):
    write_into_ftq_pc_mem(bpu_in_fire, selected_stage, selected_resp, ref)
    update_ftq_ref_bpu_ptr(bpu_in_fire, selected_stage, selected_resp, ref)

def update_ftq_ref_bpu_ptr(bpu_in_fire, selected_stage, selected_resp: BranchPredictionBundle, ref: FTQ):
    if not bpu_in_fire:
        return
    if selected_stage == 0:
        ref.bpu_ptr += 1
    else:
        print("redirect bpu ptr:", CircularQueuePtr(FTQSIZE, selected_resp.ftq_idx_flag.value, selected_resp.ftq_idx_value.value) )
        ref.bpu_ptr = CircularQueuePtr(FTQSIZE, selected_resp.ftq_idx_flag.value, selected_resp.ftq_idx_value.value) + 1


def check_resp_ready(dut):
    assert dut.io_fromBpu_resp_ready.value == bpu_resp_ready_ref(dut)

def check_allow_bpu_in(dut):
    allow_bpu_in = allow_bpu_in_ref(dut)
    assert dut.allowBpuIn.value == allow_bpu_in
    return allow_bpu_in

def check_bpu_in_fire(dut):
    bpu_in_fire = bpu_in_fire_ref(dut)
    assert dut.bpu_in_fire.value == bpu_in_fire
    return bpu_in_fire

def check_bpu_in_stage(dut):
    selected_stage = selected_stage_ref(dut)
    assert dut.bpu_in_stage.value == selected_stage
    return selected_stage

    
