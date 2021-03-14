# htmltabletomd

`htmltabletomd` is for converting html tables to markdown.
Additionally, contents inside table cells can be converted to markdown if they contain HTML, 
for which it uses the library `htmltomarkdown` .

## Installation

`pip install htmltabletomd`

## Usage

### Convert HTML table to Markdown table
```python
import htmltabletomd

html_table = """<table>
  <tr>
    <th>Heading 1</th>
    <th>Heading 2</th>
  </tr>
  <tr>
    <td>column 11</td>
    <td>column 12</td>
  </tr>
  <tr>
    <td>column 21</td>
    <td>column 22</td>
  </tr>
</table>
"""

md_table = htmltabletomd.convert_table(html_table)
print(md_table)
```

Output:

```
| Heading 1 | Heading 2 |
| :--- | :--- |
| column 11 | column 12 |
| column 21 | column 22 |
```

### Pass `all_cols_alignment` argument to align text in the columns to the left, right, or center

For the above html table...

```python
md_table = htmltabletomd.convert_table(html_table, all_cols_alignment="right")
print(md_table)
```

Output:

```
| Heading 1 | Heading 2 |
| ---: | ---: |
| column 11 | column 12 |
| column 21 | column 22 |
```

Allowed values: `left`, `right` or `center`.

### Pass `content_conversion_ind` argument to convert html contents inside the table cells to markdown

```python
import htmltabletomd

html_table = """
<table>
  <tr>
    <th>Heading <b>1</b></th>
    <th>Heading <b>2</b></th>
  </tr>
  <tr>
    <td>column <i>11</i></td>
    <td>column <b>12</b></td>
  </tr>
  <tr>
    <td>column 21</td>
    <td>column <b><i>22</i></b></td>
  </tr>
</table>
"""

md_table = htmltabletomd.convert_table(html_table, content_conversion_ind=True)
print(md_table)
```

Output:

```
| Heading __1__ | Heading __2__ |
| :--- | :--- |
| column _11_ | column __12__ |
| column 21 | column ___22___ |
```
