import pytest
import os
from sql_module.em_project import SQLTask, EMProject


def test_creates_update_sequence(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1

def test_image_file(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_create_sql_task(fs):
    sql_task_path ="/modules/CoreEntiy/rewire_search"
    sql_task = SQLTask.make().path(sql_task_path).with_table_data("some data");
    #sql_task.set_ouput()
    sql_task.write()
    
    final_path = os.path.join(EMProject.core_home(), sql_task_path)
    final_path = os.path.join(final_path, "tableData.sql")
    assert os.path.exists(final_path)
    file = open(final_path,"r")
    file_content = file.read()
    print "hola file content is ", file_content
    assert "some data" == file_content

