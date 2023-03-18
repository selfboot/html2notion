html2notion 是一个非常有用的 Python 库，它可以将 HTML 文档中的内容导入到 Notion 笔记中，从而使您能够更方便地将信息整理到 Notion 平台上。此外，由于 html2notion 与印象笔记兼容，您还可以使用它来将印象笔记中的笔记导出到 Notion 中。

html2notion 库的功能非常强大，它支持将 HTML 文件转换为 Notion 中的各种元素，如文本块、标题、图片、代码块等。这些元素可以在 Notion 中随意排列和编辑，非常方便。

如果您正在寻找一种方法来更好地管理您的笔记和信息，并且想要使用 Notion 平台，那么 html2notion 库就是一个非常不错的选择。您只需要简单地安装它，就可以开始将 HTML 文档转换为 Notion 笔记了。

# 安装

1. 首先，您需要在您的 Python 环境中安装 html2notion 库。您可以使用 pip 命令来安装它：

```
pip install html2notion

```

# 使用

## 获取 notion 参数

要获取 Notion API 密钥，请按照以下步骤操作：

1. 登录 [Notion](https://www.notion.so/)。如果您还没有 Notion 帐户，请先注册一个。
2. 转到 [Notion 开发人员页面](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration)。
3. 单击 “My integrations”。
4. 单击 “New integration”。
5. 输入一个名称，然后单击 “Submit”。
6. 单击 “Add a client secret”。
7. 将生成的 API 密钥复制到您的代码中。

要授权 Notion 的 API Key 访问某个数据库，请按照以下步骤操作：

1. 转到您要与 API Key 共享的数据库。
2. 单击数据库名称旁边的三个点。
6. 现在，您的 API Key 将能够访问此数据库。

请注意，为了使 API Key 能够访问数据库，您必须首先将其添加为 Notion 的集成。要添加集成，请转到 Notion 开发人员页面并按照指示操作。更多信息，请参阅 Notion 的 API 文档：[Notion API Docs](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration)。

要获取 Notion 数据库的 ID，请按照以下步骤操作：

1. 转到您要将 HTML 导入到的 Notion 数据库。
2. 单击数据库名称旁边的三个点。
3. 选择 “Properties”。
4. 将鼠标悬停在您想要导入 HTML 的列上，并单击列名称旁边的三个点。
5. 单击 “Property settings”。
6. 将数据库 ID 复制到您的代码中。

## 腾讯云 COS 密钥

## 印象笔记迁移
如果您想将印象笔记中的笔记导入到 Notion 中，您可以使用印象笔记的导出功能将笔记导出为 HTML 文件，然后使用上述命令将其导入到 Notion。

# 支持的 HTML 元素

以下是 html2notion 支持的 HTML 元素列表：

- `p`
- `h1`, `h2`, `h3`, `h4`, `h5`, `h6`
- `ul`, `ol`
- `li`
- `a`
- `img`
- `code`
- `blockquote`
- `hr`
- `br`

# 更多信息

您可以在 html2notion 库的 GitHub 存储库中找到更多的信息和示例：[html2notion](https://github.com/kevinzg/html2notion)

## 贡献

如果您发现了任何错误或有任何改进意见，请不要犹豫，提交一个 pull request 或提出一个 issue。我们很乐意接受您的贡献和反馈！

## 许可证

此项目使用 MIT 许可证。详情请参阅 LICENSE 文件。
