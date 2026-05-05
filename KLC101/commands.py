# command library for KLC101

table = {
    # complete command packets
    "FIXED" : {
        "identify": b"\x23\x02\x00\x00\x50\x01",
        "req_info": b"\x05\x00\x00\x00\x50\x01",
        "req_serial": b"\x15\x00\x00\x00\x50\x01",

        "lock_wheel": b"\x50\x02\x00\x01\x50\x01",
        "unlock_wheel": b"\x50\x02\x00\x02\x50\x01",
        "wheel_status": b"\x51\x02\x00\x00\x50\x01",

        "start_LUT_output": b"\x26\x20\x01\x00\x50\x01",
        "stop_LUT_output": b"\x27\x20\x01\x00\x50\x01",

        "req_ADCinmode": b"\x09\x20\x01\x00\x50\x01",
        "req_trigger_mode": b"\x0c\x20\x01\x00\x50\x01",
        "req_ADCparams": b"\x0e\x20\x01\x00\x50\x01",

        "req_swfreq": b"\x11\x20\x01\x00\x50\x01",
        "req_LUT_params": b"\x24\x20\x01\x00\x50\x01",
        "req_output_status": b"\x29\x20\x01\x00\x50\x01",
        "req_status_update": b"\x41\x20\x01\x00\x50\x01",

        "req_kcube_params": b"\x81\x20\x01\x00\x50\x01",

        "save_params": b"\x86\x20\x01\x00\x50\x01",
        "restore_factory": b"\x86\x06\x01\x00\x50\x01"
        },

    # semi-complete command packets
    "HWCHAN" : {
        "enable": b"\x10\x02\x01\x01\x50\x01",
        "disable": b"\x10\x02\x01\x02\x50\x01",
        "status": b"\x11\x02\x01\x00\x50\x01"
        },

    "CHAN" : {
        "v1": b"\x16\x20\x01\x01\x50\x01",
        "v2": b"\x16\x20\x01\x02\x50\x01",
        "switch": b"\x16\x20\x01\x03\x50\x01",
        "off": b"\x16\x20\x01\x00\x50\x01"
        },

    "STATUS" : {
        "on": b"\x40\x20\x01\x01\x50\x01",
        "off": b"\x40\x20\x01\x00\x50\x01"
        },

    "TRIGGER" : {
        1: b"\x0b\x20\x01\x01\x50\x01",
        2: b"\x0b\x20\x01\x02\x50\x01",
        3: b"\x0b\x20\x01\x03\x50\x01"
        },

    # command headers - need completing before sending
    "HDR" : {
        "set_voltage": b"\x01\x20\x06\x00\xd0\x01",
        "set_frequency": b"\x05\x20\x06\x00\xd0\x01",
        "set_LUT_value": b"\x20\x20\x06\x00\xd0\x01",
    }
}

handles = {

    b"\x02\x00": {"pending disconnect"},
    b"\x03\x20": ("output voltage"),
    b"\x06\x00": ("hardware info"),
    b"\x07\x20": ("output frequency"),
    b"\0a\x20": {"analogue input mode"},
    b"\0d\x20": {"trigger pin mode"},
    b"\0f\x20": {"ADC parameters"},
    b"\x12\x02": ("channel status"),
    b"\x12\x20": ("switching frequency"),
    b"\x16\x00": ("serial number"),
    b"\x18\x20": ("channel mode"),
    b"\x22\x20": ("LUT value"),
    b"\x25\x20": ("LUT parameters"),    
    b"\x30\x20": ("output status"),
    b"\x42\x20": ("status update"),
    b"\x52\x02": ("wheel lock status"),
    b"\x81\x00": ("rich response"),
    b"\x82\x20": ("operating / display settings"),

}