
import os
import uuid
import  graphene
import pandas as pd
from datetime import datetime, date
from graphql import GraphQLError
from django.conf import settings
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.core.files.storage import FileSystemStorage
from graphql_jwt.decorators import staff_member_required
from CRUD_BACKEND.models import role, tasks, project, user, report, enrollment



class role_type(DjangoObjectType):
    class Meta:
        model = role

class enrollment_type(DjangoObjectType):
    class Meta:
        model = enrollment

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
        project_leader_id = graphene.String()

    project = graphene.Field(project_type)


    try:
        # @staff_member_required
        def mutate(self, info,
                project_name, project_status,project_start_date, project_end_date,
                project_client,project_description, project_comments,project_remarks, project_leader_id=None):

                    start_date_object = datetime.strptime(project_start_date, '%Y-%m-%d').date()
                    end_date_object = datetime.strptime(project_end_date, '%Y-%m-%d').date()
                    try:
                        if project_leader_id is not None:
                            user_id = from_global_id(project_leader_id)[1]
                            userObject = user.objects.get(pk=user_id)
                            createdProject= project.objects.create (

                                        project_name = project_name,
                                        project_status = project_status,
                                        project_start_date = start_date_object,
                                        project_end_date = end_date_object,
                                        project_client = project_client,
                                        project_description = project_description,
                                        project_remarks = project_remarks,
                                        project_leader = userObject,
                                        project_comments = project_comments)

                        else:
                            createdProject= project.objects.create (

                                            project_name = project_name,
                                            project_status = project_status,
                                            project_start_date = start_date_object,
                                            project_end_date = end_date_object,
                                            project_client = project_client,
                                            project_description = project_description,
                                            project_remarks = project_remarks,
                                            project_comments = project_comments)

                        return CreateProject( project = createdProject)

                    except:
                        raise GraphQLError("This project exists!")

    except:
        raise GraphQLError("Dear User, A problem occurred during the project creation!")




class UpdateProject(graphene.Mutation):

    class  Arguments:

        project_id = graphene.ID(required=True)
        project_name = graphene.String()
        project_status = graphene.String()
        project_end_date = graphene.Date()
        project_client = graphene.String()
        project_description = graphene.String()
        project_comments = graphene.String()
        project_remarks = graphene.String()
        project_leader_id = graphene.ID()
        project_start_date = graphene.Date()

    project = graphene.Field(project_type)

    try:
        # @login_required
        # @staff_member_required
        def mutate(self, info, project_id, project_description = None, project_name = None,
                project_status = None, project_end_date = None,
                project_client = None, project_comments = None, project_remarks = None,
                project_leader_id = None,project_start_date=None):

            updatedProject = project.objects.get(pk=project_id)

            if  updatedProject is not None:
                updatedProject.project_description = project_description if project_description is not None else  updatedProject.project_description
                updatedProject.project_name = project_name if project_name is not None else  updatedProject.project_name
                updatedProject.project_status = project_status if project_status is not None else  updatedProject.project_status
                updatedProject.project_client = project_client if project_client is not None else  updatedProject.project_client
                updatedProject.project_description = project_description if project_description is not None else  updatedProject.project_description
                updatedProject.project_comments = project_comments if project_comments is not None else  updatedProject.project_comments
                updatedProject.project_remarks = project_remarks if project_remarks is not None else  updatedProject.project_remarks
                updatedProject.project_start_date = project_start_date if project_start_date is not None else  updatedProject.project_start_date
                updatedProject.project_end_date = project_end_date if project_end_date is not None else  updatedProject.project_end_date

                if project_leader_id is not None:

                    user_id = from_global_id(project_leader_id)[1]
                    userObject = user.objects.get(pk=user_id)
                    updatedProject.project_leader = userObject

                updatedProject.save()
                return UpdateProject( project = updatedProject)
            else:
                raise GraphQLError("The project does not exist.")

    except:
            raise GraphQLError("A problem occurred.Please try again.")



class DeleteProject(graphene.Mutation):

    class  Arguments:

        project_id = graphene.ID(required=True)

    project = graphene.Field(project_type)

    try:
        # @login_required
        # @staff_member_required
        def mutate(self, info, project_id):

            deletedProject = project.objects.get(pk=project_id)
            if deletedProject:
                deletedProject.delete()
                return DeleteProject( project = deletedProject)
            else:
                raise GraphQLError("The project does not exist.")

    except:
            raise GraphQLError("A problem occurred.Please try again.")



class CreateEnrollment(graphene.Mutation):

    class  Arguments:
            project_id = graphene.ID(required= True)
            user_id = graphene.ID(required= True)

    enrollment = graphene.Field(enrollment_type)

    # @staff_member_required
    def mutate(self, info, project_id , user_id):


        projectObject= project.objects.get(pk=project_id)
        id = from_global_id(user_id)[1]
        userObject = user.objects.get(pk=id)

        try:

            if userObject and projectObject is not None:

                createdEnrollment, created= enrollment.objects.get_or_create (project_id=projectObject, user_id=userObject, project_name = projectObject.project_name)
                projectObject.project_members.add(userObject.id)
                projectObject.save()

                return CreateEnrollment(enrollment=createdEnrollment)


        except:
            raise GraphQLError("This user is added to the project already! Try using another user.")



class DeleteEnrollment(graphene.Mutation):

    class  Arguments:
            project_id = graphene.ID(required= True)
            user_id_to_be_removed = graphene.ID(required= True)
            enrollment_id = graphene.ID(required= True)

    enrollment = graphene.Field(enrollment_type)

    # @staff_member_required
    def mutate(self, info, project_id, enrollment_id,user_id_to_be_removed):


        try:
            deletedEnrollment= enrollment.objects.get(pk = enrollment_id)

            try:
                projectObject= project.objects.get(pk=project_id)
                id = from_global_id(user_id_to_be_removed)[1]
                projectObject.project_members.remove(id)

                deletedEnrollment.delete()
                projectObject.save()

                return DeleteEnrollment(enrollment=deletedEnrollment)

            except project.DoesNotExist:
                raise GraphQLError("Project Does not exist!")

        except enrollment.DoesNotExist:
            raise GraphQLError("Enrollment Does not exist!")








class CreateTask(graphene.Mutation):

    class  Arguments:

        task_description = graphene.String(required = True)
        task_completion_date = graphene.Date(required = True)
        task_status = graphene.String(required = True)
        project_id = graphene.ID(required = True)
        user_id = graphene.ID(required = True)
        task_start_date = graphene.Date(required = True)


    task = graphene.Field(task_type)

    try:
        # @login_required
        def mutate(self, info, task_description , user_id, task_completion_date, task_status,project_id, task_start_date ):

            id = from_global_id(user_id)[1]
            userObject = user.objects.get(pk=id)
            projectObject = project.objects.get(pk=project_id)

            if projectObject is not None:
                    createdTask, created= tasks.objects.get_or_create (
                        task_description= task_description,
                        task_completion_date = task_completion_date,
                        task_status = task_status,
                        project_id = projectObject,
                        task_start_date = task_start_date,
                        user_id=userObject)

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

        @login_required
        def mutate(self, info, task_id, task_description=None , task_completion_date=None, task_status=None):

            updatedTask = tasks.objects.get(pk=task_id)

            if updatedTask:
                updatedTask.task_description = task_description if task_description is not None else  updatedTask.task_description
                updatedTask.task_status = task_status if task_status is not None else updatedTask.task_status
                updatedTask.task_completion_date = task_completion_date if task_status is not None else updatedTask.task_completion_date

                updatedTask.save()
                return UpdateTask( task = updatedTask)
            else:
                raise GraphQLError("A problem occurred in the task update process.")


class  DeleteTask(graphene.Mutation):

    class Arguments:
        task_id = graphene.ID(required=True)

    task = graphene.Field(task_type)

    # @login_required
    # @staff_member_required
    def  mutate(self, info, task_id):


        try:
            deleted_task = tasks.objects.get(pk=task_id)
            deleted_task.delete()
            return DeleteTask(task = deleted_task)

        except tasks.DoesNotExist:
            raise GraphQLError ("task does not exist")


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
        # @login_required
        def mutate(self, info,project_id, report_start_date, report_end_date):


            try:
                project_object    = project.objects.get(id=project_id)

                try:
                    tasks_queryset  = tasks.objects.filter(project_id= project_id).values
                    ('task_description','task_start_date', 'task_completion_date', 'task_status')

                    createdReport, created = report.objects.get_or_create (
                    report_start_date = report_start_date,
                    report_end_date = report_end_date,
                    # task_description = tasks_object.task_description,
                    # task_start_date = tasks_object.task_start_date,
                    # task_completion_date = tasks_object.task_completion_date,
                    # task_status = tasks_object.tasks_object,
                    project_name = project_object.project_name,
                    project_members = project_object.project_members,
                    project_status = project_object.project_status,
                    project_start_date = project_object.project_start_date,
                    project_end_date = project_object.project_end_date,
                    project_client = project_object.project_client,
                    project_description = project_object.project_description,
                    project_comments = project_object.project_comments,
                    project_remarks = project_object.project_name,
                    project_leader = project_object.project_leader)

                    return CreateReport( createdReport  = createdReport)
                except tasks.DoesNotExist:
                        raise GraphQLError(" The task does not exist")

            except project.DoesNotExist:
                raise GraphQLError("project does not exist")
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







# class export_write_xls(graphene.Mutation):

    # class Arguments:
    #     enrollment_id = graphene.ID(required=True)

    # success = graphene.Boolean()
    # full_file_url = graphene.String()
    # file_name = graphene.String()

    # def mutate(self, info,  enrollment_id, **kwargs):
    #     current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    #     report_name = 'WeeklyReport ' +str(current_time)+'.xlsx'

    #     writer = pd.ExcelWriter(report_name, engine='xlsxwriter')
    #     # data = enrollment.objects.filter(enrollment_id=enrollment_id)
    #     data = enrollment.objects.all()
    #     df = pd.DataFrame(data)
    #     df.to_excel(writer, sheet_name='Weekly Report', index=False)
    #     writer.save()


    #     try:
    #         if os.mkdir(os.path.join(str(settings.MEDIA_ROOT)+'/documents/', current_time)):
    #             pass
    #         else:
    #             raise GraphQLError ("Folder Exists")
    #         fs = FileSystemStorage(location=str(settings.MEDIA_ROOT)+'/documents/'+ current_time)

    #     except:
    #         fs = FileSystemStorage(location=str(settings.MEDIA_ROOT)+'/documents/'+ current_time)


    #     new_file_name,ext=os.path.splitext(writer.path)
    #     modified_name = '{}_{}{}'.format(new_file_name, current_time,ext)

    #     excel_attachment=fs.save(modified_name, report_name)
    #     excel_file_url = fs.url('/documents/'+current_time+"/"+ excel_attachment)

    #     save_path = os.path.join(str(settings.MEDIA_ROOT)+'/documents/'+current_time,str(modified_name))
    #     saved_file_name, file_extension=os.path.splitext(save_path)

    #     full_file_url=str(excel_file_url)
    #     file_name=writer.path

    #     return export_write_xls(success=True,full_file_url=full_file_url,file_name=file_name)




class Mutation(graphene.ObjectType):


    # Create_Report = CreateReport.Field()

    Create_Task = CreateTask.Field()
    Update_Task = UpdateTask.Field()
    Delete_Task = DeleteTask.Field()

    Create_Role = CreateRole.Field()
    Update_Role = UpdateRole.Field()

    Create_Project = CreateProject.Field()
    Update_Project = UpdateProject.Field()
    Delete_Project = DeleteProject.Field()

    # Generate_Report = export_write_xls.Field()

    Create_Enrollment = CreateEnrollment.Field()
    Delete_Enrollment = DeleteEnrollment.Field()

