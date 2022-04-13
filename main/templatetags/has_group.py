from django import template

from users.models import UserProfile

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    print("Has=Group")

    if user.groups.filter(name="Maintainer").exists():
        # Need to manually check by role and mock_group
        if group_name == "Requestor" and user.mock_group_is == UserProfile.MockGroupIs.REQUESTOR:
            return True
        return group_name=="Maintainer" and user.mock_group_is == UserProfile.MockGroupIs.MAINTAINER

    return user.groups.filter(name=group_name).exists()
