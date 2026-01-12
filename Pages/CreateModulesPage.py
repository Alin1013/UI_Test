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
        self.click(self.create_button)
        # 等待创建面板打开
        self.page.wait_for_timeout(2000)

    def create_folder_and_save(self, folder_name="ui_测试"):
        """
        创建folder，填充标题，点击保存，等待页面加载完成后截图
        """
        print("🔄 准备创建folder")
        # 直接点击创建folder按钮（不校验可见性）
        self.click(self.create_folder_button)
        print("✅ 已点击创建folder按钮")
        
        # 等待一下，确保弹窗出现
        self.page.wait_for_timeout(2000)
        
        # 直接填充folder标题（不校验可见性，根据用户要求）
        try:
            self.fill(self.folder_title, folder_name)
            print(f"✅ 已填充folder标题: {folder_name}")
        except Exception as e:
            print(f"⚠️ 填充folder标题失败，尝试等待后重试: {str(e)}")
            self.page.wait_for_timeout(1000)
            self.fill(self.folder_title, folder_name)
            print(f"✅ 已填充folder标题: {folder_name}")
        
        # 等待一下，确保填充完成
        self.page.wait_for_timeout(500)
        
        # 点击保存按钮（先等待可见）
        self.ele_to_be_visible_force(self.save_button, timeout=10)
        self.click(self.save_button)
        print("✅ 已点击保存按钮")
        
        # 等待页面加载完成
        self.page.wait_for_load_state("networkidle", timeout=15000)
        
        # 截图
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建文件夹（{folder_name}）成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建文件夹（{folder_name}）成功",
            attachment_type=allure.attachment_type.PNG
        )

    def create_word(self, component_type,title="test_word"):
        self.click_create_button()
        self.click(self.word_button)
        self.page.wait_for_timeout(2000)
        self.fill(self.title_input, title)
        self.page.wait_for_timeout(500)
        self.click(self.back_button)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建文档({title})成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建文档成功",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"✅ 截图已保存: {screenshot_path}")

    def create_traditional_word(self, component_type,title="test_traditional"):
        self.click_create_button()
        self.click(self.tra_word_button)
        self.page.wait_for_timeout(2000)
        self.fill(self.title_input, title)
        self.page.wait_for_timeout(500)
        self.click(self.back_button)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建传统文档({title})成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建传统文档成功",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"✅ 截图已保存: {screenshot_path}")

    def create_excel(self, component_type,title="test_excel"):
        self.click_create_button()
        self.click(self.pro_excel_button)
        self.page.wait_for_timeout(2000)
        self.fill(self.title_input, title)
        self.page.wait_for_timeout(500)
        self.click(self.back_button)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建专业表格({title})成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建专业表格成功",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"✅ 截图已保存: {screenshot_path}")

    def create_use_excel(self, component_type,title="test_use_excel"):
        self.click_create_button()
        self.click(self.use_excel_button)
        self.page.wait_for_timeout(2000)
        self.fill(self.title_input, title)
        self.page.wait_for_timeout(500)
        self.click(self.back_button)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建应用表格({title})成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建应用表格成功",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"✅ 截图已保存: {screenshot_path}")

    def create_ppt(self, component_type,title="test_ppt"):
        self.click_create_button()
        self.click(self.ppt_button)
        self.page.wait_for_timeout(2000)
        self.fill(self.title_input, title)
        self.page.wait_for_timeout(500)
        self.click(self.back_button)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        screenshot_path = os.path.join(Config.test_screenshots_dir, f"创建幻灯片（{title}）成功.png")
        self.screenshot(screenshot_path, full_page=True)
        allure.attach.file(
            source=screenshot_path,
            name=f"创建幻灯片成功",
            attachment_type=allure.attachment_type.PNG
        )
        print(f"✅ 截图已保存: {screenshot_path}")



    




