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
"""

$Id: rolepermission.py,v 1.3 2003/06/07 05:46:03 stevea Exp $
"""
from zope.component import getAdapter
from zope.interface import implements

from zope.app.interfaces.annotation import IAnnotations
from zope.app.interfaces.security import IRolePermissionMap
from zope.app.interfaces.security import IRolePermissionManager
from zope.app.interfaces.security import IRole

from zope.app.security.settings import Allow, Deny, Unset
from zope.app.security.role import checkRole
from zope.app.security.permission import checkPermission
from zope.app.security.grants.securitymap import PersistentSecurityMap
from zope.app.security.grants.securitymap import SecurityMap

annotation_key = 'zope.app.security.AnnotationRolePermissionManager'

class AnnotationRolePermissionManager:
    """
    provide adapter that manages role permission data in an object attribute
    """

    implements(IRolePermissionManager, IRolePermissionMap)

    def __init__(self, context):
        self._context = context

    def grantPermissionToRole(self, permission_id, role_id):
        ''' See the interface IRolePermissionManager '''
        rp = self._getRolePermissions(create=1)
        rp.addCell(permission_id, role_id, Allow)
        # probably not needed, as annotations should manage
        # their own persistence
        #self._context._p_changed = 1

    def denyPermissionToRole(self, permission_id, role_id):
        ''' See the interface IRolePermissionManager '''
        rp = self._getRolePermissions(create=1)
        rp.addCell(permission_id, role_id, Deny)
        # probably not needed, as annotations should manage
        # their own persistence
        #self._context._p_changed = 1

    def unsetPermissionFromRole(self, permission_id, role_id):
        ''' See the interface IRolePermissionManager '''
        rp = self._getRolePermissions()
        # Only unset if there is a security map, otherwise, we're done
        if rp:
            rp.delCell(permission_id, role_id)
            # probably not needed, as annotations should manage
            # their own persistence
            #self._context._p_changed = 1

    def getRolesForPermission(self, permission_id):
        '''See interface IRolePermissionMap'''
        rp = self._getRolePermissions()
        if rp:
            return rp.getRow(permission_id)
        else:
            return []

    def getPermissionsForRole(self, role_id):
        '''See interface IRolePermissionMap'''
        rp = self._getRolePermissions()
        if rp:
            return rp.getCol(role_id)
        else:
            return []

    def getRolesAndPermissions(self):
        '''See interface IRolePermissionMap'''
        rp = self._getRolePermissions()
        if rp:
            return rp.getAllCells()
        else:
            return []

    def getSetting(self, permission_id, role_id):
        '''See interface IRolePermissionMap'''
        rp = self._getRolePermissions()
        if rp:
            return rp.getCell(permission_id, role_id)
        else:
            return Unset

    def _getRolePermissions(self, create=0):
        """Get the role permission map stored in the context, optionally
           creating one if necessary"""
        # need to remove security proxies here, otherwise we enter
        # an infinite loop, becuase checking security depends on
        # getting RolePermissions.
        from zope.proxy import removeAllProxies
        context = removeAllProxies(self._context)
        annotations = getAdapter(context, IAnnotations)
        try:
            return annotations[annotation_key]
        except KeyError:
            if create:
                rp = annotations[annotation_key] = PersistentSecurityMap()
                return rp
        return None

class RolePermissions:

    implements(IRole)

    def __init__(self, role, context, permissions):
        self._role = role
        self._context = context
        self._permissions = permissions

    def getId(self):
        return self._role.getId()

    def getTitle(self):
        return self._role.getTitle()

    def getDescription(self):
        return self._role.getDescription()

    def permissionsInfo(self):
        prm = getAdapter(self._context, IRolePermissionManager)
        rperms = prm.getPermissionsForRole(self._role.getId())
        settings = {}
        for permission, setting in rperms:
            settings[permission] = setting.getName()
        nosetting = Unset.getName()
        return [{'id': permission.getId(),
                 'title': permission.getTitle(),
                 'setting': settings.get(permission.getId(), nosetting)}
                for permission in self._permissions]


class RolePermissionManager(SecurityMap):
    """Mappings between roles and permissions."""

    implements(IRolePermissionManager)

    def grantPermissionToRole(self, permission_id, role_id, check=True):
        '''See interface IRolePermissionMap'''

        if check:
            checkRole(None, role_id)
            checkPermission(None, permission_id)
        
        self.addCell(permission_id, role_id, Allow)

    def denyPermissionToRole(self, permission_id, role_id, check=True):
        '''See interface IRolePermissionMap'''

        if check:
            checkRole(None, role_id)
            checkPermission(None, permission_id)
        
        self.addCell(permission_id, role_id, Deny)

    def unsetPermissionFromRole(self, permission_id, role_id):
        '''See interface IRolePermissionMap'''

        # Don't check validity intentionally.
        # After all, we certianly want to unset invalid ids.
        
        self.delCell(permission_id, role_id)

    def getRolesForPermission(self, permission_id):
        '''See interface IRolePermissionMap'''
        return self.getRow(permission_id)

    def getPermissionsForRole(self, role_id):
        '''See interface IRolePermissionMap'''
        return self.getCol(role_id)

    def getSetting(self, permission_id, role_id):
        '''See interface IRolePermissionMap'''
        return self.getCell(permission_id, role_id)

    def getRolesAndPermissions(self):
        '''See interface IRolePermissionMap'''
        return self.getAllCells()

# Permissions are our rows, and roles are our columns
rolePermissionManager = RolePermissionManager()

# Register our cleanup with Testing.CleanUp to make writing unit tests simpler.
from zope.testing.cleanup import addCleanUp
addCleanUp(rolePermissionManager._clear)
del addCleanUp
