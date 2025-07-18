import can
import time

def send_loop(channel='can0'):
    bus = can.interface.Bus(channel=channel, bustype='socketcan')
    print(f"Sending on {channel} every 1 second. Press Ctrl+C to stop.")

    try:
        while True:
            msg = can.Message(
                arbitration_id=0x1ABCDE01,  # exemplo com ID estendido
                data=[0x11, 0x22, 0x33, 0x44],
                is_extended_id=True
            )
            bus.send(msg)
            print(f"Sent: ID={hex(msg.arbitration_id)} Data={msg.data.hex()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == '__main__':
    send_loop()
