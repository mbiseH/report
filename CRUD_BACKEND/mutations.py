
import os
import  graphene
import pandas as pd
from datetime import datetime, timedelta
from graphql import GraphQLError
from django.conf import settings
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from graphql_jwt.decorators import staff_member_required
from CRUD_BACKEND.models import role, task, project, user, status, report, enrollment, project_categories



class role_type(DjangoObjectType):
    class Meta:
        model = role



class status_type(DjangoObjectType):
    class  Meta:
        model = status


class category_type(DjangoObjectType):
    class Meta:
        model = project_categories

class enrollment_type(DjangoObjectType):
    class Meta:
        model = enrollment

class task_type(DjangoObjectType):
    class Meta:
        model = task

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
    username = graphene.String()

class Task_Input(graphene.InputObjectType):
    task_description = graphene.String(required=True)




class CreateProject(graphene.Mutation):
    class Arguments:

        project_name = graphene.String(required= True)
        project_members = graphene.List(required=True,of_type=UserInput)
        project_status_id = graphene.String(required= True)
        project_start_date = graphene.Date(required= True)
        project_end_date = graphene.Date(required= True)
        project_client = graphene.String(required= True)
        project_description = graphene.String(required= True)
        project_leader_id = graphene.String(required=True)
        project_category_id = graphene.ID(required=True)

    project = graphene.Field(project_type)
    success = graphene.Boolean(required=True)



    try:
        # @staff_member_required
        def mutate(self, info, project_category_id,
                project_name, project_status_id,project_start_date, project_end_date,
                project_client,project_description, project_leader_id, project_members):


                    try:
                        project_leader = from_global_id(project_leader_id)[1]
                        userObject = user.objects.get(pk=project_leader)
                        try:
                            project_category_object = project_categories.objects.get(pk = project_category_id )

                            try:
                                project_status_object = status.objects.get(pk = project_status_id)
                                createdProject, created= project.objects.get_or_create (
                                                            project_name = project_name,
                                                            project_status = project_status_object,
                                                            project_start_date = project_start_date,
                                                            project_end_date = project_end_date,
                                                            project_client = project_client,
                                                            project_description = project_description,
                                                            project_leader = userObject,
                                                            project_category=project_category_object)
                                if project_members is not None:
                                    for one_member in project_members:
                                        member_id = from_global_id(one_member.id)[1]
                                        createdProject.project_members.add(member_id)
                                        createdProject.save()
                                        return CreateProject( project = createdProject, success=created)
                            except status.DoesNotExist:
                                raise GraphQLError("Status does not exist")
                        except project_categories.DoesNotExist:
                            raise GraphQLError("Category does not exist")
                    except user.DoesNotExist:
                        raise GraphQLError("A problem occurred in fetching the project Leader.")



    except:
        raise GraphQLError("Dear User, A problem occurred during the project creation!")




class UpdateProject(graphene.Mutation):

    class  Arguments:

        project_id = graphene.ID(required=True)
        project_name = graphene.String()
        project_status = graphene.String()
        project_end_date = graphene.Date()
        project_client = graphene.String()
        project_leader_id = graphene.ID()
        project_remarks = graphene.String()
        project_start_date = graphene.Date()
        project_comments = graphene.String()
        project_members = graphene.List(of_type=UserInput)
        project_description = graphene.String()

    project = graphene.Field(project_type)

    try:
        # @login_required
        # @staff_member_required
        def mutate(self, info, project_id, project_description = None, project_name = None,
                project_status = None, project_end_date = None,
                project_client = None, project_comments = None, project_remarks = None,
                project_leader_id = None,project_start_date=None, project_members=None):

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

                if project_members is not None:
                    for one_member in project_members:
                        member_id = from_global_id(one_member.id)[1]
                        updatedProject.project_members.add(member_id)
                        updatedProject.save()


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
    success = graphene.Boolean()

    # @staff_member_required
    def mutate(self, info, project_id , user_id):


        projectObject= project.objects.get(pk=project_id)
        id = from_global_id(user_id)[1]
        userObject = user.objects.get(pk=id)

        try:

            if userObject and projectObject is not None:

                createdEnrollment, created= enrollment.objects.get_or_create (
                    project_id=projectObject,
                    user_id=userObject,
                    project_name = projectObject.project_name)
                projectObject.project_members.add(userObject.id)
                projectObject.save()

                return CreateEnrollment(enrollment=createdEnrollment, success = created)


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
    success = graphene.Boolean(required=True)


        # @login_required
    def mutate(self, info, task_description , user_id, task_completion_date, task_status,project_id, task_start_date ):
        try:
            id = from_global_id(user_id)[1]
            userObject = user.objects.get(pk=id)
        except user.DoesNotExist:
            raise GraphQLError("User does not exist")
        try:
            projectObject = project.objects.get(pk=project_id)
            userObjects = projectObject.project_members.all()

            created=False
            for member in userObjects:
                if member.username == userObject.username:
                    createdTask, created= task.objects.get_or_create (
                    task_description= task_description,
                    task_completion_date = task_completion_date,
                    task_status = task_status,
                    project_id = projectObject,
                    task_start_date = task_start_date,
                    user_id=userObject,)
            if created:
                    return CreateTask(task = createdTask, success = created)
            else:
                    return GraphQLError("Remember, task decription must be unique and User must be in project members.")

        except project.DoesNotExist:
            raise GraphQLError("Project Does not exist.")





class BatchCreateTask(graphene.Mutation):

    class  Arguments:

        workdone_tasks = graphene.List(of_type = Task_Input)
        way_forward_tasks = graphene.List(of_type = Task_Input)
        project_id = graphene.ID(required = True)
        user_id = graphene.ID(required = True)
        status_id = graphene.ID(required = True)

    # createdTasks = graphene.List(task_type)
    success = graphene.Boolean()

    try:
        # @login_required
        def mutate(self, info, status_id, user_id, project_id, way_forward_tasks=None , workdone_tasks =None ):

            try:
                id = from_global_id(user_id)[1]
                userObject = user.objects.get(pk=id)
                projectObject = project.objects.get(pk=project_id)
                status_object = status.objects.get(pk=status_id)
                if workdone_tasks is not None:
                    for one_task in workdone_tasks:

                            createdTask, created= task.objects.get_or_create (
                                task_description= one_task.task_description,
                                task_start_date = datetime.date(datetime.now())- timedelta(days=6),
                                task_completion_date = datetime.date(datetime.now()) ,
                                project_id = projectObject,
                                user_id=userObject,
                                task_status=status_object
                                )

                if way_forward_tasks is not None:
                    for one_task in way_forward_tasks:

                            createdTask, created= task.objects.get_or_create (
                                task_description= one_task.task_description,
                                task_start_date = datetime.date(datetime.now())+ timedelta(days=1),
                                task_completion_date = datetime.date(datetime.now()) + timedelta(days=7),
                                project_id = projectObject,
                                user_id=userObject,
                                task_status=status_object
                                )

                return BatchCreateTask(success=created)
            except ObjectDoesNotExist:
                raise GraphQLError("The user, status or the project you are creating task for, does not exist")


    except:
        raise GraphQLError("A problem occurred.")


class UpdateTask(graphene.Mutation):

        class  Arguments:
            task_id =  graphene.ID(required= True)
            task_description =  graphene.String()
            task_blocking_issue =  graphene.String()
            task_completion_date = graphene.Date()
            task_start_date = graphene.Date()
            task_status = graphene.String()

        task = graphene.Field(task_type)

        # @login_required
        def mutate(self, info, task_id,task_start_date =None, task_blocking_issue=None, task_description=None , task_completion_date=None, task_status=None):

            updatedTask = task.objects.get(pk=task_id)

            if updatedTask:
                updatedTask.task_description = task_description if task_description is not None else  updatedTask.task_description
                updatedTask.task_status = task_status if task_status is not None else updatedTask.task_status
                updatedTask.task_completion_date = task_completion_date if task_completion_date is not None else updatedTask.task_completion_date
                updatedTask.task_blocking_issue = task_blocking_issue if task_blocking_issue is not None else updatedTask.task_blocking_issue
                updatedTask.task_start_date = task_start_date if task_start_date is not None else updatedTask.task_start_date

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
            deleted_task = task.objects.get(pk=task_id)
            deleted_task.delete()
            return DeleteTask(task = deleted_task)

        except task.DoesNotExist:
            raise GraphQLError ("task does not exist")


class CreateRole(graphene.Mutation):

    class  Arguments:
        role_name = graphene.String(required=True)

    role = graphene.Field(role_type)

    try:
    # @staff_member_required
        def mutate(self, info,role_name, *kwargs):
            createdRole, created= role.objects.get_or_create (role_name =role_name)
            return CreateRole( role_name  = createdRole)
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

            updatedRole = role.objects.get(id =role_id)
            updatedRole.role_name = role_name

            updatedRole.save()
            return UpdateRole( updatedRole  = updatedRole)
    except:
        raise GraphQLError("A problem occurred.")






from django.core import files

class ExportExcel(graphene.Mutation):

    class Arguments:
        enrollment_id = graphene.ID()

    success = graphene.Boolean()
    full_file_url = graphene.String()
    file_name = graphene.String()

    def mutate(self, info, **kwargs):
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        report_name = 'WeeklyReport ' +str(current_time)+'.xlsx'

        writer = pd.ExcelWriter(report_name, engine='xlsxwriter')
        data = enrollment.objects.all()
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Weekly Report', index=False)
        writer.save()


        try:
            if os.mkdir(os.path.join(str(settings.MEDIA_ROOT)+'/documents/', current_time)):
                pass
            else:
                raise GraphQLError ("Folder Exists")
            fs = FileSystemStorage(location=str(settings.MEDIA_ROOT)+'/documents/'+ current_time)

        except:
            fs = FileSystemStorage(location=str(settings.MEDIA_ROOT)+'/documents/'+ current_time)

        new_file_name,ext=os.path.splitext(writer.path)
        modified_name = '{}_{}{}'.format(new_file_name, current_time,ext)

        reportFileObject = files.File( writer, name=modified_name)
        excel_attachment=fs.save(modified_name,reportFileObject )
        excel_file_url = fs.url('/documents/'+current_time+"/"+ excel_attachment)

        save_path = os.path.join(str(settings.MEDIA_ROOT)+'/documents/'+current_time,str(modified_name))
        saved_file_name, file_extension=os.path.splitext(save_path)

        full_file_url=str(excel_file_url)
        file_name=writer.path

        return ExportExcel(success=True,full_file_url=full_file_url,file_name=file_name)





class CreateCategory(graphene.Mutation):
    class Arguments:
        category_name = graphene.String(required=True)

    success = graphene.Boolean()
    created_category_object = graphene.Field(category_type)

    def mutate(self, info, category_name, **kwargs):
        try:
            createdCategory, created = project_categories.objects.get_or_create(
                category_name = category_name
            )
            return CreateCategory(created_category_object = createdCategory,success = created)
        except:
            return GraphQLError("Error Occured, please try again.")





class UpdateCategory(graphene.Mutation):
    class  Arguments:
        category_id = graphene.ID(required=True)
        category_name = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info,category_id,category_name, **kwargs ):
        try:
            category_object = project_categories.objects.get(category_id = category_id)
        except project_categories.DoesNotExist:
            raise GraphQLError("Category not found!")
        try:
            category_object.category_name = category_name
            category_object.save()
            return UpdateCategory(success=True)
        except:
            raise GraphQLError("Error Occured, please try again.")



class DeleteCategory(graphene.Mutation):
    class  Arguments:
        category_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info,category_id,**kwargs ):
        try:

            category_object = project_categories.objects.get(category_id = category_id)
            category_object.delete()
            return UpdateCategory(success=True)

        except project_categories.DoesNotExist:
            raise GraphQLError("Category not found!")







class CreateStatus(graphene.Mutation):
    class Arguments:
        status_name = graphene.String(required=True)

    success = graphene.Boolean()
    created_status_object = graphene.Field(status_type)

    def mutate(self, info, status_name, **kwargs):

            createdStatus, created = status.objects.get_or_create(
                status_name = status_name
            )
            return CreateStatus(created_status_object = createdStatus, success = created)






class UpdateStatus(graphene.Mutation):
    class  Arguments:
        status_id = graphene.ID(required=True)
        status_name = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, status_id,status_name, **kwargs ):
        try:
            status_object = status.objects.get(status_id = status_id)
        except status.DoesNotExist:
            raise GraphQLError("Status not found!")
        try:
            status_object.status_name = status_name
            status_object.save()
            if status_object.status_name == status_name:
                return UpdateStatus(success=True)
            else:
                return GraphQLError("Status could not be updated.")
        except:
            raise GraphQLError("Error Occured, please try again.")



class DeleteStatus(graphene.Mutation):
    class  Arguments:
        status_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info,status_id,**kwargs ):
        try:

            status_object = status.objects.get(status_id = status_id)
            status_object.delete()
            return UpdateStatus(success=True)

        except status.DoesNotExist:
            raise GraphQLError("Status not found!")






class Mutation(graphene.ObjectType):

    Create_Task = CreateTask.Field()
    Update_Task = UpdateTask.Field()
    Delete_Task = DeleteTask.Field()

    Create_Role = CreateRole.Field()
    Update_Role = UpdateRole.Field()

    Create_Project = CreateProject.Field()
    Update_Project = UpdateProject.Field()
    Delete_Project = DeleteProject.Field()



    # Create_Report = CreateReport.Field()
    Testing_Export_Excel = ExportExcel.Field()

    Create_Enrollment = CreateEnrollment.Field()
    Delete_Enrollment = DeleteEnrollment.Field()
    Create_Multiple_Tasks = BatchCreateTask.Field()


    Create_Project_Category = CreateCategory.Field()
    Update_Project_Category = UpdateCategory.Field()
    Delete_Project_Category = DeleteCategory.Field()


    Create_Status = CreateStatus.Field()
    Update_Status = UpdateStatus.Field()
    Delete_Status = DeleteStatus.Field()





