from django.test import LiveServerTestCase
from django.core import management
from django.conf import settings

from core.models import Storage, Host
from core.tests.utils import storage_enabled, set_storage


class Storage_Test(LiveServerTestCase):
    """Basic Storage tests, for check model behavor."""
    @set_storage(extras=['host'])
    def setUp(self):
        pass

    def tearDown(self):
        Host.objects.all().delete()

    @storage_enabled()
    def test_proxy(self):
        """Connection to storage."""
        url = "%(protocol)s://%(address)s:%(port)i%(url_prefix)s/hosts" % self.storage.__dict__
        r = self.storage.proxy.open(url)
        self.assertEqual(r.code, 200, "Bad response code (%i)." % r.code)

    @storage_enabled()
    def test_get_hosts(self):
        """Retrieve hosts list."""
        hosts_dict = self.storage.get_hosts()
        self.assertIsInstance(hosts_dict, dict, "Invalide response type, should be dict.")

    @storage_enabled()
    def test_create_host_from_storage(self):
        """Create host in Db from datas."""
        self.storage.create_hosts()
        hosts = Host.objects.all()
        self.assertGreater(hosts.count(), 0, "No host was created.")

    @storage_enabled()
    def test_get_info(self):
        """Retrieve host info."""
        host = Host.objects.all()[0]
        r = self.storage.get_info(host.hostid)
        self.assertIsInstance(r, dict, "Invalide response type, should be dict.")

    @storage_enabled()
    def test_get_categories(self):
        """Retrieve host categories."""
        host = Host.objects.all()[0]
        r = self.storage.get_categories(host.hostid)
        self.assertIsInstance(r, list, "Invalide response type, should be list.")

    @storage_enabled()
    def test_get_plugins(self):
        """Retrieve all host plugins."""
        host = Host.objects.all()[0]
        r = self.storage.get_plugins(host.hostid)
        # self.assertIsInstance(r, list, "Invalide response type, should be list.")

    @storage_enabled()
    def test_get_plugins_by_category(self):
        """Retrieve plugins only for a category."""
        host = Host.objects.all()[0]
        category = self.storage.get_categories(host.hostid)[0]
        r = self.storage.get_plugins_by_category(host.hostid, category)
        self.assertIsInstance(r, list, "Invalide response type, should be list.")

    @storage_enabled()
    def test_get_plugins_data_sources(self):
        """Retrieve data sources a plugin."""
        host = Host.objects.all()[0]
        plugin = self.storage.get_plugins(host.hostid)[0]['Plugin']
        r = self.storage.get_plugin_data_sources(host.hostid, plugin)
        self.assertIsInstance(r, list, "Invalide response type, should be list.")

    @storage_enabled()
    def test_get_data(self):
        """Retrieve data sources a plugin."""
        host = Host.objects.all()[0]
        plugin = self.storage.get_plugins(host.hostid)[0]['Plugin']
        source = self.storage.get_plugin_data_sources(host.hostid, plugin)[0]
        data = {'hostid':host.hostid, 'plugin':plugin, 'ds':source, 'res':'Daily'}
        r = self.storage.get_data(**data)
        self.assertIsInstance(r, dict, "Invalide response type, should be dict.")

    @storage_enabled()
    def test_get_unsaved_hosts(self):
        """Find not referenced hosts."""
        self.storage.create_hosts()
        # Del an host and find it
        Host.objects.all()[0].delete()
        unsaved_hosts = self.storage._get_unsaved_hosts()
        self.assertEqual(len(unsaved_hosts), 1, "Supposed to have 1 unsaved host (%i)" % len(unsaved_hosts))

    @storage_enabled()
    def test_get_saved_hosts(self):
        """Find referenced host"zzs."""
        initial_count = Host.objects.count()
        # Create an host and find it
        Host.objects.create(name='test', hostid='testid', storage=self.storage)
        unfoundable_hosts = self.storage._get_unfoundable_hostids()
        self.assertEqual(len(unfoundable_hosts), 1, "Supposed to have 1 unfoundable host (%i)" % len(unfoundable_hosts))


class Storage_Manager_Test(LiveServerTestCase):

    @set_storage()
    def setUp(self):
        if Storage.objects.count() < 2:
            self.skipTest('Need storages to launch this test.')
        self.storage1, self.storage2 = Storage.objects.all()[:2]

    def tearDown(self):
        Host.objects.all().delete()

    def test_unsaved_hosts(self):
        """Find not referenced hosts."""
        self.storage1.create_hosts()
        # Test to find storage2's hosts
        unsaved_hosts = Storage.objects.get_unsaved_hostids()
        hosts = self.storage2.get_hosts().keys()
        self.assertEqual(len(unsaved_hosts), len(hosts), "Missing host number not match.")
        # Test to del hosts and find them
        [ h.delete() for h in Host.objects.all()[0:5] ]
        unsaved_hosts = Storage.objects.get_unsaved_hostids()
        self.assertEqual(len(unsaved_hosts), len(hosts)+5, "Missing host number not match.")

    def test_find_host(self):
        """Find which storage has an host."""
        self.storage1.create_hosts()
        host = Host.objects.all()[0]
        # Test to find an host
        whereisit = Storage.objects.which_storage(host.hostid)
        self.assertEqual(self.storage1, whereisit, "Host not found on its storage.") 
        # Test to find host which badly referenced
        host.storage = self.storage2
        host.save()
        whereisit = Storage.objects.which_storage(host.hostid)
        self.assertEqual(self.storage1, whereisit, "Host not found when on bad storage.") 
        # Test to find a false hostID
        host.hostid = 'False test ID'
        host.save()
        whereisit = Storage.objects.which_storage(host.hostid)
        self.assertIsNone(whereisit, "False host found on a storage.") 

    def test_repair_hosts(self):
        """Fix Host/Storage bad links."""
        # Set all storage1's hosts bad
        self.storage1.create_hosts()
        Host.objects.all().update(storage=self.storage2)

        # Get the crap and test it
        bad_hosts = Storage.objects.get_bad_referenced_hostids()
        self.assertEqual(len(bad_hosts), Host.objects.count())

        # Repair and test
        Storage.objects.repair_hosts()
        bad_hosts = Storage.objects.get_bad_referenced_hostids()
        self.assertEqual(len(bad_hosts), 0, "There are always bad referenced %i host(s)." % len(bad_hosts))
