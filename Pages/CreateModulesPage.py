import os
import allure
from BasePage.BasePage import BasePage
from Config.Config import Config

class CreateModulesPage(BasePage):
    # 定位器封装
    create_button='//*[@id="desktopLayoutContainer"]/div/aside/div/div[1]/button'
    back_button='//*[@id="root"]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/svg'
    title_input='//*[@id="root"]/div/div/div[1]/div[1]/div[1]/div[1]/span/input'
    create_folder_button='//*[@id=":ra:"]/div/div/section/div[2]/div[1]/div/span'
    folder_title='//*[@id="name"]'
    save_button='body > div:nth-child(11) > div > div.ant-modal-wrap.ant-modal-confirm-centered.ant-modal-centered > div > div:nth-child(1) > div > div > div > div > div > div > div > div > button.ant-btn.css-1m63z2v.ant-btn-default.ant-btn-color-default.ant-btn-variant-outlined.sm-btn.sm-btn-normal-primary'
    #轻文档
    word_button='//*[@id=":ra:"]/div/div/section/div[1]/div[1]/div'
    #传统文档
    tra_word_button='//*[@id=":ra:"]/div/div/section/div[1]/div[2]/div/div/img'
    #专业表格
    pro_excel_button='//*[@id=":rp:"]/div/div/section/div[1]/div[3]/div'
    #应用表格
    use_excel_button='//*[@id=":rp:"]/div/div/section/div[1]/div[4]/div'
    #幻灯片
    ppt_button='//*[@id=":rp:"]/div/div/section/div[1]/div[5]/div'


    def __init__(self, page):
        super().__init__(page)  # 继承BasePage的page对象

    def click_create_button(self):
        """点击创建按钮（先等元素可见）"""
        self.ele_to_be_visible_force(self.create_button, timeout=10)
        self.page.click(self.create_button)

    def create_folder_and_save(self, folder_name="ui_测试"):
        """
        创建folder，填充标题，点击保存，等待页面加载完成后截图
        """
        # 点击创建folder按钮
        self.ele_to_be_visible_force(self.create_folder_button, timeout=10)
        self.page.click(self.create_folder_button)
        
        # 等待folder标题输入框可见并填充
        self.ele_to_be_visible_force(self.folder_title, timeout=10)
        self.fill(self.folder_title, folder_name)
        
        # 点击保存按钮
        self.ele_to_be_visible_force(self.save_button, timeout=10)
        self.page.click(self.save_button)
        
        # 等待页面加载完成
        self.page.wait_for_load_state("networkidle", timeout=15000)
        
        # 截图
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建folder_{folder_name}_成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建folder_{folder_name}_成功",
            attachment_type=allure.attachment_type.PNG
        )

    def get_component_button(self, component_type):
        """
        根据组件类型返回对应的按钮定位器
        """
        component_map = {
            "创建文档": self.word_button,
            "创建传统文档": self.tra_word_button,
            "创建专业表格": self.pro_excel_button,
            "创建应用表格": self.use_excel_button,
            "创建幻灯片": self.ppt_button
        }
        return component_map.get(component_type)

    def create_component_and_fill_title(self, component_type, title):
        """
        创建组件，填充标题，返回并截图
        Args:
            component_type: 组件类型（从yaml中的"功能"字段获取）
            title: 标题（从yaml中的"标题"字段获取）
        """
        # 获取组件按钮
        component_button = self.get_component_button(component_type)
        if component_button is None:
            raise ValueError(f"未知的组件类型: {component_type}")
        
        # 使用locator().click()并设置超时，如果元素不存在会更快失败
        # 先等待一下确保创建面板已打开
        self.page.wait_for_timeout(500)
        
        # 使用locator点击，设置较短的超时
        try:
            self.page.locator(component_button).click(timeout=5000)
        except Exception as e:
            # 如果点击失败，可能是元素还没出现，再等待一下
            print(f"⚠️ 首次点击失败，等待后重试: {str(e)}")
            self.page.wait_for_timeout(1000)
            self.page.locator(component_button).click(timeout=10000)
        
        # 等待页面加载
        self.page.wait_for_load_state("networkidle", timeout=15000)
        
        # 点击按钮后校验title输入框是否可见并填充标题
        self.ele_to_be_visible_force(self.title_input, timeout=10)
        self.fill(self.title_input, title)
        
        # 等待标题填充完成
        self.page.wait_for_timeout(500)
        
        # 点击返回按钮
        self.page.locator(self.back_button).click(timeout=5000)
        
        # 等待页面加载完成
        self.page.wait_for_load_state("networkidle", timeout=15000)
        
        # 截图
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建{component_type}_{title}_返回后.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建{component_type}_{title}_返回后",
            attachment_type=allure.attachment_type.PNG
        )

    def create_all_modules(self, test_data_list):
        """
        创建所有模块的主流程
        Args:
            test_data_list: 测试数据列表（从yaml文件读取）
        """
        # 1. 点击创建按钮
        self.click_create_button()
        
        # 2. 创建folder并保存
        self.create_folder_and_save("ui_测试")
        
        # 3. 在folder内部再次点击create_button，显示组件创建选项
        self.page.click(self.create_button)
        # 等待创建选项面板出现
        self.page.wait_for_timeout(1500)
        
        # 4. 遍历yaml中的每个组件，创建并填充标题
        for index, case_data in enumerate(test_data_list):
            component_type = case_data.get("功能")
            title = case_data.get("标题")
            
            if component_type and title:
                # 从第二个组件开始，每次创建组件前都点击create_button，确保创建面板打开
                # （因为返回后创建面板可能关闭了）
                if index > 0:
                    self.page.click(self.create_button)
                    # 等待创建选项面板出现
                    self.page.wait_for_timeout(1500)
                
                self.create_component_and_fill_title(component_type, title)

