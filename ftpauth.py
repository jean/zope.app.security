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
"""FTP Standard Authentication adapter

$Id: ftpauth.py,v 1.2 2004/03/08 12:06:01 srichter Exp $
"""
from zope.publisher.interfaces.ftp import IFTPCredentials
from loginpassword import LoginPassword

class FTPAuth(LoginPassword):
    """Adapter for handling common FTP authentication.""" 
    __used_for__ = IFTPCredentials

    __request = None

    def __init__(self, request):
        self.__request = request
        lpw = request._authUserPW()
        if lpw is None:
            login, password = None, None
        else:
            login, password = lpw
        LoginPassword.__init__(self, login, password)

    def needLogin(self, realm):
        self.__request.unauthorized("Did not work")
