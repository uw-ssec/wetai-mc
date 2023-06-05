import tempfile
import unittest
import s3_glacier_backup
from braingeneers.iot.messaging import MessageBroker
import yaml
import tempfile
import os


class TestS3GlacierBackup(unittest.TestCase):
    def setUp(self) -> None:
        self.state_file_path = '/tmp/unittest/root-folder-to-backup'
        state_file_yaml = f'backup_prefixes:\n' \
                          f' - {self.state_file_path}\n'

        s3_glacier_backup.QUEUE_NAME_LIST = 'unittest-service-s3-glacier-backup-list'
        s3_glacier_backup.QUEUE_NAME_TASK = 'unittest-service-s3-glacier-backup-task'
        s3_glacier_backup.QUEUE_NAME_LAST_MODIFIED = 'unittest-service-s3-glacier-backup-last-modified'
        self.state_file = tempfile.NamedTemporaryFile()
        self.state_file.write(state_file_yaml.encode('utf-8'))
        self.state_file.flush()
        s3_glacier_backup.STATE_FILE_PATH = self.state_file.name
        self.mb = MessageBroker()

    def tearDown(self) -> None:
        self.state_file.close()

    def test_init(self):
        s3_glacier_backup.init()
        q = self.mb.get_queue(s3_glacier_backup.QUEUE_NAME_LIST)
        self.assertEqual(self.state_file_path, q.get()[1])

    def test_main_loop(self):
        self.fail()  # todo

    def test_list_prefix(self):
        self.fail()  # todo

    def test_backup_prefix(self):
        self.fail()  # todo
