import subprocess
import can

PCAN_SOURCE = 0x10
UHDRTX_DEST = 0x26


# Read-only
ID                  = 0x0001
Serial              = 0x0002
SW_Version          = 0x0003
FW_Version          = 0x0004
HW_Version          = 0x0005
Uptime              = 0x0006

I2C_Status          = 0x0010
CAN0_Status         = 0x0012
CAN1_Status         = 0x0014

LVDS_Status         = 0x0024

Status              = 0x0030
RF_Status           = 0x0031
Temperature0        = 0x0032
Temperature1        = 0x0033
Temperature_Error   = 0x003D
Current_Err         = 0x003E
Voltage_Err         = 0x003F

Currents0           = 0x0040
Currents1           = 0x0041
Currents2           = 0x0042
Currents3           = 0x0043
Currents4           = 0x0044
Currents5           = 0x0045

Voltages0           = 0x0050
Voltages1           = 0x0051
Voltages2           = 0x0052
Voltages3           = 0x0053
Voltages4           = 0x0054
Voltages5           = 0x0055

ChannelMode         = 0x0061

PA0_Status0         = 0x0190
PA1_Status0         = 0x01A0
PA0_Status1         = 0x0191
PA1_Status1         = 0x01A1

LVDS_Rx_Count       = 0x01B1
LVDS_Rx_ParityErrors= 0x01B2

# Read/Write
Scratchpad          = 0x0007

I2C_Conf            = 0x0011
CAN0_Conf           = 0x0013
CAN1_Conf           = 0x0015

LVDS_Conf           = 0x0025
CommsUnlock         = 0x002F

Mode                = 0x0060
All_Encoding        = 0x0062
DataSource          = 0x0063
SymbolRate          = 0x0064
All_PA_Conf         = 0x0065
ImageControl        = 0x0066
PowerControl        = 0x0067

Tlim0               = 0x0070
Tlim1               = 0x0071
Tlim2               = 0x0072
TlimBoard           = 0x0073
TlimFPGA            = 0x0074
PA_Timeout          = 0x0075

CHx_Freq            = 0x0130  # múltiplos endereços
CHx_Enc             = 0x0131  # múltiplos endereços

PAx_Conf0           = 0x0190  # múltiplos endereços
PAx_Conf1           = 0x0191  # múltiplos endereços
PAx_Gate            = 0x0190  # múltiplos endereços
PAx_DAC             = 0x0191  # múltiplos endereços
PAx_Lim             = 0x0191  # múltiplos endereços

LVDS_Transceiver_Active = 0x01B0
LVDS_Data_Delay         = 0x01B4  # múltiplos endereços

def build_arbitration_id(message_type, source, dest):
    arb_id = ((message_type & 0x1F) << 24) | \
             ((0x00 & 0xFF) << 16)         | \
             ((source & 0xFF) << 8)        | \
             (dest & 0xFF)
    return arb_id

class UHDRPCAN:
    def __init__(self, channel='can0', bitrate=500000):
        self.channel = channel
        # self._setup_can_interface(bitrate)
        self.bus = can.interface.Bus(channel=self.channel, bustype='socketcan')

    def _setup_can_interface(self, bitrate):
        cmds = [
            f"sudo ip link set {self.channel} down",
            f"sudo ip link set {self.channel} type can bitrate {bitrate}",
            f"sudo ip link set {self.channel} up"
        ]
        for cmd in cmds:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def send_msg(self, message_type, data):
        arb_id = build_arbitration_id(message_type, PCAN_SOURCE, UHDRTX_DEST)
        msg = can.Message(arbitration_id=arb_id, data=data, is_extended_id=True)
        self.bus.send(msg)

    def read_msg(self, timeout=1.0):
        msg = self.bus.recv(timeout)
        if msg is not None and msg.is_extended_id:
            return msg.arbitration_id, msg.data
        return None, None

    def write_request(self, reg_addr, data, timeout=1.0):
        """
        reg_addr: int (ex: 0x0001)
        data: list de 4 bytes [d0, d1, d2, d3]
        timeout: float, tempo máximo de espera por resposta
        """
        reg_addr_bytes = [(reg_addr >> 8) & 0xFF, reg_addr & 0xFF]
        payload = reg_addr_bytes + data
        self.send_msg(0x01, payload)  # 0x01 = Write Request

        arb_id, resp_data = self.read_msg(timeout)

        if arb_id is None:
            print("Sem resposta.")
            return False

        message_type = (arb_id >> 24) & 0x1F

        if message_type == 0x02:
            # print(f"Write OK: ID=0x{arb_id:X}, REG=0x{reg_addr:04X}, DATA={[f'0x{x:02X}' for x in data]}")
            return True
        elif message_type == 0x03:
            print(f"Write ERROR: ID=0x{arb_id:X}, REG=0x{reg_addr:04X}, DATA={[f'0x{x:02X}' for x in data]}")
            return False
        else:
            print(f"Resposta inesperada: ID=0x{arb_id:X}, DATA={resp_data}")
            return False


    def read_request(self, reg_addr, timeout=1.0):
        """
        reg_addr: int (ex: 0x0001)
        timeout: float, tempo máximo de espera por resposta
        """
        reg_addr_bytes = [(reg_addr >> 8) & 0xFF, reg_addr & 0xFF]
        self.send_msg(0x04, reg_addr_bytes)  # 0x04 = Read Request
        arb_id, resp_data = self.read_msg(timeout)

        if arb_id is None:
            print("Sem resposta.")
            return None

        message_type = (arb_id >> 24) & 0x1F

        if message_type == 0x05:
            # print(f"Read OK: ID=0x{arb_id:X}, REG=0x{reg_addr:04X}, DATA={[f'0x{x:02X}' for x in resp_data[2:6]]}")
            return list(resp_data[2:6])  # dados D0-D3
        elif message_type == 0x06:
            print(f"Read ERROR: ID=0x{arb_id:X}, REG=0x{reg_addr:04X}, DATA={resp_data}")
            return None
        else:
            print(f"Resposta inesperada: ID=0x{arb_id:X}, DATA={resp_data}")
            return None

    def get_id(self):
        value = self.read_request(ID)
        if not value:
            return False
        ascii_str = ''.join(chr(b) for b in value)
        hex_str = '0x' + ''.join(f'{b:02X}' for b in value)
        print(f"ID: '{ascii_str}' ({hex_str})")
        print("")
        return value

    def get_serial(self):
        value = self.read_request(Serial)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        hex_str = f'0x{int_value:08X}'
        print(f"Serial: {int_value} ({hex_str})")
        print("")
        return int_value

    def get_swversion(self):
        value = self.read_request(SW_Version)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        major = (int_value >> 0) & 0xFF
        minor = (int_value >> 8) & 0xFF
        patch = (int_value >> 16) & 0xFF
        print(f"SW Version: {major:02}.{minor:02}.{patch:02} (0x{int_value:08X})")
        print("")
        return (major, minor, patch)

    def get_hwversion(self):
        value = self.read_request(HW_Version)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        major = (int_value >> 0) & 0xFF
        minor = (int_value >> 8) & 0xFF
        patch = (int_value >> 16) & 0xFF
        print(f"HW Version: {major:02}.{minor:02}.{patch:02} (0x{int_value:08X})")
        print("")
        return (major, minor, patch)

    def get_fwversion(self):
        value = self.read_request(FW_Version)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        major = (int_value >> 0) & 0xFF
        minor = (int_value >> 8) & 0xFF
        patch = (int_value >> 16) & 0xFF
        print(f"FW Version: {major:02}.{minor:02}.{patch:02} (0x{int_value:08X})")
        print("")
        return (major, minor, patch)

    def get_uptime(self):
        value = self.read_request(Uptime)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        print(f"Uptime: {int_value} seconds (0x{int_value:08X})")
        print("")
        return int_value

    def get_scratchpad(self):
        value = self.read_request(Scratchpad)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        print(f"Scratchpad: 0x{int_value:08X}")
        print("")
        return int_value

    def set_scratchpad(self, register_value):
        data = [
            (register_value >> 24) & 0xFF,
            (register_value >> 16) & 0xFF,
            (register_value >> 8) & 0xFF,
            register_value & 0xFF,
        ]
        return self.write_request(Scratchpad, data)

    def get_i2c_status(self):
        print("Not implemented")
        print("")

    def get_i2c_conf(self):
        print("Not implemented")
        print("")

    def set_i2c_conf(self, i2c_address, i2c_speed):
        print("Not implemented")
        print("")

    def get_can0_status(self):
        value = self.read_request(CAN0_Status)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        print(f"CAN0_Status: 0x{int_value:08X}")
        print(f"  Invalid_Address:  {bool(int_value & (1 << 0))}")
        print(f"  Out_Of_Range:     {bool(int_value & (1 << 1))}")
        print(f"  Not_Writeable:    {bool(int_value & (1 << 2))}")
        print(f"  Internal_Err:     {bool(int_value & (1 << 3))}")
        print("")
        return int_value

    def get_can0_conf(self):
        value = self.read_request(CAN0_Conf)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        address = int_value & 0x7F
        print(f"CAN0_Conf: 0x{int_value:08X}")
        print(f"  Address: {address} (0x{address:02X})")
        print("")
        return int_value

    def set_can0_conf(self, can_address):
        register_value = can_address & 0x7F  # ensure only bits 0-6 are set
        data = [0x00, 0x00, 0x00, register_value]
        print(f"Writing CAN0_Conf: Addr={can_address} (0x{can_address:02X}) -> 0x{register_value:08X}")
        print("")
        return self.write_request(CAN0_Conf, data)

    def get_can1_status(self):
        value = self.read_request(CAN1_Status)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        print(f"CAN1_Status: 0x{int_value:08X}")
        print(f"  Invalid_Address:  {bool(int_value & (1 << 0))}")
        print(f"  Out_Of_Range:     {bool(int_value & (1 << 1))}")
        print(f"  Not_Writeable:    {bool(int_value & (1 << 2))}")
        print(f"  Internal_Err:     {bool(int_value & (1 << 3))}")
        print("")
        return int_value

    def get_can1_conf(self):
        value = self.read_request(CAN1_Conf)
        if not value:
            return False
        int_value = int.from_bytes(value, byteorder='big')
        address = int_value & 0x7F
        print(f"CAN1_Conf: 0x{int_value:08X}")
        print(f"  Address: {address} (0x{address:02X})")
        print("")
        return int_value

    def set_can1_conf(self, can_address):
        register_value = can_address & 0x7F  # ensure only bits 0-6 are set
        data = [0x00, 0x00, 0x00, register_value]
        print(f"Writing CAN1_Conf: Addr={can_address} (0x{can_address:02X}) -> 0x{register_value:08X}")
        print("")
        return self.write_request(CAN1_Conf, data)

    def get_lvds_status(self):
        # return self.read_request(LVDS_Status)
        print("Not implemented")
        print("")

    def set_lvds_conf(self, enable, channel, mode, ignore_parity):
        # register_value = ((ignore_parity & 0x01) << 5) | ((mode & 0x03) << 3) | ((channel & 0x03) << 1) | (enable & 0x01)
        # data = [
        #     (register_value >> 24) & 0xFF,
        #     (register_value >> 16) & 0xFF,
        #     (register_value >> 8) & 0xFF,
        #     register_value & 0xFF,
        # ]
        # return self.write_request(LVDS_Conf, data)
        print("Not implemented")
        print("")

    def get_comm_unlock(self):
        val = self.read_request(CommsUnlock)
        if val:
            result = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
            unlocked = (result >> 16) & 0x1
            print(f"CommsUnlock: 0x{result:08X}")
            print(f"  Unlocked: {unlocked}")
            print("")
            return unlocked
        return None


    def set_comm_unlock(self):
        val = 0x000015D3
        data = [
            (val >> 24) & 0xFF,
            (val >> 16) & 0xFF,
            (val >> 8) & 0xFF,
            val & 0xFF,
        ]
        return self.write_request(CommsUnlock, data)

    def set_comm_lock(self):
        return self.write_request(CommsUnlock, [0x00, 0x00, 0x00, 0x00])

    def get_status(self):
        val = self.read_request(Status)
        if val:
            raw = (val[2] << 8) | val[3]
            print(f"Status: 0x{raw:04X}")
            flags = {
                0: "I2C_Status",
                1: "CAN0_Status",
                2: "CAN1_Status",
                8: "RF_Status",
                9: "PA0_Status",
                10: "PA1_Status",
                11: "Cal_Status",
                12: "TempStatus",
                13: "Brd_Curr_Status",
                14: "Brd_Volt_Status",
                15: "Timeout_Status"
            }

            for bit, name in flags.items():
                print(f"  {name} (bit {bit}): {(raw >> bit) & 1}")
            print("")
            return raw
        return None


    def get_rf_status(self):
        val = self.read_request(RF_Status)
        if val:
            raw = (val[2] << 8) | val[3]
            print(f"RF_Status: 0x{raw:04X}")
            flags = {
                0: "RF_Synth_Lock (0 = locked)",
                1: "RFDAC_OverTemp",
                2: "RFDAC_Lock (0 = locked)",
            }
            for bit, name in flags.items():
                status = (raw >> bit) & 1
                print(f"  {name} (bit {bit}): {status}")
            print("")
            return raw
        return None


    def get_temperature0(self):
        val = self.read_request(Temperature0)
        if val:
            board_raw = (val[2] << 8) | val[3]
            rfdac_raw = (val[0] << 8) | val[1]
            board_temp = board_raw * 0.25
            rfdac_temp = rfdac_raw * 0.25
            print(f"Board Temp  : {board_temp:.2f}°C (raw=0x{board_raw:04X})")
            print(f"RFDAC Temp  : {rfdac_temp:.2f}°C (raw=0x{rfdac_raw:04X})")
            print("")
            return board_temp, rfdac_temp
        return None

    def get_temperature1(self):
        val = self.read_request(Temperature1)
        if val:
            fpga_raw = (val[2] << 8) | val[3]
            fpga_temp = fpga_raw * 0.25
            print(f"FPGA Temp   : {fpga_temp:.2f}°C (raw=0x{fpga_raw:04X})")
            print("")
            return fpga_temp
        return None


    def get_temperature_err(self):
        # return self.read_request(Temperature_Error)
        print("Not implemented")
        print("")

    def get_current_err(self):
        # return self.read_request(Current_Err)
        print("Not implemented")
        print("")

    def get_voltage_err(self):
        # return self.read_request(Voltage_Err)
        print("Not implemented")
        print("")
        
    def get_currents(self):
        print("Currents: ")
        sensor_names = [
            "Board_VBAT",      # Currents0 - low
            "FPGA_PWR",        # Currents0 - high
            "PA_0",            # Currents1 - low
            "PA_1",            # Currents1 - high
            "RF_CH0",          # Currents2 - low
            "RF_CH1",          # Currents2 - high
            "Freq_Ref_1V8",    # Currents3 - low
            "Freq_Ref_3V3",    # Currents3 - high
            "RF_Synth_3V3",    # Currents4 - low
            "RF_DAC_1V8",      # Currents4 - high
            "RF_DAC_1V"        # Currents5 - low
        ]

        reg_map = [Currents0, Currents0, Currents1, Currents1, Currents2, Currents2,
                Currents3, Currents3, Currents4, Currents4, Currents5]
        shift = [0, 16] * 6

        for i, name in enumerate(sensor_names):
            val = self.read_request(reg_map[i])
            if val is not None and len(val) == 4:
                data = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
                raw = (data >> shift[i]) & 0xFFFF
                current = raw * 0.001
                print(f"{name}: {current:.3f} mA (raw=0x{raw:04X})")
        
        print("")

    def get_voltages(self):
        print("Voltages:")
        sensor_names = [
            "Reserved",         # Voltages0 - low
            "Reserved",         # Voltages0 - high
            "Reserved",         # Voltages1 - low
            "Reserved",         # Voltages1 - high
            "RF_CH0",           # Voltages2 - low
            "RF_CH1",           # Voltages2 - high
            "Freq_Ref_1V8",     # Voltages3 - low
            "Freq_Ref_3V3",     # Voltages3 - high
            "RF_Synth_3V3",     # Voltages4 - low
            "RF_DAC_1V8",       # Voltages4 - high
            "RF_DAC_1V",        # Voltages5 - low
            "Reserved"          # Voltages5 - high
        ]

        reg_map = [Voltages0, Voltages0, Voltages1, Voltages1, Voltages2, Voltages2,
                Voltages3, Voltages3, Voltages4, Voltages4, Voltages5, Voltages5]
        shift = [0, 16] * 6

        for i, name in enumerate(sensor_names):
            val = self.read_request(reg_map[i])
            if val is not None and len(val) == 4:
                data = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
                raw = (data >> shift[i]) & 0xFFFF
                voltage = raw * 0.001
                print(f"{name}: {voltage:.3f} mV (raw=0x{raw:04X})")

        print("")


    def get_mode(self):
        val = self.read_request(Mode)
        if val is not None and len(val) == 4:
            data = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
            mode = data & 0xFF
            busy = (data >> 8) & 0x1
            error = (data >> 9) & 0x1

            mode_str = {
                0x00: "Standby",
                0x01: "Config",
                0x02: "Transmit"
            }.get(mode, f"Unknown (0x{mode:02X})")

            print(f"Mode: {mode_str}")
            print(f"Busy: {busy}")
            print(f"Error: {error}")
            print("")
            return data
        return None

    def set_mode(self, mode):
        data = [
            (mode >> 24) & 0xFF,
            (mode >> 16) & 0xFF,
            (mode >> 8) & 0xFF,
            mode & 0xFF,
        ]
        return self.write_request(Mode, data)

    def get_channel_mode(self):
        print("Not implemented")
        print("")

    def get_all_encoding(self):
        val = self.read_request(All_Encoding)
        if val is not None and len(val) == 4:
            data = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
            rolloff = (data >> 16) & 0xFF
            pilots = (data >> 8) & 0xFF
            modcod = data & 0xFF

            print(f"Rolloff: {rolloff} (0x{rolloff:02X})")
            print(f"Pilots: {pilots} (0x{pilots:02X})")
            print(f"ModCod: {modcod} (0x{modcod:02X})")
            print("")
            return data
        return None

    def set_all_encoding(self, rolloff, pilots, modcod):
        value = (rolloff << 16) | (pilots << 8) | modcod
        data = [
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF,
        ]
        return self.write_request(All_Encoding, data)

    def get_data_source(self):
        val = self.read_request(DataSource)
        if val:
            source = val[3]
            sources = {
                0: "SERDES 0",
                1: "SERDES 1",
                2: "Custom LVDS receiver",
                3: "Reserved for SpW",
                4: "Test Pattern"
            }
            desc = sources.get(source, "Unknown")
            print(f"Data source: {desc} ({source} / 0x{source:02X})")
            print("")
            return source
        return None
    
    def set_data_source(self, data_source):
        data = [
            (data_source >> 24) & 0xFF,
            (data_source >> 16) & 0xFF,
            (data_source >> 8) & 0xFF,
            data_source & 0xFF,
        ]
        return self.write_request(DataSource, data)

    def get_symbol_rate(self):
        val = self.read_request(SymbolRate)
        if val:
            rate = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
            print(f"Symbol Rate: {rate} ({rate:#010X})")
            print("")
            return rate
        return None

    def set_symbol_rate(self, symbol_rate):
        data = [
            (symbol_rate >> 24) & 0xFF,
            (symbol_rate >> 16) & 0xFF,
            (symbol_rate >> 8) & 0xFF,
            symbol_rate & 0xFF,
        ]
        return self.write_request(SymbolRate, data)

    def get_all_pa_conf(self):
        val = self.read_request(All_PA_Conf)
        if val:
            target_dbm = val[3]
            print(f"Target PA power: {target_dbm} dBm")
            print("")
            return target_dbm
        return None

    def set_all_pa_conf(self, target_dbm):
        if not (27 <= target_dbm <= 33):
            print("Invalid dBm value. Must be between 27 and 33.")
            return None
        data = [0x00, 0x00, 0x00, target_dbm]
        return self.write_request(All_PA_Conf, data)

    def get_image_control(self): 
        # return self.read_request(ImageControl)
        print("Not implemented")
        print("")        
    
    def set_image_control(self, image, rebootCMD):
        # return self.write_request(ImageControl, (rebootCMD << 16) | image)
        print("Not implemented")
        print("")

    def get_power_control(self): 
        return self.read_request(PowerControl)
    
    def set_power_control(self, PD_FPD, PWR_DWN_CMD):
        return self.write_request(PowerControl, (PWR_DWN_CMD << 16) | (PD_FPD & 0x01))

    def get_tlim0(self): 
        # return self.read_request(Tlim0)
        print("Not implemented")
        print("")        
    
    def set_tlim0(self, power, temperature): 
        # return self.write_request(Tlim0, (power << 16) | temperature)
        print("Not implemented")
        print("")        

    def get_tlim1(self): 
        # return self.read_request(Tlim1)
        print("Not implemented")
        print("")        
    
    def set_tlim1(self, power, temperature): 
        # return self.write_request(Tlim1, (power << 16) | temperature)
        print("Not implemented")
        print("")        

    def get_tlim2(self): 
        # return self.read_request(Tlim2)
        print("Not implemented")
        print("")        
    
    def set_tlim2(self, temperature): 
        # return self.write_request(Tlim2, temperature)
        print("Not implemented")
        print("")        

    def get_tlim_board(self): 
        # return self.read_request(TlimBoard)
        print("Not implemented")
        print("")        
    
    def set_tlim_board(self, temperature): 
        # return self.write_request(TlimBoard, temperature)
        print("Not implemented")
        print("")        

    def get_tlim_fpga(self): 
        # return self.read_request(TlimFPGA)
        print("Not implemented")
        print("")
    
    def set_tlim_fpga(self, temperature): 
        # return self.write_request(TlimFPGA, temperature)
        print("Not implemented")
        print("")

    def get_chx_freq(self, channel):
        if channel not in [0, 1, 3, 4]:
            print("Invalid channel. Must be 0, 1, 3, or 4.")
            return None
        addr = CHx_Freq + (channel * 0x10)
        val = self.read_request(addr)
        if val:
            freq = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
            print(f"CH{channel} Frequency: {freq} MHz")
            print("")
            return freq
        return None

    def set_chx_freq(self, channel, freq):
        if channel not in [0, 1, 3, 4]:
            print("Invalid channel. Must be 0, 1, 3, or 4.")
            return None
        addr = CHx_Freq + (channel * 0x10)
        data = [
            (freq >> 24) & 0xFF,
            (freq >> 16) & 0xFF,
            (freq >> 8) & 0xFF,
            freq & 0xFF
        ]
        return self.write_request(addr, data)

    def get_chx_enc(self, channel): 
        # return self.read_request(CHx_Enc + (channel * 0x010))
        print("Not implemented - use all_encoding")
        print("")
    
    def set_chx_enc(self, channel, rolloff, pilots, modcod):
        # return self.write_request(CHx_Enc + (channel * 0x010), (rolloff << 16) | (pilots << 8) | modcod)
        print("Not implemented - use all_encoding")
        print("")

    def get_pax_status0(self, pa):
        if pa not in [0, 1]:
            print("Invalid PA. Must be 0 or 1.")
            return None
        addr = PA0_Status0 + (pa * 0x010)
        val = self.read_request(addr)
        if val is None:
            return None

        raw = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
        
        is_on = bool(raw & (1 << 0))
        overcurrent = bool(raw & (1 << 1))
        overtemp = (raw >> 2) & 0b11
        disconnected = bool(raw & (1 << 4))
        timeout = bool(raw & (1 << 5))
        outpower_raw = (raw >> 8) & 0xFF
        outpower_dbm = outpower_raw * 0.1 + 20
        temp_raw = (raw >> 16) & 0xFFFF
        if temp_raw & 0x8000:
            temp_raw -= 0x10000  # signed 16-bit
        temp_c = temp_raw * 0.25

        print(f"PA{pa} Status:")
        print(f"  IsOn: {is_on}")
        print(f"  OverCurrent: {overcurrent}")
        print(f"  OverTemp Level: {overtemp} (0=OK, 1=Warn, 2=High, 3=Critical)")
        print(f"  Disconnected: {disconnected}")
        print(f"  Timeout: {timeout}")
        print(f"  Output Power: {outpower_dbm:.1f} dBm (raw={outpower_raw})")
        print(f"  Temperature: {temp_c:.2f} °C (raw={temp_raw})")
        print("")

        return {
            "is_on": is_on,
            "overcurrent": overcurrent,
            "overtemp_level": overtemp,
            "disconnected": disconnected,
            "timeout": timeout,
            "output_power_dbm": outpower_dbm,
            "temperature_c": temp_c
        }

    
    def get_pax_status1(self, pa):
        if pa not in [0, 1]:
            print("Invalid PA. Must be 0 or 1.")
            return None
        addr = PA0_Status1 + (pa * 0x10)
        val = self.read_request(addr)
        if val:
            data = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]

            current_raw = data & 0xFFFF
            current_ma = current_raw * 0.1

            quanta = (data >> 16) & 0xFFFF

            print(f"PA{pa} Status1:")
            print(f"  Measured Current: {current_ma:.1f} mA (raw={current_raw})")
            print(f"  Power Quanta: {quanta} (raw=0x{quanta:04X})")
            print("")
            return {
                "Current_mA": current_ma,
                "PowerQuanta": quanta
            }
        return None


    def get_pax_conf0(self, pa): 
        # return self.read_request(PAx_Conf0 + (pa * 0x010))
        print("Not implemented")
        print("")
    
    def set_pax_conf0(self, pa, target_dbm): 
        # return self.write_request(PAx_Conf0 + (pa * 0x010), target_dbm)
        print("Not implemented")
        print("")

    def get_pax_conf1(self, pa): 
        # return self.read_request(PAx_Conf1 + (pa * 0x010))
        print("Not implemented")
        print("")
    
    def set_pax_conf1(self, pa, current_pid, pid_mode):
        # return self.write_request(PAx_Conf1 + (pa * 0x010), (current_pid << 8) | pid_mode)
        print("Not implemented")
        print("")

    def get_pax_gate(self, pa): 
        # return self.read_request(PAx_Gate + (pa * 0x010))
        print("Not implemented")
        print("")
    
    def set_pax_gate(self, pa, setvalue): 
        # return self.write_request(PAx_Gate + (pa * 0x010), setvalue)
        print("Not implemented")
        print("")

    def get_pax_dac(self, pa): 
        # return self.read_request(PAx_DAC + (pa * 0x010))
        print("Not implemented")
        print("")
    
    def set_pax_dac(self, pa, setvalue): 
        # return self.write_request(PAx_DAC + (pa * 0x010), setvalue)
        print("Not implemented")
        print("")

    def get_pax_lim(self, pa): 
        # return self.read_request(PAx_Lim + (pa * 0x010))
        print("Not implemented")
        print("")
    
    def set_pax_lim(self, pa, limit): 
        # return self.write_request(PAx_Lim + (pa * 0x010), limit)
        print("Not implemented")
        print("")
