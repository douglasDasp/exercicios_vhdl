from UHDRPCAN import UHDRPCAN
import time

if __name__ == '__main__':

    uhdrtx = UHDRPCAN(channel='can0')

    uhdrtx.get_id()
    uhdrtx.get_serial()
    uhdrtx.get_swversion()
    uhdrtx.get_fwversion()
    uhdrtx.get_hwversion()
    uhdrtx.get_uptime()
    
    uhdrtx.get_scratchpad()
    uhdrtx.set_scratchpad(0x01020304)
    uhdrtx.get_scratchpad()

    uhdrtx.get_can0_status()
    uhdrtx.get_can0_conf()

    uhdrtx.get_can1_status()
    uhdrtx.get_can1_conf()

    uhdrtx.get_lvds_status()
    # uhdrtx.get_lvds_conf()

    uhdrtx.get_status()
    uhdrtx.get_rf_status()

    uhdrtx.get_temperature0()
    uhdrtx.get_temperature1()
    # uhdrtx.get_temperature_err()

    uhdrtx.get_currents()
    uhdrtx.get_voltages()

    uhdrtx.get_mode()
    # uhdrtx.set_mode(0x01)   # 0x00 standy, 0x01 config, 0x02 transmit
    uhdrtx.get_mode()

    # uhdrtx.get_channel_mode()

    uhdrtx.get_all_encoding()
    # uhdrtx.set_all_encoding(rolloff=0, pilots=0, modcod=0) # Check table 11 and table 12
    uhdrtx.get_all_encoding()

    uhdrtx.get_data_source()
    # uhdrtx.set_data_source(data_source=0x04) # Configuring the Test pattern as data source
    uhdrtx.get_data_source()
    
    uhdrtx.get_symbol_rate()
    # uhdrtx.set_symbol_rate(symbol_rate=200000)
    uhdrtx.get_symbol_rate()

    uhdrtx.get_all_pa_conf()
    # uhdrtx.set_all_pa_conf(target_dbm=27)
    uhdrtx.get_all_pa_conf()

    uhdrtx.get_chx_freq(channel=0)
    uhdrtx.get_chx_freq(channel=1)
    uhdrtx.get_chx_freq(channel=3)
    uhdrtx.get_chx_freq(channel=4)
    # uhdrtx.set_chx_freq(channel=0, freq=515) # in MHz
    # uhdrtx.set_chx_freq(channel=1, freq=515) # in MHz
    # uhdrtx.set_chx_freq(channel=3, freq=515) # in MHz
    # uhdrtx.set_chx_freq(channel=4, freq=515) # in MHz

    uhdrtx.get_pax_status0(pa=0) # power amplifier 0
    uhdrtx.get_pax_status0(pa=1) # power amplifier 1

    uhdrtx.get_pax_status1(pa=0) # power amplifier 0
    uhdrtx.get_pax_status1(pa=1) # power amplifier 1




    


