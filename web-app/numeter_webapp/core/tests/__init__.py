from login import Login_TestCase
from perms import Perms_TestCase
from storage import Storage_TestCase, Storage_Manager_TestCase
from host import Host_TestCase
from plugin import Plugin_Manager_TestCase, Plugin_TestCase
from source import Data_Source_Manager_TestCase, Data_Source_TestCase
from browsing import Index_TestCase
from management import Manage_User_TestCase, Manage_Storage_TestCase, Manage_Repair_TestCase
from hosttree import Hosttree_TestCase
from group_restriction import Access_TestCase
from mediafield import MediaField_TestCase

def suite():
    import unittest
    TEST_CASES = (
        'core.tests.management',
        'core.tests.perms',
        'core.tests.mediafield',
        'core.tests.login',
        'core.tests.group_restriction',
        'core.tests.browsing',
        'core.tests.hosttree',
        'core.tests.storage',
        'core.tests.host',
        'core.tests.plugin',
        'core.tests.source',
    )
    suite = unittest.TestSuite()
    for t in TEST_CASES:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(__import__(t, globals(), locals(), fromlist=["*"])))
    return suite