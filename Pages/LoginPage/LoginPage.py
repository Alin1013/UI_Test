#封装登陆页面便于后续复用
from BasePage.BasePage import BasePage
import allure
from Config.Config import  Config

class LoginPage(BasePage):
    username='//*[@id="login_username"]'
    password='//*[@id="login_password"]'
    login_button='//*[@id="login"]/div[5]/div/div/div/div/button'

    #清除原始数据残留
    def del_auth(self):
        self.del_auth()

    @allure.step("打开登陆界面")
    def goto_login_page(self,url):
        full_url=Config.Base_url+url
        self.goto_url(full_url)
        #确保登录页元素可见
        self.ele_to_be_visible_force(self.username,timeout=10)

    @allure.step("输入账号")
    def fill_username(self,value):
        self.fill(self.username,value)

    @allure.step("输入密码")
    def fill_password(self,value):
        self.fill(self.password,value)

    @allure.step("点击登陆")
    def click_login_button(self):
        self.click(self.login_button)

    #刷新页面
    def browser_operation(self,reload=False,forward=False,back=False):
        self.browser_operation(reload=True,forward=False,back=False)