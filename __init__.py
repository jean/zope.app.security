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
"""Zope Application-specific Security code

$Id$
"""
# Register some standard types
import _protections
_protections.protect()
del _protections


class LogoutSupported:
    """A class that can be registered as an adapter to flag logout support."""

    from zope.component import adapts
    from zope.interface import implements, Interface
    from zope.app.security.interfaces import ILogoutSupported

    adapts(Interface)    
    implements(ILogoutSupported)

    def __init__(self, dummy):
        pass
