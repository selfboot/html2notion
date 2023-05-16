<h1 align="center">Html2notion <a href='https://github.com/selfboot/html2notion/blob/master/READMEh.md'>English</a></h1>
<p align="center">
  <a href="https://github.com/selfboot/html2notion/actions/workflows/python-package.yml">
    <img src="https://github.com/selfboot/html2notion/actions/workflows/python-package.yml/badge.svg" alt="CI Test Status">
  </a>
 <a href="https://codecov.io/gh/selfboot/html2notion" >
 <img src="https://codecov.io/gh/selfboot/html2notion/branch/master/graph/badge.svg?token=SIM6I7BZU6" alt="Test coverage"/>
 </a>
</p>

html2notion 是一个非常有用的 Python 写的工具，它可以将 HTML 文档中的内容导入到 Notion 笔记中，从而使您能够更方便地将信息整理到 Notion 平台上。此外，html2notion 对印象笔记的内容进行了专门优化，还可以使用它来将印象笔记中的笔记导入到 Notion 中。

html2notion 功能非常强大，它支持将 HTML 文件的各种标签转换为 Notion 中对应的 Block，比如富文本块、标题、图片、代码块、引用、链接等。下面是将印象笔记中的笔记转换为 notion page 中的示例。

![迁移notion(保留格式)](https://raw.githubusercontent.com/selfboot/html2notion/master/demos/yinxiang_notion.png)

![迁移notion2(保留格式)](https://raw.githubusercontent.com/selfboot/html2notion/master/demos/yinxiang_notion2.png)

# 准备工作

只需要3步就可以使用 htmlnotion 来导入 html 到 notion 中。

## 复制 notion 数据库

点击链接 [notion template](https://selfboot.notion.site/selfboot/130bb48c6cbd4abbbb713d4d8472481a?v=ddda20d3f46b4b44a055d06792c142f0), 如下面的图所示，通过 "Duplicate" 按钮，复制一个新的数据库到自己的notion工作空间。

![notion template](https://raw.githubusercontent.com/selfboot/html2notion/master/demos/notion_templage.png)

## 安装 html2notion
需要 python>=3.8, 安装 html2notion 库。您可以使用 pip 命令来安装它：

```
pip install html2notion
```

## 准备 Notion 配置

我们需要使用 Notion API 密钥和数据库 ID 来授权 html2notion 访问 Notion 数据库，请按照以下步骤操作：

1. 创建 Integration
2. 与 Integration 共享数据库
3. 获取数据库 ID 和 API Key

这里共享数据库的时候，要选择前面 Duplicate 的数据库，因为导入操作需要用到这个 database 里面的一些预设 [Properties](https://developers.notion.com/reference/property-object) 信息。

具体方法请参考 notion 官方文档 [Create an integration](https://developers.notion.com/docs/create-a-notion-integration)。

设置完成后，将自己的 API Key 和数据库 ID 写入到一个配置文件 `config.json`。

```shell
{
    "notion": {
        "database_id": "<***demo***>",
        "api_key": "<***demo***>"
    }
}
```

# 使用

可以使用 `html2notion -h` 查看详细的帮助文档;

```
usage: html2notion [-h] --conf CONF [--log LOG] [--batch BATCH] (--file FILE | --dir DIR)

Html2notion: Save HTML to your Notion notes quickly and easily, while keeping the original format as much as possible

options:
  -h, --help     show this help message and exit
  --conf CONF    conf file path
  --log LOG      log direct path
  --batch BATCH  batch save concurrent limit
  --file FILE    Save single html file to notion
  --dir DIR      Save all html files in the dir to notion
```

比如要将路径 `./demos` 下的所有 html 文件导入到 notion 中，可以使用如下命令：

```shell
html2notion --conf config.json --dir ./demos --log ~/logs --batch 10
```

上面命令会将 `./demos` 目录下的所有 html 文件导入到 notion 中，同时会将日志输出到 `~/logs` 目录下，最多有 10 个并发任务。

# 更多信息

您可以在 html2notion 库的 GitHub 存储库中找到更多的信息和示例：[html2notion](https://github.com/kevinzg/html2notion)

## 贡献

如果您发现了任何错误或有任何改进意见，请不要犹豫，提交一个 pull request 或提出一个 issue,我很乐意接受您的贡献和反馈！

如果遇到导入失败，可以将 html 文件和日志文件一起提交到 issue 中，方便定位问题。

> 如果 html 文件中有隐私信息，请先删除。

## 许可证

此项目使用 MIT 许可证。详情请参阅 [LICENSE](./LICENSE) 文件。
