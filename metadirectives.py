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
"""securityPolicy Directive Schema

$Id: metadirectives.py,v 1.2 2004/03/08 12:06:41 srichter Exp $
"""
from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Tokens, PythonIdentifier
from zope.configuration.fields import MessageID
from zope.schema import InterfaceField, Id, TextLine

class ISecurityPolicyDirective(Interface):
    """Defines the security policy that will be used for Zope."""

    component = GlobalObject(
        title=u"Component",
        description=u"Pointer to the object that will handle the security.",
        required=True)


class IModule(Interface):
    """Group security declarations about a module"""

    module = GlobalObject(
        title=u"Module",
        description=u"Pointer to the module object.",
        required=True)


class IAllow(Interface):
    """Allow access to selected module attributes

    Access is unconditionally allowed to any names provided directly
    in the attributes attribute or to any names defined by
    interfaces listed in the interface attribute.
    """

    attributes = Tokens(
        title=u"Attributes",
        description=u"The attributes to provide access to.",
        value_type = PythonIdentifier(),
        required=False)

    interface = Tokens(
        title=u"Interface",
        description=u"Interfaces whos names to provide access to. Access "
                    u"will be provided to all of the names defined by the "
                    u"interface(s). Multiple interfaces can be supplied.",
        value_type = GlobalObject(value_type=InterfaceField()),
        required=False)


class IRequire(Interface):
    """Require a permission to access selected module attributes

    The given permission is required to access any names provided
    directly in the attributes attribute or any names defined by
    interfaces listed in the interface attribute.  
    """
    
    permission = Id(
        title=u"Permission ID",
        description=u"The id of the permission to require.")


class IBaseDefineDirective(Interface):
    """Define a new security object."""
    
    id = Id(
        title=u"Id",
        description=u"Id as which this object will be known and used.",
        required=True)

    title = MessageID(
        title=u"Title",
        description=u"Provides a title for the object.",
        required=True)

    description = MessageID(
        title=u"Description",
        description=u"Provides a description for the object.",
        required=False)


class IDefinePermissionDirective(IBaseDefineDirective):
    """Define a new permission."""

class IBasePrincipalDirective(Interface):
    """Base interface for principal definition directives."""
    
    id = Id(
        title=u"Id",
        description=u"Id as which this object will be known and used.",
        required=True)

    title = TextLine(
        title=u"Title",
        description=u"Provides a title for the object.",
        required=True)

    description = TextLine(
        title=u"Title",
        description=u"Provides a description for the object.",
        required=False)

class IDefinePrincipalDirective(IBasePrincipalDirective):
    """Define a new principal."""

    login = TextLine(
        title=u"Username/Login",
        description=u"Specifies the Principal's Username/Login.",
        required=True)

    password = TextLine(
        title=u"Password",
        description=u"Specifies the Principal's Password.",
        required=True)


class IDefineUnauthenticatedPrincipalDirective(IBasePrincipalDirective):
    """Define a new unauthenticated principal."""
