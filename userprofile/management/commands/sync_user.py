import ldap

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User

from oaprofile.ldaphelper import get_ldap_con, LDAPSearchExt
from oaprofile.models import UserProfile 


class Command(BaseCommand):
    help = "Sync User & UserProfile"
    
    def handle(self, **options):
        users = User.objects.all()
        for user in users:
            try:
                user.get_profile()#if no profile, create it.
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
        con = get_ldap_con()
        search = settings.AUTH_LDAP_USER_BASE_SEARCH
        try:
            users = search.execute(con, attrs = ['cn', 'cnName', 'mail', 'mobile'])
            print "ldap user count:", len(users)
        finally:
            con.unbind()

        users = [u[1] for u in users]
        for u in users:
            user, created = User.objects.get_or_create(username=u['cn'][0])
            if created:
                print "create user:", user.username
            try:
                user.get_profile()#if no profile, create it.
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
            userprofile = user.get_profile()
            try:
                user.email = u['mail'][0]
                user.save()
            except:
                pass
            try:
                userprofile.cnName = u['cnName'][0]
                userprofile.mobile = u['mobile'][0]
                userprofile.save()
            except:
                pass
