#yaml文件的读取
import yaml,os
from Config.Config import Config

class ReadYaml(object):
    def __init__(self,filename):
        self.filename = filename

    #定义yaml读取方法
    def read(self):
        with open(self.filename,mode='r',encoding='utf-8')as file:
            data=file.read()

        data_yaml=yaml.load(data,Loader=yaml.FullLoader)
        for value in data_yaml:
            #从用例里面的url字段，拼接url地址（用例存储在yaml文件里面）
            if value.get("url地址") is not None:
                value["url地址"]=Config.url+value["url地址"]

            #如果有文件上传，则拼接文件上传的地址
            if value.get("file地址") is not None:
                value["file地址"]=Config.test_files_dir+value["file地址"]

        return data_yaml

if __name__=="__main__":
    pass