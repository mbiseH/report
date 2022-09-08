
from typing import List
import  graphene
from graphql import GraphQLError
from datetime import date, timedelta, datetime
from graphql_jwt.decorators import login_required
from CRUD_BACKEND.models import task, project, status, enrollment, role, project_categories
from graphql_relay import from_global_id
from django.core.paginator import Paginator
from CRUD_BACKEND.mutations import project_type, status_type, enrollment_type, category_type, role_type, task_type
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist



class Query(graphene.ObjectType):

    count_total_projects = graphene.Int()
    count_all_delayed_projects = graphene.Int()
    count_all_on_progress_projects = graphene.Int()
    one_status = graphene.Field(status_type, status_id = graphene.ID())
    one_project = graphene.Field(project_type, project_id = graphene.ID())
    one_category = graphene.Field(category_type, category_id = graphene.ID())
    count_all_on_hold_projects = graphene.Int(status_id = graphene.ID(required=True))
    count_all_completed_projects = graphene.Int(status_id = graphene.ID(required=True))
    count_total_projects_per_user= graphene.Int(username = graphene.String(required = True))
    count_all_delayed_projects_per_user =  graphene.Int(username = graphene.String(required = True))
    all_tasks= graphene.List(task_type,  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_roles = graphene.List(role_type,  entries_per_page= graphene.Int(),page_number= graphene.Int())
    count_all_on_progress_projects_per_user = graphene.Int(username = graphene.String(required = True))
    all_status= graphene.List(status_type, entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_projects= graphene.List(project_type, entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_categories= graphene.List(category_type, entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_enrollments= graphene.List(enrollment_type,  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_delayed_projects = graphene.List(project_type, entries_per_page= graphene.Int(),page_number= graphene.Int())
    manager_summary_report = graphene.List(task_type,  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_on_progress_projects = graphene.List(project_type,  entries_per_page= graphene.Int(),page_number= graphene.Int())
    count_all_completed_projects_per_user = graphene.Int(status_id = graphene.ID(), username = graphene.String(required = True))
    count_all_on_hold_projects_per_user = graphene.Int(username = graphene.String(required = True), status_id = graphene.ID(required=True))
    all_on_hold_projects = graphene.List(project_type, status_id = graphene.ID(required=True), entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_completed_projects = graphene.List(project_type, status_id = graphene.ID(required=True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_projects_of_a_particular_user = graphene.List(project_type, username=graphene.ID(required=True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_delayed_projects_per_user = graphene.List(project_type, username = graphene.String(required = True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_on_progress_projects_per_user =  graphene.List(project_type, username = graphene.String(required = True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    get_any_week_tasks = graphene.List(task_type,  start_date = graphene.Date(required = True), end_date = graphene.Date(required=True), project_id = graphene.ID(required = True))
    all_projects_per_user_and_tasks_for_the_past_week = graphene.List(project_type, username=graphene.String(required=True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_tasks_for_a_project_per_user = graphene.List(task_type, project_id=graphene.ID(required=True), username=graphene.String(required=True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_tasks_for_a_user_per_week_per_project = graphene.List(task_type, entries_per_page= graphene.Int(),page_number= graphene.Int(), project_id=graphene.ID(required=True), username=graphene.ID(required=True))
    all_on_hold_projects_per_user= graphene.List(project_type, status_id = graphene.ID(required=True), username = graphene.String(required = True),  entries_per_page= graphene.Int(),page_number= graphene.Int())
    all_completed_projects_per_user= graphene.List(project_type, username = graphene.String(required = True),  entries_per_page= graphene.Int(),page_number= graphene.Int(), status_id = graphene.ID(required=True))





    # @login_required
    def resolve_all_projects(self, info, page_number=1, entries_per_page=10, **kwargs, ):
        return Query.pagination(project.objects.all(),entries_per_page,page_number)


    def pagination( query_set,entries_per_page, page_number):
        paginator = Paginator(query_set, entries_per_page)
        tuples_per_page = paginator.get_page(page_number)
        return tuples_per_page


    def resolve_one_project(self, info,project_id):
        try:
            return project.objects.get(project_id=project_id)
        except ObjectDoesNotExist:
            raise GraphQLError("The object was not found.")


    # @login_required
    def resolve_all_categories(self, info, page_number=1, entries_per_page=5,**kwargs):
        return Query.pagination(project_categories.objects.all(),entries_per_page,page_number)


    def resolve_one_category (self, info,category_id):
        try:
            return project_categories.objects.get(category_id=category_id)
        except ObjectDoesNotExist:
            raise GraphQLError("The object was not found.")


    # @login_required
    def resolve_all_status(self, info, page_number=1, entries_per_page=10, **kwargs):
        return Query.pagination(status.objects.all(),entries_per_page,page_number)


    # @login_required
    def resolve_one_status(self, info, status_id):
        try:
            return status.objects.get(pk=status_id)
        except ObjectDoesNotExist:
            raise GraphQLError("The object was not found.")


    # @login_required
    def resolve_all_tasks(self, info, page_number=1, entries_per_page=10, **kwargs):
        return Query.pagination(task.objects.all(),entries_per_page,page_number)


    # @login_required
    def resolve_all_tasks_for_a_project_per_user(self, info, project_id, username, page_number=1, entries_per_page=10):
        all_tasks_for_the_project = task.objects.filter(project_id=project_id)
        List = []
        for tuple in all_tasks_for_the_project:
            if tuple.user_id.username == username:
                List.append(tuple)
        return Query.pagination(List,entries_per_page,page_number)


    # @login_required
    def resolve_all_enrollments(self, info, page_number=1, entries_per_page=10):
        return Query.pagination(enrollment.objects.all(),entries_per_page,page_number)


    def resolve_all_tasks_for_a_user_per_week_per_project(self, info, project_id, username, page_number=1, entries_per_page=10, **kwargs):
        queryset = task.objects.filter(project_id=project_id)
        current_unix_time= datetime.timestamp(datetime.now())
        List =[]

        for tuple in queryset:
            if tuple.user_id.username == username:
                datetime_from_date = datetime( tuple.task_start_date.year, tuple.task_start_date.month, tuple.task_start_date.day)
                start_date_unix_time = datetime.timestamp(datetime_from_date)
                if  current_unix_time - start_date_unix_time >=0 and current_unix_time - start_date_unix_time <= 7*86400:
                        List.append(tuple)
        return Query.pagination(List, entries_per_page, page_number)


    # @login_required
    def resolve_all_roles(self, info, page_number=1, entries_per_page=10, **kwargs):
        return Query.pagination(role.objects.all(),entries_per_page,page_number)


    # @login_required
    # @staff_member_required
    def resolve_all_on_hold_projects(self, info, status_id, page_number=1, entries_per_page=10):
        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id  == status_object.status_id:
                    List.append(one_project)
            return Query.pagination(List, entries_per_page, page_number)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")


    # @login_required
    # @staff_member_required
    def resolve_count_all_on_hold_projects(self, info, status_id):
        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id  == status_object.status_id:
                    List.append(one_project)
            return len(List)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")



    # @login_required
    def resolve_all_on_hold_projects_per_user(self, info, status_id, username, page_number=1, entries_per_page=10):

        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id  == status_object.status_id:
                    userObjects = one_project.project_members.all()
                    for one_user in userObjects:
                        if username == one_user.username:
                            List.append(one_project)
            return Query.pagination(List,entries_per_page,page_number)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")




    # @login_required
    def resolve_count_all_on_hold_projects_per_user(self, info, status_id, username):
        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id  == status_object.status_id:
                    userObjects = one_project.project_members.all()
                    for one_user in userObjects:
                        if username == one_user.username:
                            List.append(one_project)
            return len(List)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")


    # @login_required
    # @staff_member_required
    def resolve_all_completed_projects(self, info, status_id, page_number=1, entries_per_page=10):
        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id == status_object.status_id:
                    List.append(one_project)
            return Query.pagination(List, entries_per_page,page_number)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")

    # @login_required
    # @staff_member_required
    def resolve_count_all_completed_projects(self, info, status_id):
        try:
            status_object = status.objects.get(pk=status_id)
            return project.objects.filter(project_status=status_object.status_id).count()
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")


    # @login_required
    def resolve_all_completed_projects_per_user(self, info, status_id, username, page_number=1, entries_per_page=10):
        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id  ==status_object.status_id:
                    userObjects = one_project.project_members.all()
                    for one_user in userObjects:
                        if username == one_user.username:
                            List.append(one_project)
            return Query.pagination(List, entries_per_page,page_number)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")



    # @login_required
    def resolve_count_all_completed_projects_per_user(self, info, status_id, username):
        try:
            status_object = status.objects.get(pk=status_id)
            List =[]
            all_projects = project.objects.all()
            for one_project in all_projects:
                if one_project.project_status.status_id  == status_object.status_id:
                    userObjects = one_project.project_members.all()
                    for one_user in userObjects:
                        if username == one_user.username:
                            List.append(one_project)
            return len(List)
        except ObjectDoesNotExist:
            raise GraphQLError("The status object was not found.")

    # @login_required
    # @staff_member_required
    def resolve_all_delayed_projects(self, info, page_number=1, entries_per_page=10):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
                if current_unix_time > datetime.timestamp(datetime_from_date):
                    List.append(one_project)
        return Query.pagination(List, entries_per_page,page_number)


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
    def resolve_all_delayed_projects_per_user(self, info, username, page_number=1, entries_per_page=10):
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
        return Query.pagination(List, entries_per_page,page_number)


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
    def resolve_all_on_progress_projects(self, info, page_number=1, entries_per_page=10):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                datetime_from_date = datetime( one_project.project_end_date.year, one_project.project_end_date.month, one_project.project_end_date.day)
                if current_unix_time <= datetime.timestamp(datetime_from_date):
                    List.append(one_project)
        return Query.pagination(List, entries_per_page,page_number)


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
    def resolve_all_on_progress_projects_per_user(self, info, username, page_number=1, entries_per_page=10):
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
        return Query.pagination(List, entries_per_page,page_number)


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
        return len(List)


    # @login_required
    def resolve_get_any_week_tasks(self, info, start_date, end_date , project_id , page_number=1, entries_per_page=10):
        all_tasks = task.objects.filter(project_id = project_id)

        start_date_unix_time  = datetime.timestamp(datetime(start_date.year, start_date.month, start_date.day))
        end_date_unix_time = datetime.timestamp(datetime(end_date.year, end_date.month, end_date.day))

        List=[]
        for tuple in all_tasks:
            task_start_date_unix_time = datetime.timestamp(datetime( tuple.task_start_date.year, tuple.task_start_date.month, tuple.task_start_date.day))
            task_end_date_unix_time  = datetime.timestamp(datetime( tuple.task_completion_date.year, tuple.task_completion_date.month, tuple.task_completion_date.day))

            if task_start_date_unix_time >= start_date_unix_time and task_end_date_unix_time <= end_date_unix_time:
                List.append(tuple)
        return Query.pagination(List, entries_per_page,page_number)


    # @login_required
    def resolve_all_projects_of_a_particular_user(self, info,username, page_number=1, entries_per_page=10):
        List =[]
        all_projects = project.objects.all()
        for one_project in all_projects:
            userObjects = one_project.project_members.all()
            for one_user in userObjects:
                if username == one_user.username:
                    List.append(one_project)
        return Query.pagination(List, entries_per_page,page_number)


    def resolve_all_projects_per_user_and_tasks_for_the_past_week(self, info, username, page_number=1, entries_per_page=10):
        current_unix_time= datetime.timestamp(datetime.now())
        queryset= project.objects.all()
        List = []
        for one_project in queryset:
                all_members = one_project.project_members.all()
                for one_member in all_members:
                    if one_member.username == username:
                        all_tasks = one_project.task_set.all()
                        for one_task in all_tasks:
                            datetime_from_date = datetime( one_task.task_start_date.year, one_task.task_start_date.month, one_task.task_start_date.day)
                            start_date_unix_time = datetime.timestamp(datetime_from_date)
                            if  current_unix_time - start_date_unix_time >=0 and current_unix_time - start_date_unix_time <= 7*86400:
                                List.append(one_project)
        return Query.pagination(List, entries_per_page,page_number)


    def resolve_count_total_projects(self, info, page_number=1, entries_per_page=10):
        return len(project.objects.all())


    def resolve_count_total_projects_per_user(self,info, username):
        all_projects = project.objects.all()
        List =[]
        for one_project in all_projects:
            users = one_project.project_members.all()
            for one_user in users:
                if one_user.username == username:
                    List.append(one_project)
        return len(List)


    def resolve_manager_summary_report(self,info, page_number=1, entries_per_page=10,**kwargs):
        all_projects = project.objects.all()
        workdone_tasks_for_all_projects = []
        wayforward_tasks_for_all_projects = []
        summary_report=[]
        current_unix_time= datetime.timestamp(datetime.now())

        for one_project in all_projects:
                all_tasks = one_project.task_set.all()
                for one_task in all_tasks:
                    start_date_unix_time = datetime.timestamp(datetime( one_task.task_start_date.year, one_task.task_start_date.month, one_task.task_start_date.day))
                    end_date_unix_time = datetime.timestamp(datetime( one_task.task_completion_date.year, one_task.task_completion_date.month, one_task.task_completion_date.day))

                    if  current_unix_time - start_date_unix_time >=0 and current_unix_time - start_date_unix_time <= 7*86400:
                        workdone_tasks_for_all_projects.append(one_task)

                    elif end_date_unix_time - current_unix_time >=0 and  end_date_unix_time - current_unix_time <= 6*86400:
                        wayforward_tasks_for_all_projects.append(one_task)

        summary_report = wayforward_tasks_for_all_projects + workdone_tasks_for_all_projects
        return Query.pagination(summary_report, entries_per_page,page_number)

