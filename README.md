html2notion is an incredibly useful tool written in Python, which allows you to import content from HTML documents into Notion notes, making it more convenient for you to organize information on the Notion platform. In addition, html2notion has been specifically optimized for the content of Evernote, and you can also use it to import notes from Evernote into Notion.

html2notion has powerful features and supports converting various tags in HTML files into corresponding Blocks in Notion, such as rich text blocks, headings, images, code blocks, quotes, links, etc. Below are examples of converting notes from Evernote into Notion pages.

![yinxiang notion(simple demos)](https://github.com/selfboot/html2notion/blob/master/demos/yinxiang_notion.png)

![yinxiang notion2(rich text)](https://github.com/selfboot/html2notion/blob/master/demos/yinxiang_notion2.png)

# Prepare

You only need 3 steps to use htmlnotion to import HTML into Notion.

## Duplicate database

Click the link [notion template](https://selfboot.notion.site/selfboot/130bb48c6cbd4abbbb713d4d8472481a?v=ddda20d3f46b4b44a055d06792c142f0). As shown in the image below, use the "Duplicate" button to copy a new database to your own Notion workspace.

![notion template](https://github.com/selfboot/html2notion/blob/master/demos/yinxiang_notion.png)

## Install html2notion

Requires python>=3.8, install the html2notion library. You can use the pip command to install it:

```
pip install html2notion
```

# Usage

## Get Notion parameters

To get a Notion API key, follow these steps:

1. Log in to [Notion](https://www.notion.so/). If you don't have a Notion account yet, please register one first.
2. Go to the [Notion Developer](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration) page.
3. Click "My integrations".
4. Click "New integration".
5. Enter a name and click "Submit".
6. Click "Add a client secret".
7. Copy the generated API key to your code.

To authorize a Notion API key to access a database, follow these steps:

1. Go to the database you want to share with the API key.
2. Click the three dots next to the database name.
3. Now your API key will be able to access this database.

Note that in order for an API key to access a database, you must first add it as an integration to Notion. To add an integration, go to the Notion Developer page and follow the instructions. For more information, see Notion's API documentation: [Notion API Docs](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration).

To get the ID of a Notion database, follow these steps:

1. Go to the Notion database you want to import HTML into.
2. Click the three dots next to the database name.
3. Select "Properties".
4. Hover over the column where you want to import HTML and click the three dots next to the column name.
5. Click "Property settings".
6. Copy the database ID to your code.

## Tencent Cloud COS key

## Evernote migration

If you want to import notes from Evernote into Notion, you can use Evernote's export function to export notes as HTML files and then use the above command to import them into Notion.

# Supported HTML elements

The following is a list of HTML elements supported by html2notion:

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

# More information

You can find more information and examples in the html2notion library's Issue: [html2notion](https://github.com/selfboot/html2notion/issues)

## Contribution

If you find any errors or have any improvement suggestions, please do not hesitate to submit a pull request or issue. We are happy to accept your contributions and feedback!

## License

This project uses the MIT license. Please refer to the LICENSE file for details.