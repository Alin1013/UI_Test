#封装页面基础元素
import os
from playwright.sync_api import expect, Page
from selenium.common.exceptions import TimeoutException

from BuildinLibrary.BuildinLibrary import BuildinLibrary
from Config.Config import Config

class BasePage:
    def __init__(self, page:Page):
        self.page = page

        #获取网页地址
    def goto_url(self,url):
        self.page.goto(url,wait_until="domcontentloaded",timeout=60000)

        #关闭浏览器
    def quit_browser(self) ->None:
        self.page.quit()

        #点击元素(将frame框架和普通框架的封装在一起，就不用进行后续判断）
    def click(self,locator,fram_locator=None):
        try:
            if fram_locator is not None:
                self.page.frame_locator(fram_locator).locator(locator).click()
            else:
                self.page.click(locator)
        except Exception as e:
            print(e)

        #悬浮操作
    def hover(self,locator,fram_locator=None):
        try:
            if fram_locator is not None:
                self.page.frame_locator(fram_locator).locator(locator).hover()
            else:
                self.page.hover(locator)
        except Exception as e:
            print(e)

            #填充值操作
    def fill(self,locator,value,fram_locator=None):
        value=BuildinLibrary().replace_parameter(value)
        try:
            if fram_locator is not None:
                self.page.frame_locator(selector=fram_locator).locator(selector_or_locator=locator).fill(value)
            else:
                self.page.fill(selector=locator,value=value)
        except Exception as e:
            print(e)

            #键值操作
    def type(self,locator,value,fram_locator=None):
        value=BuildinLibrary().replace_parameter(value)
        try:
            if fram_locator is not None:
                self.page.frame_locator(selector=fram_locator).locator(selector_or_locator=locator).type(value)
            else:
                self.page.type(selector=locator,text=value,delay=100)
        except Exception as e:
            print(e)

            #文件上传操作
    def file(self,locator,files,fram_locator=None):
        try:
            if fram_locator is not None:
                self.page.frame_locator(fram_locator).locator(locator).set_input_files(files=files)
            else:
                self.page.locator(locator).set_input_files(files=files)
        except Exception as e:
            print(e)

            #断言操作—元素可见
    def ele_to_be_visible(self,locator):
        return expect(self.page.locator(locator)).to_be_visible()

            #强制等待—元素可见
    def ele_to_be_visible_force(self,locator,frame_locator=None,timeout: int=5):
        ele=None
        if frame_locator is not None:
            ele=self.page.frame_locator(frame_locator).locator(locator)
        else:
            ele=self.page.locator(locator)
        for t in range(0,timeout):
            self.page.wait_for_selector(500)
            if ele.is_visible():
                break
        else:
            raise Exception("Timed out waiting for element to be visible")

            #元素是否check
    def ele_is_checked(self,selector):
        return self.page.is_checked(selector)

            #浏览器操作（刷新reload，前进forward，后退back）
    def browser_operation(self,reload=False,forward=False,back=False):
        if reload:
            self.page.reload()
        if forward:
            self.page.go_forward()
        if back:
            self.page.go_back()

            #截图操作
    def screenshot(self,path,full_page=True,locator=None):
        if locator is not None:
            self.page.locator(locator).screenshot(path=path)
            return path
        self.page.screenshot(path=path,full_page=full_page)
        return path

            #删除对象
    def del_auth(self):
        auth_path=Config.auth_dir+os.path.sep+"auth.json"
        if os.path.exists(auth_path):
            os.remove(auth_path)