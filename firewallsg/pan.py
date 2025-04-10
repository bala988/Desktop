from pandevice.firewall import Firewall
from pandevice.policies import SecurityRule

def update_security_rules(firewall_ip, username, password, rule_updates, default_wildfire="default-wildfire"):
    """
    Update security rules on a Palo Alto Firewall.

    Args:
        firewall_ip (str): IP address of the firewall.
        username (str): Username to authenticate with.
        password (str): Password to authenticate with.
        rule_updates (list of dict): List of rule updates where each dict contains:
            - 'name': Name of the rule to update.
            - Other fields: Fields to update in the rule.
        default_wildfire (str): Default value to set for `wildfire_analysis` if it's None.
    """
    # Initialize firewall connection
    fw = Firewall('192.168.29.237', 'admin', 'Admin@123')

    for update in rule_updates:
        rule_name = update.get('name')
        if not rule_name:
            print("Skipping update as 'name' is missing in rule update.")
            continue

        # Find the rule
        rule = fw.find(rule_name, SecurityRule)
        if not rule:
            print(f"Rule '{rule_name}' not found. Skipping.")
            continue

        # Update the rule attributes
        for key, value in update.items():
            if key != 'name' and hasattr(rule, key):
                setattr(rule, key, value)

        # Check and update `wildfire_analysis` if it is None
        if getattr(rule, 'wildfire_analysis', None) is None:
            rule.wildfire_analysis = default_wildfire
            print(f"Set 'wildfire_analysis' to '{default_wildfire}' for rule '{rule_name}'.")

        try:
            # Push the changes
            rule.apply()
            print(f"Successfully updated rule '{rule_name}'.")
        except Exception as e:
            print(f"Failed to update rule '{rule_name}': {e}")


# Example usage
if __name__ == "__main__":
    firewall_ip = "192.168.29.237"  # Replace with your firewall's IP
    username = "admin"  # Replace with your username
    password = "Admin@123"  # Replace with your password

    # List of rule updates
    rule_updates = [
        {
            'name': 'Allow-HTTP',
            'action': 'allow',
            'description': 'Updated to allow HTTP traffic',
        },
        {
            'name': 'Block-FTP',
            'action': 'deny',
            'description': 'Updated to block FTP traffic',
        },
    ]

    update_security_rules(firewall_ip, username, password, rule_updates)
