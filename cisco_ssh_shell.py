import paramiko
import time

class CiscoSwitch:
    def __init__(self, hostname, username, password, port=22):
        """
        Initialize the CiscoSwitch object with connection details.
        
        :param hostname: IP address or hostname of the Cisco switch.
        :param username: Username for authentication.
        :param password: Password for authentication.
        :param port: SSH port (default is 22).
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.ssh_client = None
        self.shell = None

    def connect(self):
        """
        Connect to the Cisco switch using SSH.
        """
        try:
            # Create an SSH client
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect to the switch
            self.ssh_client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                look_for_keys=False,
                allow_agent=False
            )
            
            # Open an interactive shell
            self.shell = self.ssh_client.invoke_shell()
            time.sleep(1)  # Wait for the shell to initialize
            
            print(f"Connected to {self.hostname}")
        except Exception as e:
            print(f"Failed to connect to {self.hostname}: {e}")

    def send_command(self, command, timeout=2):
        """
        Send a command to the Cisco switch and return the output.
        
        :param command: The command to execute on the switch.
        :param timeout: Time to wait for the response (default is 2 seconds).
        :return: Output of the command.
        """
        try:
            if not self.shell:
                raise Exception("Not connected to the switch. Call connect() first.")
            
            # Send the command
            self.shell.send(command + "\n")
            time.sleep(timeout)  # Wait for the command to execute
            
            # Read the output
            output = ""
            while self.shell.recv_ready():
                output += self.shell.recv(65535).decode('utf-8')
            
            return output.strip()
        except Exception as e:
            print(f"Error sending command '{command}': {e}")
            return None

    def show_running_config(self):
        """
        Retrieve the running configuration of the switch.
        
        :return: Running configuration as a string.
        """
        return self.send_command("show running-config", timeout=5)

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
            if self.ssh_client:
                self.ssh_client.close()
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
