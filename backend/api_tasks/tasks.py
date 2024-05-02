from .models import *


def create_user_tasks_profile_for_all():
    """
    Create UserTasksProfile for all users
    """
    from api_base.models import UserProfile
    from api_tasks.models import UserTasksProfile
    for user in UserProfile.objects.all():
        if not hasattr(user, 'tasks_profile'):
            UserTasksProfile.objects.create(user_profile=user)
