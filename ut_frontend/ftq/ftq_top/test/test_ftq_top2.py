# import random
# import toffee_test
# import pytest
# from collections import namedtuple
# from ..ref.ftq_ref import FtqAccurateRef, BpuPacket, FtqPointer, get_random_ptr_before_bpu
# from .top_test_fixture import ftq_env
# from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 

# @toffee_test.testcase
# async def test_example_integration(ftq_env):
#     dut = ftq_env.dut
#     ref = FtqAccurateRef()
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_rise()

# ###############################
# ## Test BPU enq requirements ##
# ###############################

# # Recieve BPU packets
# # FUNCTION POINT: BPU_IN_RECEIVE
# @toffee_test.testcase
# async def test_recieve_bpu(ftq_env):
#     dut = ftq_env.dut
#     # ref = FtqAccurateRef()
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_rise()

#     # 可以使用循环，每个cycle随机选择测试一种场景，并覆盖测试点
#     for cycle in range(50):
#         # Set pins values
#         dut.commit_ptr.value = random.randint(0, dut.FTQ_SIZE - 1)
#         dut.bpu_ptr.value = random.randint(0, dut.FTQ_SIZE - 1)
#         dut.can_commit.value = random.choice([True, False])
#         ftq_env.fromBpu.resp_valid.value = random.choice([True, False])

#         validEntries = dut.commit_ptr.value - dut.bpu_ptr.value
#         have_space = (validEntries < dut.FTQ_SIZE)
#         if(dut.can_commit.value and have_space):
#             assert(ftq_env.fromBpu.resp_ready.value == 1)
#             if(ftq_env.fromBpu.resp_valid.value == 1):
#                 # BPU packet is accepted
#                 assert(ftq_env.fromBpu.fire.value == 1)
#                 await ftq_env.ftq_agent.bundle.step(1)
#             else:
#                 # No BPU packet this 
#                 assert(ftq_env.fromBpu.fire.value == 0)
#                 await ftq_env.ftq_agent.bundle.step(1)
#         else:
#             assert(ftq_env.fromBpu.resp_ready.value == 0)
#         await ftq_env.ftq_agent.bundle.step(1)
    
    
# # Enqueue from the BPU packets
# # FUNCTION POINT: BPU_IN_ALLOW
# @toffee_test.testcase
# async def test_bpu_enqueue(ftq_env):
#     dut = ftq_env.dut
#     # ref = FtqAccurateRef()
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_rise()

#     for cycle in range(50):
#         # Set pins values
#         ftq_env.fromBackend.redirect_valid.value = random.choice([True, False])
#         ftq_env.ifu_redirect_valid.value = random.choice([True, False])
#         ftq_env.realAhdValid.value = random.choice([True, False])

#         #### Time cycle 1 ####
#         # Can allow BPU packet in
#         if(ftq_env.fromBackend.redirect_valid.value == 0 or ftq_env.ifu_redirect_valid.value == 0):
            
#             assert(ftq_env.allowBpuIn.value == 1)
#             # await ftq_env.ftq_agent.bundle.step(1)
#         # Can't allow BPU packet in
#         else:
#             assert(ftq_env.allowBpuIn.value == 0)
#             last_cycle_realAhdValid = ftq_env.realAhdValid.value
#             await ftq_env.ftq_agent.bundle.step(1)
            
#             #### Time cycle 2 if needed ####
#             if(last_cycle_realAhdValid == 1 and (ftq_env.fromBackend.redirect_valid.value == 0 or ftq_env.ifu_redirect_valid.value == 0)):
#                 assert(ftq_env.allowBpuIn.value == 1)   
#             else:
#                 assert(ftq_env.allowBpuIn.value == 0)
#         await ftq_env.ftq_agent.bundle.step(1)
        

# # Enqueue from the BPU prediction redirect
# # FUNCTION POINT: BPU_IN_BY_REDIRECT
# @toffee_test.testcase
# async def test_bpu_redirect_enque(ftq_env):
#     dut = ftq_env.dut
#     # ref = FtqAccurateRef()
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_rise()

#     for cycle in range(50):
#         # Set pins values
#         ftq_env.fromBackend.redirect_valid.value = random.choice([True, False])
#         ftq_env.ifu_redirect_valid.value = random.choice([True, False])
#         ftq_env.realAhdValid.value = random.choice([True, False])

       
        
        
        
         

#         #### Time cycle 1 ####
#         # Can allow BPU packet in
#         if(ftq_env.fromBackend.redirect_valid.value == 0 or ftq_env.ifu_redirect_valid.value == 0):
            
#             assert(ftq_env.allowBpuIn.value == 1)
#             # await ftq_env.ftq_agent.bundle.step(1)
#         # Can't allow BPU packet in
#         else:
#             assert(ftq_env.allowBpuIn.value == 0)
#             last_cycle_realAhdValid = ftq_env.realAhdValid.value
#             await ftq_env.ftq_agent.bundle.step(1)
            
#             #### Time cycle 2 if needed ####
#             if(last_cycle_realAhdValid == 1 and (ftq_env.fromBackend.redirect_valid.value == 0 or ftq_env.ifu_redirect_valid.value == 0)):
#                 assert(ftq_env.allowBpuIn.value == 1)   
#             else:
#                 assert(ftq_env.allowBpuIn.value == 0)
#         await ftq_env.ftq_agent.bundle.step(1)



# To test enque action truly write FTQ items into each FTQ subqueue and status queue

# Write into subqueue
# @toffee_test.testcase
# async def test_bpu_redirect_enque(ftq_env):
#     dut = ftq_env.dut
#     ref = FtqAccurateRef()
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_rise()

#     # drive BPU bundle
#     for cycle in range(300):
#         event_type = random.choices(BPU_REDIRECT_EVENT_TYPES, 
#                                  weights=BPU_REDIRECT_EVENT_WEIGHTS)[0]                         
#         s1_valid = s2_valid = s2_hasRedirect = s3_valid = s3_hasRedirect = False
#         if event_type == 'S1':
#             s1_valid = True
#         elif event_type == 'S2_REDIRECT':
#             s2_valid = s2_hasRedirect = True
#         elif event_type == 'S3_REDIRECT':
#             s3_valid = s3_hasRedirect = True
#         s1_packet = BpuPacket(pc=0x8000_0000 | (cycle << 4), fallThruError=(random.random() < 0.05))
#         s2_redirect_ptr = get_random_ptr_before_bpu(ref.bpu_ptr)
#         s2_redirect_idx = s2_redirect_ptr.value
#         s2_redirect_flag = s2_redirect_ptr.flag
#         s2_packet = BpuPacket(pc=0x9000_0000 | (s2_redirect_idx << 4), fallThruError=(random.random() < 0.05))
#         s3_redirect_ptr = get_random_ptr_before_bpu(ref.bpu_ptr)
#         s3_redirect_idx = s3_redirect_ptr.value
#         s3_redirect_flag = s3_redirect_ptr.flag
#         s3_packet = BpuPacket(pc=0xA000_0000 | (s3_redirect_idx << 4), fallThruError=(random.random() < 0.05))
#         to_ifu_ready = random.choice([True, True, False])
#         await ftq_env.ftq_agent.drive_toifu_ready(to_ifu_ready)
#         await ftq_env.ftq_agent.drive_s1_signals(
#             valid=s1_valid,
#             pc=s1_packet.pc,
#             fallThruError=s1_packet.fallThruError
#         )
#         await ftq_env.ftq_agent.drive_s2_signals(
#             valid=s2_valid,
#             hasRedirect=s2_hasRedirect,
#             pc=s2_packet.pc,
#             redirect_idx=s2_redirect_ptr.value,
#             redirect_flag=s2_redirect_ptr.flag,
#             fallThruError=s2_packet.fallThruError
#         )
#         await ftq_env.ftq_agent.drive_s3_signals(
#             valid=s3_valid,
#             hasRedirect=s3_hasRedirect,
#             pc=s3_packet.pc,
#             redirect_idx=s3_redirect_ptr.value,
#             redirect_flag=s3_redirect_ptr.flag,
#             fallThruError=s3_packet.fallThruError
#         )
#         await ftq_env.ftq_agent.bundle.step(1)
#         s3_redirect_fire = s3_valid and s3_hasRedirect
#         s2_redirect_fire = s2_valid and s2_hasRedirect
#         s1_enqueue_fire = s1_valid and await ftq_env.ftq_agent.get_fromBpu_resp_ready()

#         for condition, action, *args in [
#             (s3_redirect_fire, 'redirect', s3_redirect_ptr.value, s3_redirect_ptr.flag, s3_packet),
#             (s2_redirect_fire, 'redirect', s2_redirect_ptr.value, s2_redirect_ptr.flag, s2_packet),
#             (s1_enqueue_fire, 'enqueue', s1_packet)
#         ]:
#             if condition:
#                 if action == 'redirect':
#                     ref.redirect(args[0], args[1], args[2])
#                 elif action == 'enqueue':
#                     ref.enqueue(args[0])
#                 break     


# import random
# import toffee_test
# import pytest
# from collections import namedtuple
# from ..ref.ftq_ref import FtqAccurateRef, BpuPacket, FtqPointer, get_random_ptr_before_bpu
# from .top_test_fixture import ftq_env
# from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 

# @toffee_test.testcase
# async def test_12444(ftq_env):
#     dut = ftq_env.dut
#     ref = FtqAccurateRef()
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_imme()
#     print("test get internal")
#     print(dut.canCommit.value)
#     dut.canCommit.value = 0
#     print(dut.canCommit.value)
#     for i in range(100):
#         dut.canCommit.value = random.choice([True, True, False])
#         print( "canCommit:", dut.canCommit.value)
#         dut.Step()

#     print("notice")