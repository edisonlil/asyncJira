from jira import JIRA

# 项目用户
ProjectUsers = {}
# 优先级
Priorities = {}
# 相关模块
Components = {}

# 任务类型
IssueTypeTask = {"id": "10100", "name": "任务"}


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

    def init_user(self):

        users = self.client.search_assignable_users_for_issues(query="query", project=self.projectCode )
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
        project_components = self.client.project_components(project=self.projectCode )
        for component in project_components:
            Components[component.name] = component.id
        pass

    pass

    def create_issue(self, fields):
        """
            创建问题
        """
        return self.client.create_issue(fields)
    pass
