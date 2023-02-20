import json

from jira import JIRA

# 项目用户
ProjectUsers = {}
# 优先级
Priorities = {}
# 相关模块
Components = {}

FixVersions = {}

# 问题类型
# For JiraClient().issue_types()
IssueTypeTask = {"id": "10100", "name": "任务"}
IssueTypeImprove = {"id": "10203", "name": "改进"}
IssueTypeSubTask = {"id": "10101", "name": "子任务"}
IssueTypeBug = {"id": "10201", "name": "BUG"}
IssueTypeBug = {"id": "10204", "name": "新功能"}


class JiraClient:

    def __init__(self, jiraServer, username, password, projectCode):
        """
        jiraServer： jira地址
        username： 用户名
        password： 密码
        projectCode：项目code
        """

        self.server = jiraServer
        self.basic_auth = (username, password)
        self.projectCode = projectCode
        self.client = None
        self.login()

    def login(self):
        """
            登录
            self: JiraClient
        """
        self.client = JIRA(server=self.server, basic_auth=self.basic_auth)
        if self.client is not None:
            self.init()
            return True
        else:
            return False

    def init(self):
        self.init_priority()
        self.init_user()
        self.init_components()
        self.init_fixVersion()

    def init_user(self):

        users = self.client.search_assignable_users_for_issues(query="query", project=self.projectCode)
        for user in users:
            ProjectUsers[user.displayName] = user.key
        pass

    pass

    def init_priority(self):
        """
            任务优先级
        """
        priorities = self.client.priorities()
        for priority in priorities:
            Priorities[priority.name] = priority.id
        pass

    pass

    def init_components(self):
        """
           相关模块
        """
        project_components = self.client.project_components(project=self.projectCode)
        for component in project_components:
            Components[component.name] = component.id
        pass

    pass

    def init_fixVersion(self):
        """
           相关模块
        """
        project_versions = self.client.project_versions(project=self.projectCode)
        for version in project_versions:
            FixVersions[version.name] = version.id
        pass

    pass

    def create_issue(self, fields):
        """
            创建问题
        """
        return self.client.create_issue(fields)

    pass

    def issue_types(self):
        """
        获取所有问题类型
        任务，子任务，故事，故障，Epic，BUG，新功能，改进，子任务
        """
        return self.client._get_json("issuetype")


if __name__ == "__main__":
    client = JiraClient('http://127.0.0.1:28080/', 'admin', '******', "******")
    print(json.dumps(client.issue_types(), ensure_ascii=False))

    pass
