# -*- coding: utf-8 -*-
import odoorpc
HOST = 'localhost'
PORT = 8069
DB = 'odoo-test'
USER = 'sebastian.hernandez@benandfrank.com'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# Prepare connection
ODOO = odoorpc.ODOO('localhost', port=8069)

# Check available databases
print(ODOO.db.list())

# Login
ODOO.login(DB, USER, PASS)

# Current USER
USER = ODOO.env.USER
print(USER.name)
print(USER.company_id.name)

# Simple raw query
USER_DATA = ODOO.execute('res.USERs', 'read', [USER.id])
print(USER_DATA)

# Use all methos of a model
if 'openacademy.course' in ODOO.env:
    COURSE = ODOO.env['openacademy.course']
    COURSE_IDS = COURSE.search([])
    print(COURSE_IDS)
    for course in COURSE.browse(COURSE_IDS):
        course.name = course.name + ' D'
        print(course.name)
