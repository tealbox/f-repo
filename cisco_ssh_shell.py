from netmiko import ConnectHandler
import time

class CiscoSwitch:
    def __init__(self, hostname, username, password, device_type="cisco_ios", port=22):
        """
        Initialize the CiscoSwitch object with connection details.
        
        :param hostname: IP address or hostname of the Cisco switch.
        :param username: Username for authentication.
        :param password: Password for authentication.
        :param device_type: Device type (default is "cisco_ios").
        :param port: SSH port (default is 22).
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.device_type = device_type
        self.port = port
        self.connection = None

    def connect(self):
        """
        Connect to the Cisco switch using Netmiko.
        """
        try:
            # Define the device parameters
            device = {
                "device_type": self.device_type,
                "host": self.hostname,
                "username": self.username,
                "password": self.password,
                "port": self.port,
            }

            # Establish the connection
            self.connection = ConnectHandler(**device)
            print(f"Connected to {self.hostname}")
        except Exception as e:
            print(f"Failed to connect to {self.hostname}: {e}")

    def send_command(self, command):
        """
        Send a command to the Cisco switch and return the output.
        
        :param command: The command to execute on the switch.
        :return: Output of the command.
        """
        try:
            if not self.connection:
                raise Exception("Not connected to the switch. Call connect() first.")
            
            # Send the command and retrieve the output
            output = self.connection.send_command(command)
            return output.strip()
        except Exception as e:
            print(f"Error sending command '{command}': {e}")
            return None

    def show_running_config(self):
        """
        Retrieve the running configuration of the switch.
        
        :return: Running configuration as a string.
        """
        return self.send_command("show running-config")

    def save_config_to_file(self, config, filename="switch_config.cfg"):
        """
        Save the running configuration to a local .cfg file.
        
        :param config: Configuration string to save.
        :param filename: Name of the file to save the configuration.
        """
        try:
            with open(filename, "w") as f:
                f.write(config)
            print(f"Configuration saved to {filename}")
        except Exception as e:
            print(f"Failed to save configuration to {filename}: {e}")

    def disconnect(self):
        """
        Disconnect from the Cisco switch.
        """
        try:
            if self.connection:
                self.connection.disconnect()
            print(f"Disconnected from {self.hostname}")
        except Exception as e:
            print(f"Error disconnecting from {self.hostname}: {e}")


# Example Usage
if __name__ == "__main__":
    # Define switch connection details
    hostname = "192.168.1.1"  # Replace with your switch's IP address
    username = "admin"       # Replace with your username
    password = "password"    # Replace with your password

    # Create an instance of the CiscoSwitch class
    switch = CiscoSwitch(hostname, username, password)

    try:
        # Connect to the switch
        switch.connect()

        # Run a command (e.g., show version)
        output = switch.send_command("show version")
        print("Output of 'show version':")
        print(output)

        # Retrieve the running configuration
        running_config = switch.show_running_config()
        print("\nRunning Configuration:")
        print(running_config)

        # Save the running configuration to a file
        switch.save_config_to_file(running_config, "switch_config.cfg")

    finally:
        # Disconnect from the switch
        switch.disconnect()
