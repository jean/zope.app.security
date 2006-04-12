##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Permissions

$Id$
"""
from persistent import Persistent
from zope.interface import implements
from zope.location import Location
from zope.security.interfaces import IPermission

from zope.app.i18n import ZopeMessageFactory as _
NULL_ID = _('<permission not activated>')

##############################################################################
# BBB 2006/04/03 -- to be removed after 12 months

import zope.deferredimport
zope.deferredimport.deprecatedFrom(
    "It has been moved to zope.security.permission.  This reference "
    "will be gone in Zope 3.5", 'zope.security.permission',
    'Permission', 'checkPermission', 'allPermissions'
    )

##############################################################################

class LocalPermission(Persistent, Location):
    implements(IPermission)

    def __init__(self, title="", description=""):
        self.id = NULL_ID
        self.title = title
        self.description = description


def setIdOnActivation(permission, event):
    """Set the permission id upon registration activation.

    Let's see how this notifier can be used. First we need to create an event
    using the permission instance and a registration stub:

    >>> class Registration:
    ...     def __init__(self, obj, name):
    ...         self.component = obj
    ...         self.name = name

    >>> perm1 = LocalPermission('Permission 1', 'A first permission')
    >>> perm1.id
    u'<permission not activated>'
    
    >>> from zope.app.component import registration 
    >>> event = registration.RegistrationActivatedEvent(
    ...     Registration(perm1, 'perm1'))

    Now we pass the event into this function, and the id of the permission
    should be set to 'perm1'.

    >>> setIdOnActivation(perm1, event)
    >>> perm1.id
    'perm1'
    """
    permission.id = event.object.name


def unsetIdOnDeactivation(permission, event):
    """Unset the permission id up registration deactivation.

    Let's see how this notifier can be used. First we need to create an event
    using the permission instance and a registration stub:

    >>> class Registration:
    ...     def __init__(self, obj, name):
    ...         self.component = obj
    ...         self.name = name

    >>> perm1 = LocalPermission('Permission 1', 'A first permission')
    >>> perm1.id = 'perm1'

    >>> from zope.app.component import registration 
    >>> event = registration.RegistrationDeactivatedEvent(
    ...     Registration(perm1, 'perm1'))

    Now we pass the event into this function, and the id of the permission
    should be set to NULL_ID.

    >>> unsetIdOnDeactivation(perm1, event)
    >>> perm1.id
    u'<permission not activated>'
    """
    permission.id = NULL_ID
