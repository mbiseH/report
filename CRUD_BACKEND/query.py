
import  graphene
from datetime import date, timedelta, datetime
from CRUD_BACKEND.models import tasks, project, enrollment
from CRUD_BACKEND.mutations import project_type, enrollment_type, task_type



class Query(graphene.ObjectType):

    all_projects= graphene.List(project_type)
    one_project = graphene.Field(project_type, project_id = graphene.ID())

    # @login_required
    def resolve_all_projects(self, info, **kwargs):
        return project.objects.all()

    # @login_required
    def resolve_one_project (self, info, project_id):
        return project.objects.get(pk=project_id)



    all_tasks_for_a_project = graphene.List(task_type, project_id=graphene.ID())

    # @login_required
    def resolve_all_tasks_for_a_project(self, info, project_id):
            return tasks.objects.filter(project_id=project_id)



    all_enrollments= graphene.List(enrollment_type)

    # @login_required
    def resolve_all_enrollments(self, info):
        return enrollment.objects.all()


    all_tasks_for_a_user_per_week_per_project = graphene.List(
        task_type, project_id=graphene.ID(required=True), user_id=graphene.ID(required=True), task_start_date=graphene.ID(required=True))


    def resolve_all_tasks_for_a_user_per_week_per_project(self, info, project_id, user_id, task_start_date, **kwargs):

        task_start_date = datetime.strptime(task_start_date, '%Y-%m-%d').date()
        task_start_date + timedelta(days=7)

        queryset = tasks.objects.filter(project_id=project_id).filter(user_id=user_id)
        for tuple in queryset:
            if tuple.task_start_date <=  date.today():
                pass
            else:
                tuple.delete()
        return queryset


    all_tasks_for_aperson_for_a_specific_project = graphene.List(
        task_type, project_id=graphene.ID(required=True), user_id=graphene.ID(required=True))

    def resolve_all_tasks_for_User_for_specific_project(self, info, project_id,user_id, **kwargs):
        return tasks.objects.filter(project_id=project_id).filter(user_id=user_id)

