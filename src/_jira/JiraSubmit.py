import src._jira.JiraClient as jc
import pandas as pd


class JiraTaskSubmit:

    def __init__(self, jiraServer, username, password, projectCode):
        self.jiraClient = jc.JiraClient(jiraServer, username, password, projectCode)

    pass

    def process_excel(self, excelFilePath):

        """
            解析excel导入到jira
        """

        df = pd.read_excel(excelFilePath,
                           sheet_name='任务管理',
                           skiprows=[1],
                           engine='openpyxl'
                           )

        for row in df.itertuples():

            # 入参字段
            fields = {
                "project": {"key": self.jiraClient.projectCode},
                "assignee": {"name": jc.ProjectUsers[getattr(row, '任务执行人')]},
                "summary": getattr(row, '概要').strip().replace('\n', ''),
                "priority": {"id": jc.Priorities[getattr(row, '重要紧急程度')]},
                "reporter": {"name": jc.ProjectUsers[getattr(row, '报告人')]},
                "components": getComponents(row),
                "fixVersions": getFixVersions(row),
                "versions": getVersions(row)
            }

            if getattr(row, '问题类型') is not None:
                fields["issuetype"] = switchIssueTask(row)
            pass

            if getattr(row, '问题类型') is not None:
                if str(getattr(row, '问题类型')) == "BUG":
                    fields["issuetype"] = jc.IssueTypeBug
                elif str(getattr(row, '问题类型')) == "改进":
                    fields["issuetype"] = jc.IssueTypeImprove
                else:
                    fields["issuetype"] = jc.IssueTypeTask
            pass

            # 预估工时
            if getattr(row, '计划完成时长') is not None:
                fields['timetracking'] = {
                    "originalEstimate": str(getattr(row, '计划完成时长')) + 'h'
                }
            pass

            # 任务描述
            if isinstance(getattr(row, '描述'), str):
                fields['description'] = getattr(row, '描述')
            else:
                fields['description'] = ''
            pass
            create_issue = self.jiraClient.create_issue(fields)
            print(create_issue)
        pass

    pass


pass


def switchIssueTask(row):
    if str(getattr(row, '问题类型')) == "BUG":
        return jc.IssueTypeBug
    elif str(getattr(row, '问题类型')) == "改进":
        return jc.IssueTypeImprove
    else:
        return jc.IssueTypeTask


def getFixVersions(row):
    if getattr(row, "影响版本") is None:
        return []

    versions = str(getattr(row, '影响版本')).split(",")
    result = []
    for version in versions:
        result.append({
            "id": jc.FixVersions[version]
        })
    pass
    return result


def getVersions(row):
    if getattr(row, "修复的版本") is None:
        return []

    versions = str(getattr(row, '修复的版本')).split(",")
    result = []
    for version in versions:
        result.append({
            "id": jc.FixVersions[version]
        })
    pass
    return result


def getComponents(row):
    if getattr(row, '职责分类') is None:
        return []

    components = str(getattr(row, '职责分类')).split(",")

    result = []
    for component in components:
        result.append({
            "id": jc.Components[component]
        })
    pass
    return result


def fromDate(date):
    try:
        return date.__format__('%Y/%m/%d')
    except Exception as e:
        {}

    try:
        return date.__format__('%Y-%m-%d')
    except Exception as e:
        {}
