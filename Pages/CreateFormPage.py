from BasePage.BasePage import BasePage

class CreateFormPage(BasePage):
    # 定位器封装（和你的用例一致）
    create_button = '//*[@id="desktopLayoutContainer"]/div/aside/div/div[1]/button'
    hover_form_button = '//*[@id=":ra:"]/div/div/section/div[1]/div[6]/div/div/img'
    create_sample_form_button = '//*[@id=":r4u:"]/div/div/div[1]/div/div/img'

    def __init__(self, page):
        super().__init__(page)  # 继承BasePage的page对象

    # 注意：原代码中调用的goto方法需删除，改用page.goto
    def click_create_button(self):
        """点击创建按钮（先等元素可见）"""
        self.ele_to_be_visible_force(self.create_button, timeout=10)
        self.page.click(self.create_button)

    def hover_hover_form_button(self):
        """悬浮到表单按钮（先等元素可见）"""
        self.ele_to_be_visible_force(self.hover_form_button, timeout=10)
        # 使用locator进行悬浮
        form_button_locator = self.page.locator(self.hover_form_button)
        form_button_locator.hover()
        # 等待悬浮菜单出现（等待创建示例表单按钮出现）
        # 使用较短的超时时间，因为菜单应该很快出现
        try:
            self.page.wait_for_selector(
                self.create_sample_form_button,
                state="visible",
                timeout=5000
            )
            print("✅ 已悬浮到表单按钮，菜单已出现")
        except Exception as e:
            print(f"⚠️ 等待菜单出现超时，但继续尝试：{e}")
            # 即使超时也继续，可能菜单需要更长时间或已经出现

    def click_create_sample_form_button(self):
        """点击创建示例表单按钮（先等元素可见）
        注意：需要在悬浮表单按钮后调用，保持悬浮状态
        悬浮后菜单会动态出现，需要等待菜单中的元素可见
        """
        # 等待悬浮菜单中的元素出现（使用更长的超时时间，因为菜单是动态加载的）
        # 使用 ele_to_be_visible_force 等待元素可见，但增加超时时间
        self.ele_to_be_visible_force(self.create_sample_form_button, timeout=15)
        # 元素可见后，立即点击（保持悬浮状态，不要移开鼠标）
        # 使用 locator 的 click 方法，Playwright 会自动处理鼠标位置
        sample_form_button = self.page.locator(self.create_sample_form_button)
        sample_form_button.click()