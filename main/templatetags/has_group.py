from django import template

from users.models import UserProfile

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    print("Has=Group")
    if user.groups.filter(name=group_name).exists():
        print("\n\n\nUser is authenticated as Requestor or Maintainer")
        if user.groups.filter(name='Maintainer').exists():
            print("User is authenticated as Maintainer", user.mock_group_is)
            return True
        return True
    return False 
