import argparse
import queue
from braingeneers.iot.messaging import MessageBroker
import braingeneers.utils.smart_open_braingeneers as smart_open
from braingeneers.utils import common_utils
import yaml
import braingeneers.utils.s3wrangler as wr
from stream_zip import stream_zip, ZIP_64


# todo document this 1) MD file 2) config file usage 3) arch diagram 4) cron job config
# todo add new trello task to add lifecycle management web page


QUEUE_NAME_LIST = 'service-s3-glacier-backup-list'
QUEUE_NAME_TASK = 'service-s3-glacier-backup-task'
QUEUE_NAME_LAST_MODIFIED = 'service-s3-glacier-backup-last-modified'
STATE_FILE_PATH = 's3://braingeneers/services/s3-glacier-backup/s3-glacier-backup-state.yaml'

TASK_LIST = 'LIST',
TASK_LIST_DONE = 'LIST_DONE',
TASK_BACKUP_PREFIX = 'BACKUP_PREFIX',
TASK_END = 'END'
TASK_WRITE_STATE = 'TASK_WRITE_STATE'

# BACKUP_BUCKET = 'braingeneers-backups'
# AWS_ENDPOINT = 's3.us-west-1.amazonaws.com'

BACKUP_BUCKET = 'braingeneersdev'
AWS_ENDPOINT = 'https://s3-west.nrp-nautilus.io'


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Performs backup of PRP/S3 to Glacier.'
    )
    parser.add_argument(
        '--init', type=bool, action='store_true', default=False,
        help='Initializes the process, this must be called before workers start.'
    )

    return vars(parser.parse_args())


def read_state_file():
    # read state file
    with smart_open.open(STATE_FILE_PATH, 'r') as f:
        return yaml.safe_load(f)


def init():
    """ This function must be called before the workers start """
    # get queue & read state file
    mb = MessageBroker()
    # delete previous iterations of the queue
    mb.delete_queue(QUEUE_NAME_LIST)
    mb.delete_queue(QUEUE_NAME_TASK)
    mb.delete_queue(QUEUE_NAME_LAST_MODIFIED)
    list_queue = mb.get_queue(QUEUE_NAME_LIST)
    state = read_state_file()

    # seed queue with state file prefixes
    for prefix in state['backup_prefixes']:
        list_queue.put((TASK_LIST, prefix))


def main():
    """ Iterates the queue(s) for tasks and processes them. """
    # get queue & read state file
    mb = MessageBroker()
    list_queue = mb.get_queue(QUEUE_NAME_LIST)  # filled with top level S3 prefixes to be converted to UUIDs
    task_queue = mb.get_queue(QUEUE_NAME_TASK)  # filled with UUIDs to check and backup if appropriate
    last_modified_queue = mb.get_queue(QUEUE_NAME_LAST_MODIFIED)  # collects last modified hash values for a single-writer to save at the end of the job
    state = read_state_file()  # yaml configuration file containing prefixes to scan and last modified hash values

    # loop over list_queue until empty
    try:
        while task := list_queue.get(block=False):
            prefixes = list_prefix(task[1])
            for prefix in prefixes:
                task_queue.put(prefix)
            list_queue.task_done()
            task_queue.put((TASK_LIST_DONE,))
    except queue.Empty:
        pass  # when the list queue is empty then we've completed this portion successfully

    # loop: pull backup tasks from the queue until END received
    while task := task_queue.get():
        if task[0] == TASK_LIST_DONE:
            # Once a LIST_DONE token is reached wait for all list operations to finish
            task_queue.put((TASK_LIST_DONE,))
            list_queue.join()
            # at this point all list operations are complete the last task is to write the state file (by one worker)
            task_queue.put((TASK_WRITE_STATE,))
            task_queue.put((TASK_END,))

        elif task[0] == TASK_WRITE_STATE:
            task_queue.join()  # wait for all tasks to complete
            save_state_file(state, last_modified_queue)

        elif task[0] == TASK_BACKUP_PREFIX:
            prefix = task[1]
            new_hash = backup_prefix(task[1], state.get(prefix, None))
            last_modified_queue.put((prefix, new_hash))

        elif task[0] == TASK_END:
            q.put((TASK_END,))  # replace end token for other workers
            break  # exit successfully

        else:
            raise ValueError(f'Bug condition: {task[0]} is not a valid task token.')


def save_state_file(state: dict, last_modified_queue: MessageBroker.NamedQueue):
    """ One-time write of the updated state file, this will be run by one and only one worker. """
    last_modified_hash = {}
    while not last_modified_queue.empty():
        prefix, md5_hash = last_modified_queue.get()
        last_modified_hash[prefix] = md5_hash
    state['last_modified_hash'] = last_modified_hash
    with smart_open.open(STATE_FILE_PATH, 'w') as f:
        yaml.dump(state, f)


def list_prefix(prefix: str):
    """ List all directories at the given prefix, e.g. a list of UUIDs. """
    return wr.list_directories(prefix)


def backup_prefix(prefix: str, last_modified_hash: str) -> str:
    """
    1) Lists all files and last timestamps at {prefix}.
    2) Sorts the list and excludes NOBACKUP token prefixes
    3) Generates MD5 hash of the list.
    4) Compares the MD5 hash to the last_modified_hash
    5) If no changes return the last_modified_hash
    6) If changes backup to AWS/S3/Glacier and return new MD5 hash

    :param prefix: s3 prefix to back up
    :param last_modified_hash: MD5 hash of last state
    :return: MD5 hash, same form as last_modified_hash for tracking changes
    """
    # List all objects under the prefix
    object_list = common_utils.file_list(prefix)  # produces [(file, last-modified, size), ...]
    nobackup_prefixes = [(o[0].split('NOBACKUP')[0], o[1]) for o in object_list if 'NOBACKUP' in o]  # produces [(file, last-modified), ...]
    # Exclude suffixes under a NOBACKUP empty-file
    filtered_list = sorted([
        o for o in object_list
        if not any([o[0].startswith(exclude) for exclude in nobackup_prefixes])
    ])
    # Generate an MD5 hash of the file list, size and last modified hash
    m = hashlib.md5()
    for o in filtered_list:
        m.update(bytes('-'.join(o), 'utf-8'))
    new_last_modified_hash = m.hexdigest()

    # Download the file from PRP/S3 and stream (zipped) to AWS/S3 in 1 MB chunks
    if new_last_modified_hash != last_modified_hash:
        path_prefix = urllib.parse(prefix).path
        braingeneers.set_default_endpoint(AWS_ENDPOINT)
        with smart_open.open(f's3://{BACKUP_BUCKET}/{path_prefix}.zip', 'wb') as f_out:
            zipped_chunks = stream_zip(path_prefix, member_files_iterator(filtered_list))
            for zipped_chunk in zipped_chunks:
                f_out.write(zipped_chunk)

    return new_last_modified_hash


def member_files_iterator(file_and_last_modified_tuple: str, filepaths: str):
    """ Iterator yields each file to be added to the zip. """
    for (file, last_modified) in file_and_last_modified_tuple:
        yield file, last_modified, 0o600, ZIP_64, download_iterator(file)


def download_iterator(path: str):
    """ Iterator yields the file bytes. """
    with smart_open.open(path, 'rb') as f:
        yield f.read(2**20)


if __name__ == '__main__':
    args = arg_parser()
    if args['init'] is True:
        init()
    else:
        main()
