# quickstart.schema.py

import graphene
import CRUD_BACKEND.mutations as mutation
import CRUD_BACKEND.query as query
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):

    register = mutations.Register.Field()
    swap_emails = mutations.SwapEmails.Field()
    verify_account = mutations.VerifyAccount.Field()
    password_reset = mutations.PasswordReset.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()


    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()



class Query(query.Query, UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(mutation.Mutation, AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)