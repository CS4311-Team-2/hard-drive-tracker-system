

#TODO: Need to implement this in all functions
def is_in_groups(request, *groups):
    if request.user.is_staff:
        return True

    for group in groups:
        if request.user.groups.filter(name=group).exists(): 
            return True
    return False