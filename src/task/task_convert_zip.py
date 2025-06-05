import os

from task.task_convert import TaskConvertBase
from tools.log import Log
from tools.str import Str
import zipfile


class TaskConvertZip(TaskConvertBase):
    def __init__(self) -> None:
        TaskConvertBase.__init__(self)

    def start(self):
        try:
            zip_filename = os.path.join(self.to_path, self.fileName) + ".zip"
            Log.Info("add convert zip, name={}, in_path={}, to_path={}".format(zip_filename, self.in_path, self.to_path))
            zip_mode = 'w'
            zip_file = zipfile.ZipFile(zip_filename, zip_mode)
            for root, dirs, files in os.walk(self.in_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path)
            zip_file.close()
            return Str.Ok
        except Exception as es:
            Log.Error(es)
            return Str.Error
