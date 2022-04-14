from django.contrib.auth.decorators import user_passes_test

from users.models import UserProfile

#This are helper funtions that add functionality to view function such as
#authenticating the user and check if they are in a specific group

def group_required(*group_names):
    def in_group(user):
        print("in-group")
        if user.is_authenticated:
            print("User is Authenticated [In-Group]: ", group_names)
            print("Mock group is: ", user.mock_group_is)
            if bool(user.groups.filter(name__in = group_names)) | user.is_superuser:
                if user.groups.filter(name='Maintainer').exists() and group_names[0] == "Maintainer":
                    print("Group Decorator Maintainer-Maintainer")
                    return user.mock_group_is == UserProfile.MockGroupIs.MAINTAINER
                return True
            if user.groups.filter(name='Maintainer').exists() and group_names[0] == "Requestor":
                print("Group Decorator Maintainer-Requestor")
                return user.mock_group_is == UserProfile.MockGroupIs.REQUESTOR
        print("----Going Here------")
        return False
    
    return user_passes_test(in_group, login_url='403')