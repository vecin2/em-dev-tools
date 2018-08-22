import pytest
import os


def test_creates_update_sequence(tmpdir):

    #sql_module = SqlModule("GSCCoreEntities")
    #sql_module.add(SqlTask("override_search"))

    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1

def test_image_file(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_create_normal_file(fs):
    f = open("gurufs.txt", "w+")
    
def test_create_normal_file():
    f = open("guru.txt", "w+")

def test_sql_module():
    sql_module = SqlModule("test_dir")
    sql_module.create()
    assert os.path.exists("test_dir")

def test_sql_module(fs):
    sql_module = SqlModule("test_dir_fs")
    sql_module.create()
    assert os.path.exists("test_dir_fs")

class SqlModule(object):
    def __init__(self,name):
        self.name =name

    def create(self):
        os.makedirs(self.name)

class SqlTask(object):
    def __init__(self,name):
        self.name =name


class EMProject(object):
    def add_sql_task(self, sql_task):
        2 = 2
