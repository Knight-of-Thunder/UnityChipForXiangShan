class FtqMetaEntry:
    def __init__(self):
        self.meta = None

        self.ftb = {
            "valid": None,
            "isCall": None,
            "isRet": None,
            "isJalr": None,
            "last_may_be_rvi_call": None,
            "carry": None,
            "pftAddr": None,

            "brSlot": {
                "offset": None,
                "sharing": None,
                "valid": None,
                "lower": None,
                "tarStat": None,
            },

            "tailSlot": {
                "offset": None,
                "sharing": None,
                "valid": None,
            }
        }

def unpack_ftq_meta(raw):
    e = FtqMetaEntry()
    b = 0

    def take(w):
        nonlocal b
        v = (raw >> b) & ((1 << w) - 1)
        b += w
        return v

    # 必须要严格按照 Verilog 拼接的【逆序】来解析：
    
    # 1. 硬件最末尾：strong_bias
    e.ftb["strong_bias_0"] = take(1)  # 对应硬件拼接最后一位
    e.ftb["strong_bias_1"] = take(1)
    
    # 2. 倒数第二个：flags
    e.ftb["last_may_be_rvi_call"] = take(1)
    e.ftb["carry"]                = take(1)
    e.ftb["pftAddr"]              = take(4)
    
    # 3. tailSlot 系列 (逆序)
    e.ftb["tailSlot"]["tarStat"]  = take(2)
    e.ftb["tailSlot"]["lower"]    = take(20)
    e.ftb["tailSlot"]["valid"]    = take(1)
    e.ftb["tailSlot"]["sharing"]  = take(1)
    e.ftb["tailSlot"]["offset"]   = take(4)
    
    # 4. brSlot 系列 (逆序)
    e.ftb["brSlot"]["tarStat"]    = take(2)
    e.ftb["brSlot"]["lower"]      = take(12)
    e.ftb["brSlot"]["valid"]      = take(1)
    e.ftb["brSlot"]["sharing"]    = take(1)
    e.ftb["brSlot"]["offset"]     = take(4)
    
    # 5. FTB flags
    e.ftb["valid"]  = take(1)
    e.ftb["isJalr"] = take(1)
    e.ftb["isRet"]  = take(1)
    e.ftb["isCall"] = take(1)
    
    # 6. 硬件最开头（最高位）：meta
    e.meta = take(516)

    assert b == 576, f"Mismatch! Expected 576, got {b}"
    return e



ENTRY_W = 576

def get_entry(ram, idx):
    lo = idx * ENTRY_W
    return (ram >> lo) & ((1 << ENTRY_W) - 1)
