
import  graphene
from datetime import date, timedelta, datetime
from graphql_jwt.decorators import login_required
from CRUD_BACKEND.models import task, project, status, enrollment, role, project_categories
from graphql_relay import from_global_id
from CRUD_BACKEND.mutations import project_type, status_type, enrollment_type, category_type, role_type, task_type



class Query(graphene.ObjectType):

    all_projects= graphene.List(project_type)
    one_project = graphene.Field(project_type, project_id = graphene.ID())

    # @login_required
    def resolve_all_projects(self, info, **kwargs):
        return project.objects.all()


    all_categories= graphene.List(category_type)
    one_category = graphene.Field(category_type, category_id = graphene.ID())

    # @login_required
    def resolve_all_categories(self, info, **kwargs):
        return project_categories.objects.all()



    all_status= graphene.List(status_type)
    one_status = graphene.Field(status_type, status_id = graphene.ID())

    # @login_required
    def resolve_all_status(self, info, **kwargs):
        return status.objects.all()


    # @login_required
    def resolve_one_status(self, info, status_id):
        return status.objects.get(pk=status_id)


    all_tasks= graphene.List(task_type)

    # @login_required
    def resolve_all_tasks(self, info, **kwargs):
        return task.objects.all()




    all_tasks_for_a_project_per_user = graphene.List(task_type, project_id=graphene.ID(required=True), username=graphene.String(required=True))

    # @login_required
    def resolve_all_tasks_for_a_project_per_user(self, info, project_id, username):
        all_tasks_for_the_project = task.objects.filter(project_id=project_id)
        List = []
        for tuple in all_tasks_for_the_project:
            if tuple.user_id.username == username:
                List.append(tuple)
        return List



    all_enrollments= graphene.List(enrollment_type)

    # @login_required
    def resolve_all_enrollments(self, info):
        return enrollment.objects.all()


    all_tasks_for_a_user_per_week_per_project = graphene.List(
        task_type, project_id=graphene.ID(required=True), username=graphene.ID(required=True))


    def resolve_all_tasks_for_a_user_per_week_per_project(self, info, project_id, username,  **kwargs):

        queryset = task.objects.filter(project_id=project_id)
        current_unix_time= datetime.timestamp(datetime.now())
        List =[]

        for tuple in queryset:
            if tuple.user_id.username == username:
                datetime_from_date = datetime( tuple.task_start_date.year, tuple.task_start_date.month, tuple.task_start_date.day)
                start_date_unix_time = datetime.timestamp(datetime_from_date)
                if  current_unix_time - start_date_unix_time >=0 and current_unix_time - start_date_unix_time <= 7*86400:
                        List.append(tuple)
        return List





    all_roles = graphene.List(role_type)
    # @login_required
    def resolve_all_roles(self, info, **kwargs):
        return role.objects.all()






    all_completed_projects = graphene.List(project_type)
    count_all_completed_projects_per_user = graphene.Int(username = graphene.String(required = True))
    on_hold_projects = graphene.List(project_type)
    all_delayed_projects = graphene.List(project_type)
    count_all_completed_projects = graphene.Int()
    count_all_delayed_projects = graphene.Int()
    count_all_on_hold_projects = graphene.Int()
    count_all_on_hold_projects_per_user = graphene.Int(username = graphene.String(required = True))
    all_completed_projects_per_user= graphene.List(project_type, username = graphene.String(required = True))
    all_on_hold_projects_per_user= graphene.List(project_type, username = graphene.String(required = True))
    all_on_hold_projects = graphene.List(project_type)
    all_on_progress_projects = graphene.List(project_type)
    count_all_on_progress_projects = graphene.Int()
    count_all_on_progress_projects_per_user = graphene.Int(username = graphene.String(required = True))
    all_on_progress_projects_per_user =  graphene.List(project_type, username = graphene.String(required = True))
    all_delayed_projects_per_user = graphene.List(project_type, username = graphene.String(required = True))
    count_all_delayed_projects_per_user =  graphene.Int(username = graphene.String(required = True))





    # @login_required
    # @staff_member_required
    def resolve_all_on_hold_projects(self, info):
        status = "OnHold"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                List.append(one_project)
        return List


    # @login_required
    # @staff_member_required
    def resolve_count_all_on_hold_projects(self, info):
        status = "OnHold"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                List.append(one_project)
        return len(List)







    # @login_required
    def resolve_all_on_hold_projects_per_user(self, info, username):
        status = "OnHold"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                userObjects = one_project.project_members.all()
                for one_user in userObjects:
                    if username == one_user.username:
                        List.append(one_project)
        return List

    # @login_required
    def resolve_count_all_on_hold_projects_per_user(self, info, username):
        status = "Completed"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                userObjects = one_project.project_members.all()
                for one_user in userObjects:
                    if username == one_user.username:
                        List.append(one_project)
        return len(List)





    # @login_required
    # @staff_member_required
    def resolve_all_completed_projects(self, info):
        status = "Completed"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                List.append(one_project)
        return List

    # @login_required
    # @staff_member_required
    def resolve_count_all_completed_projects(self, info):
        status = "Completed"
        return project.objects.filter(project_status=status).count()






    # @login_required
    def resolve_all_completed_projects_per_user(self, info, username):
        status = "Completed"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                userObjects = one_project.project_members.all()
                for one_user in userObjects:
                    if username == one_user.username:
                        List.append(one_project)
        return List

    # @login_required
    def resolve_count_all_completed_projects_per_user(self, info, username):
        status = "Completed"
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            if one_project.project_status == status:
                userObjects = one_project.project_members.all()
                for one_user in userObjects:
                    if username == one_user.username:
                        List.append(one_project)
        return len(List)




    # @login_required
    # @staff_member_required
    def resolve_all_delayed_projects(self, info):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
                if current_unix_time > datetime.timestamp(datetime_from_date):
                    List.append(one_project)
        return List

    # @login_required
    # @staff_member_required
    def resolve_count_all_delayed_projects(self, info):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
                if current_unix_time > datetime.timestamp(datetime_from_date):
                    List.append(one_project)
        return len(List)


    # @login_required
    def resolve_all_delayed_projects_per_user(self, info, username):
        current_unix_time= datetime.timestamp(datetime.now())
        all_projects= project.objects.all()
        List = []
        for one_project in all_projects:
            datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
            if current_unix_time > datetime.timestamp(datetime_from_date):
                    userObjects = one_project.project_members.all()
                    for one_user in userObjects:
                        if username == one_user.username:
                            List.append(one_project)
        return List

    # @login_required
    def resolve_count_all_delayed_projects_per_user(self, info, username):
        current_unix_time= datetime.timestamp(datetime.now())
        all_projects= project.objects.all()
        List = []
        for one_project in all_projects:
            datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
            if current_unix_time > datetime.timestamp(datetime_from_date):
                    userObjects = one_project.project_members.all()
                    for one_user in userObjects:
                        if username == one_user.username:
                            List.append(one_project)
        return len(List)






    # @login_required
    # @staff_member_required
    def resolve_all_on_progress_projects(self, info):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
                if current_unix_time <= datetime.timestamp(datetime_from_date):
                    List.append(one_project)
        return List

    # @login_required
    # @staff_member_required
    def resolve_count_all_on_progress_projects(self, info):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
                if current_unix_time <= datetime.timestamp(datetime_from_date):
                    List.append(one_project)
        return len(List)






    # @login_required
    def resolve_all_on_progress_projects_per_user(self, info, username):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
            datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
            if current_unix_time <= datetime.timestamp(datetime_from_date):
                userObjects = one_project.project_members.all()
                for one_user in userObjects:
                    if username == one_user.username:
                        List.append(one_project)
        return List

    # @login_required
    def resolve_count_all_on_progress_projects_per_user(self, info, username):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
            datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
            if current_unix_time <= datetime.timestamp(datetime_from_date):
                userObjects = one_project.project_members.all()
                for one_user in userObjects:
                    if username == one_user.username:
                        List.append(one_project)
        if len(List)!=None:
            return len(List)
        else:
            return 0







    get_any_week_tasks = graphene.List(task_type,  start_date = graphene.Date(required = True), end_date = graphene.Date(required=True), project_id = graphene.ID(required = True))

    # @login_required
    def resolve_get_any_week_tasks(self, info, start_date, end_date , project_id ):

        all_tasks = task.objects.filter(project_id = project_id)

        start_date_unix_time  = datetime.timestamp(datetime(start_date.year, start_date.month, start_date.day))
        end_date_unix_time = datetime.timestamp(datetime(end_date.year, end_date.month, end_date.day))

        List=[]
        for tuple in all_tasks:
            task_start_date_unix_time = datetime.timestamp(datetime( tuple.task_start_date.year, tuple.task_start_date.month, tuple.task_start_date.day))
            task_end_date_unix_time  = datetime.timestamp(datetime( tuple.task_completion_date.year, tuple.task_completion_date.month, tuple.task_completion_date.day))

            if task_start_date_unix_time >= start_date_unix_time and task_end_date_unix_time <= end_date_unix_time:
                List.append(tuple)
        return List




    all_projects_of_a_particular_user = graphene.List(project_type, username=graphene.ID(required=True))

    # @login_required
    def resolve_all_projects_of_a_particular_user(self, info,username):
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            userObjects = one_project.project_members.all()
            for one_user in userObjects:
                if username == one_user.username:
                    List.append(one_project)

        return List

    all_projects_per_user_and_tasks_for_the_past_week = graphene.List(project_type, username=graphene.String(required=True))
    def resolve_all_projects_per_user_and_tasks_for_the_past_week(self, info, username):

        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                all_members = one_project.project_members.all()
                for one_member in all_members:
                    if one_member.username == username:
                        all_tasks = one_project.taskSet.all()
                        for one_task in all_tasks:
                            datetime_from_date = datetime( one_task.task_start_date.year, one_task.task_start_date.month, one_task.task_start_date.day)
                            start_date_unix_time = datetime.timestamp(datetime_from_date)
                            if  current_unix_time - start_date_unix_time >=0 and current_unix_time - start_date_unix_time <= 7*86400:
                                List.append(one_project)

        return List



    count_total_projects = graphene.Int()

    def resolve_count_total_projects(self, info):
        return len(project.objects.all())



    count_total_projects_per_user= graphene.Int(username = graphene.String(required = True))

    def resolve_count_total_projects_per_user(self,cls, info, username):
        all_projects = project.objects.all()
        List =[]
        for one_project in all_projects:
            users = one_project.project_members.all()
            for one_user in users:
                if one_user.username == username:
                    List.append(one_project)
        return len(List)