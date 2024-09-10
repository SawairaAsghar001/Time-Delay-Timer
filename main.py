import serial
import time

def connect_to_arduino(port='COM3', baudrate=9600):
    """
    Establishes a serial connection to the Arduino.
    
    :param port: The serial port to which the Arduino is connected (e.g., 'COM3' on Windows or '/dev/ttyACM0' on Linux/Mac).
    :param baudrate: The baud rate for the serial communication (must match the Arduino code).
    :return: The serial connection object.
    """
    try:
        arduino = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to Arduino on {port} at {baudrate} baud rate.")
        time.sleep(2)  # Wait for Arduino to reset
        return arduino
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        return None

def send_command_to_arduino(arduino, command):
    """
    Sends a single-character command to the Arduino.
    
    :param arduino: The serial connection object.
    :param command: The command character ('H' to turn on, 'L' to turn off).
    """
    if arduino and arduino.is_open:
        arduino.write(command.encode())  # Send the command as bytes
        print(f"Sent command '{command}' to Arduino.")
    else:
        print("Arduino is not connected or serial port is not open.")

def countdown_timer(seconds, arduino):
    """
    Countdown timer function that controls an LED or relay on the Arduino.
    
    :param seconds: The total time in seconds for the countdown.
    :param arduino: The serial connection object.
    """
    print(f"Timer set for {seconds} seconds.")
    send_command_to_arduino(arduino, 'H')  # Turn ON the LED or relay

    while seconds > 0:
        mins, secs = divmod(seconds, 60)  # Convert seconds to minutes and seconds
        time_format = f"{mins:02d}:{secs:02d}"
        print(f"Time remaining: {time_format}")
        
        time.sleep(1)  # Pause the program for 1 second
        seconds -= 1

    send_command_to_arduino(arduino, 'L')  # Turn OFF the LED or relay
    print("Time's up! Device is turned off.")

# Example usage
if __name__ == "__main__":
    arduino = connect_to_arduino(port='COM3')  # Replace 'COM3' with your actual port
    if arduino:
        try:
            countdown_timer(10, arduino)  # Set timer for 10 seconds
        finally:
            arduino.close()  # Close the serial connection
            print("Serial connection closed.")