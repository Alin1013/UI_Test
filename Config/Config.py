#基础配置，相关base_url以及配置目录的地址dir
import os

class Config:
    #基础的url地址，其余的页面在此基础上进行接口拼接
    Base_url="https://"

    #项目根目录的配置，如果不存在就自行创建
    root_dir=os.path.split(os.path.split(__file__))[0][0]
    test_cases_dir =os.path.join(root_dir,"TestCases")
    test_datas_dir =os.path.join(root_dir,"TestData")
    test_files_dir =os.path.join(root_dir,"TestFiles")
    #report,result,screenshots目录在同一级TestReports内
    test_reports_dir =os.path.join(root_dir,"TestReports","AllureReports")
    test_results_dir =os.path.join(root_dir,"TestReports","AllureResults")
    test_screenshots_dir =os.path.join(root_dir,"TestReports","Screenshots")
    logs =os.path.join(root_dir,"Logs")

    #权限认证目录
    auth_dir = os.path.join(root_dir,"Auth")
    #playwright框架中的浏览器的选择——chrome
    browser="chrome"

    @classmethod
    #上述目录如果不存在则创建
    def create_directories(cls):
        directories=[
            cls.test_cases_dir,
            cls.test_datas_dir,
            cls.test_reports_dir,
            cls.test_results_dir,
            cls.test_screenshots_dir,
            cls.logs,
            cls.auth_dir,
        ]
        for dir_path in directories:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path,exist_ok=True)

if __name__ == "__main__":
    Config.create_directories()
    print(Config.root_dir)
    print(Config.test_cases_dir)



