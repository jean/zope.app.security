##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Define Zope\'s default security policy

$Id: zopepolicy.py,v 1.11 2003/06/03 15:45:10 stevea Exp $
"""
__version__='$Revision: 1.11 $'[11:-2]

from zope.component import queryAdapter
from zope.context import ContainmentIterator

from zope.security.interfaces import ISecurityPolicy
from zope.security.management import system_user

from zope.app.interfaces.security import \
     IRolePermissionMap, IPrincipalPermissionMap, IPrincipalRoleMap
from zope.app.security.grants.principalpermission \
     import principalPermissionManager
from zope.app.security.grants.rolepermission import rolePermissionManager
from zope.app.security.grants.principalrole import principalRoleManager
from zope.app.security.settings import Allow, Deny
from zope.interface import implements

getPermissionsForPrincipal = \
                principalPermissionManager.getPermissionsForPrincipal
getPermissionsForRole = rolePermissionManager.getPermissionsForRole
getRolesForPrincipal = principalRoleManager.getRolesForPrincipal

globalContext = object()


class ZopeSecurityPolicy:

    implements(ISecurityPolicy)

    def __init__(self, ownerous=True, authenticated=True):
        """
            Two optional keyword arguments may be provided:

            ownerous -- Untrusted users can create code
                (e.g. Python scripts or templates),
                so check that code owners can access resources.
                The argument must have a truth value.
                The default is true.

            authenticated -- Allow access to resources based on the
                privileges of the authenticated user.
                The argument must have a truth value.
                The default is true.

                This (somewhat experimental) option can be set
                to false on sites that allow only public
                (unauthenticated) access. An anticipated
                scenario is a ZEO configuration in which some
                clients allow only public access and other
                clients allow full management.
        """

        self._ownerous = ownerous
        self._authenticated = authenticated

    def checkPermission(self, permission, object, context):
        # XXX We aren't really handling multiple principals yet

        # mapping from principal to set of roles
        user = context.user
        if user is system_user:
            return True

        roledict = {'Anonymous': Allow}
        principals = {user.getId() : roledict}

        role_permissions = {}
        remove = {}

        # Look for placeless grants first.

        # get placeless principal permissions
        for principal in principals:
            for principal_permission, setting in (
                getPermissionsForPrincipal(principal)):
                if principal_permission == permission:
                    if setting is Deny:
                        return False
                    assert setting is Allow
                    remove[principal] = True

        # Clean out removed principals
        if remove:
            for principal in remove:
                del principals[principal]
            if principals:
                # not done yet
                remove.clear()
            else:
                # we've eliminated all the principals
                return True

        # get placeless principal roles
        for principal in principals:
            roles = principals[principal]
            for role, setting in getRolesForPrincipal(principal):
                assert setting in (Allow, Deny)
                if role not in roles:
                    roles[role] = setting

        for perm, role, setting in (
            rolePermissionManager.getRolesAndPermissions()):
            assert setting in (Allow, Deny)
            if role not in role_permissions:
                role_permissions[role] = {perm: setting}
            else:
                if perm not in role_permissions[role]:
                    role_permissions[role][perm] = setting

        # Get principal permissions based on roles
        for principal in principals:
            roles = principals[principal]
            for role in roles:
                if role in role_permissions:
                    if permission in role_permissions[role]:
                        setting = role_permissions[role][permission]
                        if setting is Deny:
                            return False
                        remove[principal] = True


        # Clean out removed principals
        if remove:
            for principal in remove:
                del principals[principal]
            if principals:
                # not done yet
                remove.clear()
            else:
                # we've eliminated all the principals
                return True

        # Look for placeful grants
        for place in ContainmentIterator(object):

            # Copy specific principal permissions
            prinper = queryAdapter(place, IPrincipalPermissionMap)
            if prinper is not None:
                for principal in principals:
                    for principal_permission, setting in (
                        prinper.getPermissionsForPrincipal(principal)):
                        if principal_permission == permission:
                            if setting is Deny:
                                return False

                            assert setting is Allow
                            remove[principal] = True

            # Clean out removed principals
            if remove:
                for principal in remove:
                    del principals[principal]
                if principals:
                    # not done yet
                    remove.clear()
                else:
                    # we've eliminated all the principals
                    return True

            # Collect principal roles
            prinrole = queryAdapter(place, IPrincipalRoleMap)
            if prinrole is not None:
                for principal in principals:
                    roles = principals[principal]
                    for role, setting in (
                        prinrole.getRolesForPrincipal(principal)):
                        assert setting in (Allow, Deny)
                        if role not in roles:
                            roles[role] = setting

            # Collect role permissions
            roleper = queryAdapter(place, IRolePermissionMap)
            if roleper is not None:
                for perm, role, setting in roleper.getRolesAndPermissions():
                    assert setting in (Allow, Deny)
                    if role not in role_permissions:
                        role_permissions[role] = {perm: setting}
                    else:
                        if perm not in role_permissions[role]:
                            role_permissions[role][perm] = setting

            # Get principal permissions based on roles
            for principal in principals:
                roles = principals[principal]
                for role in roles:
                    if role in role_permissions:
                        if permission in role_permissions[role]:
                            setting = role_permissions[role][permission]
                            if setting is Deny:
                                return False
                            remove[principal] = True

            # Clean out removed principals
            if remove:
                for principal in remove:
                    del principals[principal]
                if principals:
                    # not done yet
                    remove.clear()
                else:
                    # we've eliminated all the principals
                    return True

        return False # deny by default


def permissionsOfPrincipal(principal, object):
    permissions = {}

    roles = {'Anonymous': Allow}
    role_permissions = {}
    principalid = principal.getId()

    # Make two passes.

    # First, collect what we know about the principal:


    # get placeless principal permissions
    for permission, setting in getPermissionsForPrincipal(principalid):
        if permission not in permissions:
            permissions[permission] = setting

    # get placeless principal roles
    for role, setting in getRolesForPrincipal(principalid):
        if role not in roles:
            roles[role] = setting

    # get placeful principal permissions and roles
    for place in ContainmentIterator(object):

        # Copy specific principal permissions
        prinper = queryAdapter(place, IPrincipalPermissionMap)
        if prinper is not None:
            for permission, setting in prinper.getPermissionsForPrincipal(
                principalid):
                if permission not in permissions:
                    permissions[permission] = setting

        # Collect principal roles
        prinrole = queryAdapter(place, IPrincipalRoleMap)
        if prinrole is not None:
            for role, setting in prinrole.getRolesForPrincipal(principalid):
                if role not in roles:
                    roles[role] = setting

    # Second, update permissions using principal

    for perm, role, setting in (
        rolePermissionManager.getRolesAndPermissions()):
        if role in roles and perm not in permissions:
            permissions[perm] = setting

    for place in ContainmentIterator(object):

        # Collect role permissions
        roleper = queryAdapter(place, IRolePermissionMap)
        if roleper is not None:
            for perm, role, setting in roleper.getRolesAndPermissions():
                if role in roles and perm not in permissions:
                    permissions[perm] = setting



    result = [permission
              for permission in permissions
              if permissions[permission] is Allow]

    return result

zopeSecurityPolicy=ZopeSecurityPolicy()
