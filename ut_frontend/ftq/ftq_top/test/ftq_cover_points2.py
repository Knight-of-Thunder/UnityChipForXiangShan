from tokenize import group
import toffee.funcov as fc
from toffee.funcov import CovGroup
from ut_frontend.ftq.ftq_top.env.ftq_bundle import FromBackendBundle
from .utils import canCommit_ref, validInstructions_ref, lastInstructionStatus_ref, firstInstructionFlushed_ref
from .utils import last_valid_rob_commit_ref

c_empty     = 0
c_toCommit  = 1
c_committed = 2
c_flushed   = 3

def redirect_from_flush(dut):
    return dut.fromIfuRedirect_valid_probe.value

def redirect_from_backend(dut):
    realAhdValid = dut.realAhdValid.value
    backendRedirectReg = dut.backendRedirectReg.value
    backendRedirect = dut.backendRedirect.value
    return backendRedirect if realAhdValid else backendRedirectReg

def to_bpu_redirect(dut)-> CovGroup:
    group = CovGroup("commit redirect info to BPU")
    group.add_watch_point(dut, {"redirect_from_flush": redirect_from_flush}, name="redirect_from_flush")
    group.add_watch_point(dut, {"redirect_from_backend": redirect_from_backend}, name="redirect_from_backend")
    return group

# def test_cov_group():
#     m = 1
#     group = CovGroup("test cov group")
#     group.add_watch_point(m, {
#         "test cov group": fc.Eq(1),
#         }, name="test cov group")

def update_stall(dut)-> CovGroup:
    group = CovGroup("we need stall when update BPU")
    group.add_watch_point(dut.bpu_ftb_update_stall, {
        "no stall": fc.Eq(0),
        "have stall": fc.Ne(0),
        }, name="bpu_ftb_update_stall")
    return group

def can_commit_cond1(dut):
    validInstructions = validInstructions_ref(dut)
    commPtr = dut.gen_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    robCommPtr = dut.gen_rob_comm_ptr()
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canCommit = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
            (robCommPtr > commPtr)
        )
    )
    return canCommit

def can_commit_cond2(dut):
    validInstructions = validInstructions_ref(dut)
    has_valid = any(validInstructions)
    commPtr = dut.gen_rob_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canCommit = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
                has_valid
                # and lastInstructionStatus == c_committed
        )
    )
    return canCommit

def can_commit(dut)-> CovGroup:
    group = CovGroup("can commit to bpu")
    group.add_watch_point(dut, {"can_commit_cond2": can_commit_cond2}, name="can_commit_cond2", once = True)
    group.add_watch_point(dut, {"can_commit_cond1": can_commit_cond1}, name="can_commit_cond1", once = True)
    return group

def move_commptr_when_flush(dut):
    commPtr = dut.gen_rob_comm_ptr()
    ifuWbPtr = dut.gen_ifu_wb_ptr()
    commit_state = [i.value for i in dut.commitStateQueue[commPtr.value]]
    firstInstructionFlushed = firstInstructionFlushed_ref(commit_state)
    may_have_stall_from_bpu = dut.bpu_ftb_update_stall.value != 0
    canMoveCommPtr = (
        commPtr != ifuWbPtr
        and not may_have_stall_from_bpu
        and (
            firstInstructionFlushed
        )
    )
    return canMoveCommPtr

def move_commptr_when_can_commit(dut):
    return dut.canCommit.value == 1

def can_move_commit_ptr(dut)-> CovGroup:
    group = CovGroup("can_move_commit_ptr")
    group.add_watch_point(dut, {"move_commptr_when_can_commit": move_commptr_when_can_commit}, name="move_commptr_when_can_commit")
    group.add_watch_point(dut, {"move_commptr_when_flush": move_commptr_when_flush}, name="move_commptr_when_flush")
    return group

def rob_commit_valid(formBackend: FromBackendBundle):
    return last_valid_rob_commit_ref(formBackend) is not None

def rob_commit_no_valid(formBackend: FromBackendBundle):
    return last_valid_rob_commit_ref(formBackend) is None

def update_rob_commit_ptr(formBackend: FromBackendBundle)->CovGroup:
    group = CovGroup("update_rob_commit_ptr")
    group.add_watch_point(formBackend, 
                          {"rob_commit_valid": rob_commit_valid,
                           "rob_commit_no_valid": rob_commit_no_valid
                           },
                          name="rob_commit_valid")
    # group.add_watch_point(formBackend, {"rob_commit_no_valid": rob_commit_no_valid}, name="rob_commit_no_valid")
    return group


def mmio_last_commit_cond1(dut):
    commPtr = dut.gen_comm_ptr()
    mmioReadValid = 1
    mmioReadPtr = dut.gen_mmio_ftq_ptr()
    mmioLastCommit = (
        mmioReadValid
        and (
            (commPtr > mmioReadPtr)
        )
    )
    return mmioLastCommit

def mmio_last_commit_cond2(dut):
    commPtr = dut.gen_comm_ptr()
    mmioReadValid = 1
    mmioReadPtr = dut.gen_mmio_ftq_ptr()
    lastInstructionStatus = lastInstructionStatus_ref(dut, validInstructions_ref(dut))
    has_valid = any(validInstructions_ref(dut))
    mmioLastCommit = (
        mmioReadValid
        and (
            commPtr == mmioReadPtr
            and has_valid
            and lastInstructionStatus == c_committed
        )
    )
    return mmioLastCommit   

def mmio_last_commit(dut)->CovGroup:
    group = CovGroup("mmio_last_commit")
    group.add_watch_point(dut, {"mmio_last_commit_cond1": mmio_last_commit_cond1}, name="mmio_last_commit_cond1")
    group.add_watch_point(dut, {"mmio_last_commit_cond2": mmio_last_commit_cond2}, name="mmio_last_commit_cond2")
    return group

def ftb_entry_gen_modify_old(dut)->CovGroup:
    group = CovGroup("modify old ftb entry to commit")
    group.add_watch_point(dut.ftb_entry_gen_io_is_br_full.value, {
        "ftb_entry_gen_io_is_br_full": fc.Eq(1),
        }, name="ftb_entry_gen_io_is_br_full")
    group.add_watch_point(dut.ftb_entry_gen_io_is_jalr_target_modified.value, {
        "ftb_entry_gen_io_is_jalr_target_modified": fc.Eq(1),
        }, name="ftb_entry_gen_io_is_jalr_target_modified")
    group.add_watch_point(dut.ftb_entry_gen_io_is_new_br.value, {
        "ftb_entry_gen_io_is_new_br": fc.Eq(1),
        }, name="ftb_entry_gen_io_is_new_br")
    group.add_watch_point(dut.ftb_entry_gen_io_is_strong_bias_modified.value, {
        "ftb_entry_gen_io_is_strong_bias_modified": fc.Eq(1),
        }, name="ftb_entry_gen_io_is_strong_bias_modified")
    return group

def update_ftb_entry(dut)->CovGroup:
    group = CovGroup("update ftb entry and commit it to BPU")
    group.add_watch_point(dut.io_toBpu_update_bits_old_entry.value, {
        "io_toBpu_update_bits_old_entry": fc.Eq(1),
        }, name="io_toBpu_update_bits_old_entry")
    group.add_watch_point(dut.io_toBpu_update_bits_old_entry.value, {
        "io_toBpu_update_bits_init_entry": fc.Eq(0),
        }, name="io_toBpu_update_bits_init_entry")
    return group