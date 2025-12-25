#设置内置库，对相关操作进行替换
#设置全局环境变量进行使用
from inspect import Parameter
import random,time,re

class BuildinLibrary():
    #存放全局变量
    global_parameter ={}
        #设置全局变量
    def set_global_parameter(self,key,value):
        #将value的值存放到key中
        #提取key值
        parameter_key=re.fullmatch(r'{{(\w+)}}',key).group(1)
        #保存参数
        self.global_parameter[parameter_key]=value
        return self.global_parameter.get(parameter_key)

        #获取全局变量
    def get_global_parameter(self,key):
        #设置时间戳
        self.global_parameter['timestamp']=str(int(time.time()*1000))
        self.global_parameter['timetime']=str(int(time.time()))
        self.global_parameter['random_phone']="1"+\
                                                str(random.randint(3,9))+\
                                                str(random.randint(0,9))+\
                                                time.strftime("%d%H%M%S")
        return self.global_parameter.get(key)

        #替换全局变量
    def replace_parameter(self,text):
        parameter_key=re.findall(r'{{\$(\w+)}}',text)
        for param in parameter_key:
            value =self.get_global_parameter(param)
            to=rf"{value}"
            text=re.sub(rf'{{{{\${param}}}}}',lambda m:to,text)
        return text


if __name__=='__main__':
    bl=BuildinLibrary()
    bl.set_global_parameter("{{username}}","admin")
    bl.set_global_parameter("{{password}}","admin@")
    username=bl.get_global_parameter("username")
    password=bl.get_global_parameter("password")
    text="{{$username}}+{{$password}}+{{$timetime}}"
    t=bl.replace_parameter(text)
    print(t)





