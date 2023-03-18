html2notion is a very useful Python library that allows you to import content from HTML documents into Notion notes, making it easier for you to organize information on the Notion platform. In addition, because html2notion is compatible with Evernote, you can also use it to export notes from Evernote to Notion.

The html2notion library is very powerful and supports converting HTML files to various elements in Notion, such as text blocks, headings, images, code blocks, and more. These elements can be arranged and edited freely in Notion, which is very convenient.

If you are looking for a way to better manage your notes and information and want to use the Notion platform, then the html2notion library is a great choice. You just need to install it and you can start converting HTML documents to Notion notes.

# Installation

1. First, you need to install the html2notion library in your Python environment. You can use the pip command to install it:

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