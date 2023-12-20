from hdfs import InsecureClient

HDFS_HOSTS: list[str] = [
    "http://simple-hdfs-namenode-default-0.simple-hdfs-namenode-default:8020",
    "http://simple-hdfs-namenode-default-1.simple-hdfs-namenode-default:8020",
]
HDFS_USER_NAME: str = "hdfs"


def get_hdfs_client() -> InsecureClient:
    return InsecureClient(";".join(HDFS_HOSTS), user=HDFS_USER_NAME)