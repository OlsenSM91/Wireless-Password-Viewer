import subprocess

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

        password_lines = [line for line in output.splitlines() if "Key Content" in line]
        if not password_lines:
            security_lines = [line for line in output.splitlines() if "Security key" in line]
            if security_lines and "Absent" in security_lines[0]:
                return "Open network - no password"
            return "Password cannot be retrieved - run as administrator"

        password = password_lines[0].split(":")[-1].strip()
        return password if password else "Password hidden or unavailable"
    except subprocess.CalledProcessError as e:
        print(f"\nError retrieving password for {profile_name}: {e}")
        return "Access denied - run as administrator"

def get_all_data():
    """
    Display all stored Wi-Fi passwords in clear text.
    """
    print("\n:: Stored Wi-Fi Passwords ::")
    wifi_profiles = list_wifi_profiles()
    if not wifi_profiles:
        print("\nNo Wi-Fi profiles found.")
        return

    for profile in wifi_profiles:
        password = get_wifi_password(profile)
        print(f"\nWi-Fi Profile: {profile}")
        print(f"Password: {password}")

def main():
    get_all_data()

if __name__ == "__main__":
    main()
