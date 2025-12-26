#allure页面美化
import os.path, allure, pytest, functools
from Config.Config import Config

class AllurePretty(object):
    @classmethod
    def AllurePretty(cls,page,CaseData):
        allure.dynamic.feature(CaseData.get("模块"))
        allure.dynamic.story(CaseData.get("功能"))
        allure.dynamic.severity(CaseData.get("优先级"))
        allure.dynamic.title(f'{CaseData.get("用例编号")}_{CaseData.get("用例标题")}')
        if CaseData.get("是否执行") != "Y":
            allure.dynamic.description("用例指定跳过")
            pytest.skip("用例指定跳过")

    @classmethod
    def AllurePretty_Screenshot(cls,page,CaseData):
        filename=os.path.join(Config.test_screenshots_dir,f"{CaseData.get('用例标题')}.png")
        page.screenshot(path=filename)
        allure.attach.file(source=filename,name=CaseData.get('用例标题'),attachment_type=allure.attachment_type.PNG)

    @classmethod
    def AllurePretty_Warpper(cls,func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            #获取page对象（支持page和logged_in_page两种参数名）
            page_obj = kwargs.get("page") or kwargs.get("logged_in_page")
            #获取casedata
            cls.AllurePretty(page=page_obj,CaseData=kwargs.get("CaseData"))
            #运行测试用例
            r=func(*args,**kwargs)
            #添加截图
            cls.AllurePretty_Screenshot(page=page_obj,CaseData=kwargs.get("CaseData"))
            return r
        return inner

if __name__=='__main__':
    pass