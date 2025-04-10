
import xml.etree.ElementTree as ET

import pandevice.errors as err
from pandevice import getlogger
from pandevice.base import ENTRY, MEMBER, OpState, PanObject, Root
from pandevice.base import VarPath as Var
from pandevice.base import VersionedPanObject, VersionedParamPath
from pandevice.policies import Rulebase, SecurityRule

fw = ('192.168.29.237', 'admin', 'Admin@123')

logger = getlogger(__name__)

def bulk_update_policies(firewall, policy_updates):
    """
    Updates multiple policies on a Palo Alto firewall.

    Args:
        firewall: The firewall object to interact with.
        policy_updates (list of dict): A list where each dict contains:
            - 'name': Name of the policy to update
            - Other fields: Key-value pairs representing the policy attributes to update
    """
    for update in policy_updates:
        policy_name = update.get('name')
        if not policy_name:
            logger.error("Policy name is missing in update: %s", update)
            continue

        try:
            # Retrieve the policy by name
            policy = firewall.find(policy_name, SecurityRule)
            if not policy:
                logger.warning("Policy '%s' not found. Skipping.", policy_name)
                continue
            
            # Update the policy attributes
            for attr, value in update.items():
                if attr != 'name' and hasattr(policy, attr):
                    setattr(policy, attr, value)

            # Push the updates to the firewall
            policy.apply()
            logger.info("Updated policy '%s' successfully.", policy_name)
        except Exception as e:
            logger.error("Failed to update policy '%s': %s", policy_name, str(e))

# Example usage
policy_updates = [
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

# Assuming `fw` is an authenticated firewall object
bulk_update_policies(fw, policy_updates)
