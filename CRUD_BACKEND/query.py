
from typing import List
import  graphene
from datetime import date, timedelta, datetime
from graphql_jwt.decorators import login_required
from CRUD_BACKEND.models import task, project, enrollment, role
from graphql_relay import from_global_id
from CRUD_BACKEND.mutations import project_type, enrollment_type, role_type, task_type



class Query(graphene.ObjectType):

    all_projects= graphene.List(project_type)
    one_project = graphene.Field(project_type, project_id = graphene.ID())

    # @login_required
    def resolve_all_projects(self, info, **kwargs):
        return project.objects.all()

    # @login_required
    def resolve_one_project (self, info, project_id):
        return project.objects.get(pk=project_id)



    all_tasks_for_a_project = graphene.List(task_type, project_id=graphene.ID(required=True))

    # @login_required
    def resolve_all_tasks_for_a_project(self, info, project_id):
            return task.objects.filter(project_id=project_id)



    all_enrollments= graphene.List(enrollment_type)

    # @login_required
    def resolve_all_enrollments(self, info):
        return enrollment.objects.all()


    all_tasks_for_a_user_per_week_per_project = graphene.List(
        task_type, project_id=graphene.ID(required=True), user_id=graphene.ID(required=True))


    def resolve_all_tasks_for_a_user_per_week_per_project(self, info, project_id, user_id,  **kwargs):

        queryset = task.objects.filter(project_id=project_id).filter(user_id=user_id)
        last_seven_days = date.today() - timedelta(days=7)
        last_seven_days = datetime( last_seven_days.year, last_seven_days.month, last_seven_days.day)
        last_seven_days_unix_time = datetime.timestamp(last_seven_days)

        current_unix_time= datetime.timestamp(datetime.now())
        List =[]

        for tuple in queryset:
            datetime_from_date = datetime( tuple.task_start_date.year, tuple.task_start_date.month, tuple.task_start_date.day)
            start_date_unix_time = datetime.timestamp(datetime_from_date)
            if start_date_unix_time <= current_unix_time and start_date_unix_time >= last_seven_days_unix_time:
                List.append(tuple)
        return List


    all_task_for_aperson_for_a_specific_project = graphene.List(
        task_type, project_id=graphene.ID(required=True), user_id=graphene.ID(required=True))

    def resolve_all_task_for_User_for_specific_project(self, info, project_id,user_id, **kwargs):
        return task.objects.filter(project_id=project_id).filter(user_id=user_id)




    all_roles = graphene.List(role_type)

    def resolve_all_roles(self, info, **kwargs):
        return role.objects.all()






    all_completed_projects = graphene.List(project_type)
    on_hold_projects = graphene.List(project_type)
    all_delayed_projects = graphene.List(project_type)




    def resolve_all_completed_projects(self, info):
        status = "Completed"
        return project.objects.filter(task_status=status)


    def resolve_on_hold_projects(self, info, user_id):
        status = "On Hold"
        return project.objects.filter(staff_id=user_id).filter(task_status=status)


    def resolve_all_delayed_projects(self, info):
        current_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for tuple in queryset:
                datetime_from_date = datetime( tuple.project_end_date.year, tuple.project_end_date.month, tuple.project_end_date.day)
                if datetime.timestamp(datetime_from_date) > current_time:
                    List.append(tuple)
        return List





    create_report = graphene.List(task_type, report_start_date = graphene.Date(required = True),report_end_date = graphene.Date(required=True))
    def resolve_create_report(self, info,report_start_date, report_end_date ):

        all_tasks = task.objects.all()

        report_start_date_unix_time  = datetime.timestamp(datetime(report_start_date.year, report_start_date.month, report_start_date.day))
        report_end_date_unix_time = datetime.timestamp(datetime(report_end_date.year, report_end_date.month, report_end_date.day))

        List=[]
        for tuple in all_tasks:
            task_start_date_unix_time = datetime.timestamp(datetime( tuple.task_start_date.year, tuple.task_start_date.month, tuple.task_start_date.day))
            task_end_date_unix_time  = datetime.timestamp(datetime( tuple.task_completion_date.year, tuple.task_completion_date.month, tuple.task_completion_date.day))

            if task_start_date_unix_time >= report_start_date_unix_time and task_end_date_unix_time <= report_end_date_unix_time:
                List.append(tuple)
        return List




    all_projects_of_a_particular_user = graphene.List(project_type, user_id=graphene.ID(required=True))


    def resolve_all_projects_of_a_particular_user(self, info,user_id):
        # id = from_global_id(user_id)[1]
        List =[]
        all_projects = project.objects.filter()
        for tuple in all_projects:
            if user_id in tuple.project_members.all():
                List.append (tuple)
        return List



