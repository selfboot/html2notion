html2notion 是一个非常有用的 Python 写的工具，它可以将 HTML 文档中的内容导入到 Notion 笔记中，从而使您能够更方便地将信息整理到 Notion 平台上。此外，html2notion 对印象笔记的内容进行了专门优化，还可以使用它来将印象笔记中的笔记导入到 Notion 中。

html2notion 功能非常强大，它支持将 HTML 文件的各种标签转换为 Notion 中对应的 Block，比如富文本块、标题、图片、代码块、引用、链接等。下面是将印象笔记中的笔记转换为 notion page 中的示例。

![迁移notion(保留格式)](https://github.com/selfboot/html2notion/blob/master/demos/yinxiang_notion.png)

![迁移notion2(保留格式)](https://github.com/selfboot/html2notion/blob/master/demos/yinxiang_notion2.png)

# 准备工作

只需要3步就可以使用 htmlnotion 来导入 html 到 notion 中。

## 复制 notion 数据库

点击链接 [notion template](https://selfboot.notion.site/selfboot/130bb48c6cbd4abbbb713d4d8472481a?v=ddda20d3f46b4b44a055d06792c142f0), 如下面的图所示，通过 "Duplicate" 按钮，复制一个新的数据库到自己的notion工作空间。

![notion template](https://github.com/selfboot/html2notion/blob/master/demos/notion_templage.png)

## 安装 html2notion
需要 python>=3.8, 安装 html2notion 库。您可以使用 pip 命令来安装它：

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
