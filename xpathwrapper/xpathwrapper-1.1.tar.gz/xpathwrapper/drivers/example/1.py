from xpathwrapper.basec import driver,checkbyxpath

driver.get('http://testing.pythonautomation.tk/')

checkbyxpath("//ul[@class='actions']//li/a[text()='Test Me']").click()