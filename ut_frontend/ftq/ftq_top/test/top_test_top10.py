import random
from this import d
import toffee_test
import pytest
from collections import namedtuple
from ..ref.ftq_ref import FtqAccurateRef, BpuPacket, FtqPointer, get_random_ptr_before_bpu
from .top_test_fixture import ftq_env
from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 

# Test commit requirement

@toffee_test.testcase
async def test_can_commit(ftq_env):
    dut = ftq_env.dut
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_imme()

    for i in range(100):
        dut.comm_ptr_flag.value = random.randint(0, 1)
        dut.comm_ptr.value = random.randint(0, dut.FTQSIZE - 1)
        dut.bpu_ptr_flag.value = random.randint(0, 1)
        dut.bpu_ptr.value = random.randint(0, dut.FTQSIZE - 1)
        dut.io_fromBpu_resp_valid.value = 1
        print( "comm_ptr, flag:", dut.comm_ptr.value, dut.comm_ptr_flag.value)
        print( "bpu_ptr, flag:", dut.bpu_ptr.value, dut.bpu_ptr_flag.value)
        print( "distance between bpu and commit:", dut.distance_between_bpu_and_commit())
        print( "io_fromBpu_resp_valid:", dut.io_fromBpu_resp_valid.value)

        dut.Step()  