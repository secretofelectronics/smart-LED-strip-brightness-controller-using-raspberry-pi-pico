from machine import Pin, PWM, UART
import time

# Set up PWM pin for LED brightness control
led_pin = PWM(Pin(2))  # GPIO pin 15 for LED
led_pin.freq(1000)      # PWM frequency set to 1 kHz

# Initialize UART for communication with HC-05
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def set_led_brightness(duty):
    """ Set the brightness of the LED based on the duty cycle. """
    # Duty cycle should be between 0 and 65535 (16-bit resolution for PWM)
    led_pin.duty_u16(duty)

while True:
    if uart.any():
        # Read the data received from the smartphone
        data = uart.read().decode().strip()

        # Assuming the data is a number between 0 to 100 to control brightness
        if data.isdigit():
            brightness = int(data)

            # Make sure brightness is within 0-100
            if 0 <= brightness <= 100:
                # Convert brightness range (0-100) to PWM duty cycle (0-65535)
                duty_cycle = int(brightness * 65535 / 100)
                set_led_brightness(duty_cycle)

                print(f"Received brightness value: {brightness}, Duty cycle: {duty_cycle}")
            else:
                print("Error: Value out of range! Please send a value between 0 and 100.")

        # Add a small delay to avoid overloading the UART
        time.sleep(0.1)