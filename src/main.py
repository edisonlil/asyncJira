# 环境准备
# !pip3 install _jira
# !pip3 install pandas
# !pip3 install openpyxl

# 参考资料：https://developer.atlassian.com/cloud/jira/platform

import src._jira.JiraSubmit as jira

# Jira 域名
JIRA_SERVER = 'http://127.0.0.1:28080/'
# Jira账号（必须有建子任务权限）
JIRA_USER = "admin"
# Jira密码
JIRA_PWD = "******"

# 项目Code
ProjectCode = "******"

if __name__ == "__main__":

    print("开始导入")
    jiraTaskSubmit = jira.JiraTaskSubmit(JIRA_SERVER, JIRA_USER, JIRA_PWD, ProjectCode)
    jiraTaskSubmit.process_excel(r'C:\Users\edsio\Documents\WeChat Files\wxid_uslo8uwcxquz22\FileStorage\File\2023-02\任务管理_1.xlsx')
    print("导入完毕")