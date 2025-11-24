# Utils for ftqPtr
FTQSIZE = 64

def distance_between(enq_flag: bool, enq_value: int,
                    deq_flag: bool, deq_value: int,
                    entries=FTQSIZE) -> int:
    if enq_flag == deq_flag:
        return enq_value - deq_value
    else:
        return entries + enq_value - deq_value
            
def distance_between_bpu_and_commit(self):
    return self._distance_between(enq_flag = self.bpu_ptr_flag.value, enq_value = self.bpu_ptr.value, deq_flag = self.comm_ptr_flag.value, deq_value = self.comm_ptr.value)

def is_After(left, right) -> bool:
    different_flag = left.flag != right.flag
    value_compare = left.value > right.value
    return different_flag != value_compare  # XOR

def is_Before(left, right) -> bool:
    different_flag = left.flag != right.flag
    value_compare = left.value < right.value
    return different_flag != value_compare
