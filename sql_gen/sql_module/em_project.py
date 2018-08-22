import os

class EMProject(object):
    def __init__(self):
        self.core_home = os.environ['EM_CORE_HOME']

    @staticmethod
    def core_home():
        return os.environ['EM_CORE_HOME']

    def write_sql_task(self, sql_task):
        self.name = sql_task

class SQLTask(object):

    @staticmethod
    def make():
        sql_task = SQLTask()
        return sql_task
    
    def path(self, task_path):
        self.task_path = task_path
        return self

    def with_table_data(self, table_data):
        self.table_data = table_data
        return self

    def write(self):
        print("writing to disk sql_task under: "+ self.__get_full_path())
        table_data_path = os.path.join(self.__get_full_path(), "tableData.sql")
        if not os.path.exists(self.__get_full_path()):
                os.makedirs(self.__get_full_path())
        f = open(table_data_path, "w+")
        f.write(self.table_data)
        f.close()

    def __get_full_path(self):
        return os.path.join(EMProject.core_home(), self.task_path)
