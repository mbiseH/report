import os
import xlwt
import  graphene
from xlutils.copy import copy
from datetime import datetime
from xlrd import open_workbook
from graphql import GraphQLError
from django.http import HttpResponse
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from django.shortcuts import render, redirect
from graphql_jwt.decorators import login_required
from django.views.generic.base import TemplateView
from graphql_jwt.decorators import staff_member_required
from CRUD_BACKEND.models import role, tasks, project, user, report



class role_type(DjangoObjectType):
    class Meta:
        model = role

class task_type(DjangoObjectType):
    class Meta:
        model = tasks

class project_type(DjangoObjectType):
    class Meta:
        model = project

class user_type(DjangoObjectType):
    class Meta:
        model = user

class report_type(DjangoObjectType):
    class Meta:
        model = report

class UserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    username = graphene.String(required=True)





class Query(graphene.ObjectType):

    all_projects= graphene.List(project_type)
    project = graphene.List(project_type, project_id = graphene.ID())

    # @login_required
    def resolve_all_projects(self, info, **kwargs):
        return project.objects.all()

    @login_required
    def resolve_project (self, info, project_id):
        return project.objects.filter(pk=project_id)



class CreateProject(graphene.Mutation):

    class  Arguments:

        project_name = graphene.String(required= True)
        project_members = graphene.List(of_type=UserInput)
        project_status = graphene.String(required= True)
        project_start_date = graphene.String(required= True)
        project_end_date = graphene.String(required= True)
        project_client = graphene.String(required= True)
        project_description = graphene.String(required= True)
        project_comments = graphene.String(required= True)
        project_remarks = graphene.String(required= True)
        project_leader = graphene.String(required= True)

    project = graphene.Field(project_type)


    try:
        # @staff_member_required
        def mutate(self, info,
                project_name, project_members, project_status,
                project_start_date, project_end_date, project_client,
                project_description, project_leader,project_comments,
                project_remarks):
                # try:
                start_date_date_object = datetime.strptime(project_start_date, '%Y-%m-%d').date()
                end_date_date_object = datetime.strptime(project_end_date, '%Y-%m-%d').date()

                createdProject= project.objects.create (

                            project_name = project_name,
                            project_status = project_status,
                            project_start_date = start_date_date_object,
                            project_end_date = end_date_date_object,
                            project_client = project_client,
                            project_description = project_description,
                            project_remarks = project_remarks,
                            project_leader = project_leader,
                            project_comments = project_comments)

                if project_members is not None:
                    for member in project_members:
                        createdProject.project_members.add(member.username)
                        createdProject.save()
                return CreateProject( project = createdProject)

                # except:
                #     raise GraphQLError("A problem occurred during the project creation!")


    except:
        raise GraphQLError("Dear User, A problem occurred during the project creation!")




class CreateTask(graphene.Mutation):

    class  Arguments:

        task_description = graphene.String(required = True)
        task_completion_date = graphene.Date(required = True)
        task_status = graphene.String(required = True)
        associated_project = graphene.ID(required = True)

    task = graphene.Field(task_type)

    try:
        @login_required
        def mutate(self, info, task_description , task_completion_date, task_status,associated_project ):

            projectObject = project.objects.filter(pk=associated_project)

            if projectObject is not None:
                    createdTask= tasks.objects.create (
                        task_description= task_description,
                        task_completion_date = task_completion_date,
                        task_status = task_status,
                        project_id = projectObject)

                    return CreateTask(task = createdTask)

            else:
                raise GraphQLError("The project you are trying to create a task does not exist")
    except:
        raise GraphQLError("A problem occurred.")




class UpdateTask(graphene.Mutation):

    class  Arguments:
        task_id =  graphene.ID(required= True)
        task_description =  graphene.String()
        task_completion_date = graphene.Date()
        task_status = graphene.String()

    task = graphene.Field(task_type)
    try:
        @login_required
        def mutate(self, info, task_id, task_description=None , task_completion_date=None, task_status=None):

            updatedTask = tasks.objects.filter(pk=task_id)

            updatedTask.task_description = task_description if task_description is not None else  updatedTask.task_description
            updatedTask.task_status = task_status if task_status is not None else updatedTask.task_status

            if task_completion_date is not None:
                date_object = datetime.strptime(task_completion_date, "%Y-%m-%d").date()
                updatedTask.task_completion_date = date_object

            updatedTask.save()
            return UpdateTask( task = updatedTask)
    except:
            raise GraphQLError("A problem occurred in the task update process.")



class UpdateProject(graphene.Mutation):

    class  Arguments:

        project_id = graphene.ID(required=True)
        project_name = graphene.String()
        project_members = graphene.List(graphene.ID)
        project_status = graphene.String()
        project_end_date = graphene.String()
        project_client = graphene.String()
        project_description = graphene.String()
        project_comments = graphene.String()
        project_remarks = graphene.String()
        project_leader = graphene.String()

    project = graphene.Field(project_type)
    try:
        @login_required
        @staff_member_required
        def mutate(self, info, project_id, project_description = None, project_name = None,
                project_members = None,project_status = None, project_end_date = None,
                project_client = None, project_comments = None, project_remarks = None,
                project_leader = None):

            updatedProject = project.objects.filter(pk=project_id)

            updatedProject.task_description = project_description if project_description is not None else  updatedProject.task_description
            updatedProject.project_name = project_name if project_name is not None else  updatedProject.project_name
            updatedProject.project_status = project_status if project_status is not None else  updatedProject.project_status
            updatedProject.project_client = project_client if project_client is not None else  updatedProject.project_client
            updatedProject.project_description = project_description if project_description is not None else  updatedProject.project_description
            updatedProject.project_comments = project_comments if project_comments is not None else  updatedProject.project_comments
            updatedProject.project_remarks = project_remarks if project_remarks is not None else  updatedProject.project_remarks
            updatedProject.project_leader = project_leader if project_leader is not None else  updatedProject.project_leader

            if project_end_date is not None:
                date_object = datetime.strptime(project_end_date, "%Y-%m-%d").date()
                updatedProject.project_end_date = date_object

            if project_members is not None:
                updatedProject.groups = user.objects.filter(pk__in=project_members)

            updatedProject.save()
            return UpdateTask( task = updatedProject)
    except:
            raise GraphQLError("A problem occurred.Please try again.")


class CreateRole(graphene.Mutation):

    class  Arguments:
        role_name = graphene.String()

    role = graphene.Field(role_type)

    try:
        @staff_member_required
        def mutate(self, info,role_name):
            createdRole = role.objects.create (role_name =role_name)
            return CreateRole( role_name  = createdRole)
    except:
        raise GraphQLError("Ooops, something went wrong.")



class CreateReport(graphene.Mutation):

    class  Arguments:
        project_id = graphene.ID(required=True)
        report_start_date = graphene.Date(required = True)
        report_end_date = graphene.Date(required=True)


    report = graphene.Field(report_type)

    try:
        @login_required
        def mutate(self, info,project_id, report_start_date, report_end_date):

            start_date_object = datetime.strptime(report_start_date,"%Y-%m-%d").date()
            end_date_object   = datetime.strptime(report_end_date,"%Y-%m-%d").date()
            project_object    = project.objects.filter(id=project_id)
            tasks_object      = tasks.objects.list(project_id= project_id)

            if start_date_object and end_date_object and project_object is not None:

                createdReport = report.objects.create (
                                report_start_date = start_date_object,
                                report_end_date = end_date_object,
                                task_description = tasks_object.task_description,
                                task_start_date = tasks_object.task_start_date,
                                task_completion_date = tasks_object.task_completion_date,
                                task_status = tasks_object.tasks_object,
                                project_name = project_object.project_name,
                                project_members = project_object.project_members,
                                project_status = project_object.project_status,
                                project_start_date = project_object.project_start_date,
                                project_end_date = project_object.project_end_date,
                                project_client = project_object.project_client,
                                project_description = project_object.project_description,
                                project_comments = project_object.project_comments,
                                project_remarks = project_object.project_name,
                                project_leader = project_object.project_leader,
                    )
                return CreateReport( createdReport  = createdReport)

            else:
                return GraphQLError("Provide Project name that exists and a valid date in a YYYY-MM-DD format.")
    except:
        raise GraphQLError("Ooops, something went wrong.")


class UpdateRole(graphene.Mutation):

    class  Arguments:
        role_id = graphene.ID()
        role_name = graphene.String()

    role = graphene.Field(role_type)
    try:
        @staff_member_required
        def mutate(self, info, role_id, role_name):

            updatedRole = role.objects.filter(id =role_id)
            updatedRole.role_name = role_name

            updatedRole.save()
            return UpdateRole( updatedRole  = updatedRole)
    except:
        raise GraphQLError("A problem occurred.")







# class ExcelPageView(TemplateView):
#     template_name = "excel_home.html"



# def export_project_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename= projects_report' + str(datetime.datetime.now()) + '.xls'

#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Weekly Report ') # sheet of project Data

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['S/N', 'Client/Institution', 'Description', 'Project Team',
#                'Status', 'Actions Taken During the Week and Plan', 'Project Comments',
#                'Start Date', 'Expected Completion Date', 'Blocking Issues', 'Remarks']

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()

#     rows = report.objects.filter(project_id=request.user).values_list('report_id', 'project_client', 'project_description', 'project_members',
#                                             'project_status', 'project_remarks','project_comments', 'project_start_date'
#                                             'project_end_date', 'project_remarks','project_remarks')
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)

#     return response


# def export_styling_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="projects.xls"'

#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Styling Data') # this will make a sheet named Users Data - First Sheet
#     styles = dict(
#         bold = 'font: bold 1',
#         italic = 'font: italic 1',
#         # Wrap text in the cell
#         wrap_bold = 'font: bold 1; align: wrap 1;',
#         # White text on a blue background
#         reversed = 'pattern: pattern solid, fore_color blue; font: color white;',
#         # Light orange checkered background
#         light_orange_bg = 'pattern: pattern fine_dots, fore_color white, back_color orange;',
#         # Heavy borders
#         bordered = 'border: top thick, right thick, bottom thick, left thick;',
#         # 16 pt red text
#         big_red = 'font: height 320, color red;',
#     )

#     for idx, k in enumerate(sorted(styles)):
#         style = xlwt.easyxf(styles[k])
#         ws.write(idx, 0, k)
#         ws.write(idx, 1, styles[k], style)

#     wb.save(response)

#     return response



# def export_write_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="projects.xls"'

#     path = os.path.dirname(__file__)
#     file = os.path.join(path, 'sample.xls')

#     rb = open_workbook(file, formatting_info=True)
#     r_sheet = rb.sheet_by_index(0)

#     wb = copy(rb)
#     ws = wb.get_sheet(0)

#     row_num = 2 # index start from 0
#     rows = report.objects.all().values_list('report_id', 'project_client', 'project_description', 'project_members',
#                                             'project_status', 'project_remarks','project_comments', 'project_start_date'
#                                             'project_end_date', 'project_remarks','project_remarks')

#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num])

#     # wb.save(file) # will replace original file
#     # wb.save(file + '.out' + os.path.splitext(file)[-1]) # will save file where the excel file is
#     wb.save(response)



class Mutation(graphene.ObjectType):

    Create_Project = CreateProject.Field()
    Update_Project = CreateProject.Field()

    Create_Task = CreateTask.Field()
    Update_Task = UpdateTask.Field()

    Create_Role = CreateRole.Field()
    Update_Role = UpdateRole.Field()
