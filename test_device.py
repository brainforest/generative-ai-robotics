import smbus2
import time

# Define I2C bus and device address
I2C_BUS = 1
DEVICE_ADDRESS = 0x3C  # Replace with your device's I2C address

# Create I2C bus object
bus = smbus2.SMBus(I2C_BUS)

def send_command(command, data):
    try:
        bus.write_byte_data(DEVICE_ADDRESS, command, data)
    except OSError as e:
        print(f"Error: {e}")

def setup():
    # Initialize the AIP1640 chip
    send_command(0x00, 0x00)  # Example initialization command
    time.sleep(0.1)  # Short delay to ensure initialization

def display_smiling_face():
    # Define a smiling face pattern (example pattern)
    smiling_face = [
        0x00, 0x3C, 0x42, 0x42, 0x42, 0x3C, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]

    for i, value in enumerate(smiling_face):
        send_command(0x00, i)  # Set the column address (example)
        send_command(0x40, value)  # Send the pattern data

def main():
    setup()
    while True:
        display_smiling_face()
        time.sleep(2)  # Display for 2 seconds

if __name__ == "__main__":
    main()

