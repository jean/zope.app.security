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
"""Principals.

$Id$
"""
from zope.app import zapi
from zope.app.security.interfaces import PrincipalLookupError
from zope.app.security.interfaces import IAuthentication

# BBB Backward Compatibility
from zope.exceptions import NotFoundError
import warnings

def checkPrincipal(context, principal_id):

    auth = zapi.getUtility(IAuthentication, context=context)
    try:
        if auth.getPrincipal(principal_id):
            return
    except PrincipalLookupError:
        pass
    except NotFoundError: # BBB Backward Compatibility
        warnings.warn(
            "A %s instance raised a NotFoundError in "
            "getPrincipals.  Raising NotFoundError in this "
            "method is deprecated and will no-longer be supported "
            "staring in ZopeX3 3.3.  PrincipalLookupError should "
            "be raised instead."
            % auth.__class__.__name__,
            DeprecationWarning)
    
    raise ValueError("Undefined principal id", principal_id)
