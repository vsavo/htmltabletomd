import pytest

from htmltabletomd import htmltabletomd

test_data = [
    (
        """
<table>
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
""",
        """| Heading 1 | Heading 2 |
| :--- | :--- |
| column 11 | column 12 |
| column 21 | column 22 |
""",
    ),
    (
        """
<table>
  <tr>
    <td>column 11</td>
    <td>column 12</td>
  </tr>
  <tr>
    <td>column 21</td>
    <td>column 22</td>
  </tr>
</table>
""",
        """| | |
| :--- | :--- |
| column 11 | column 12 |
| column 21 | column 22 |
""",
    ),
    (
        """
<table>
  <tr>
    <th>Heading 1</th>
    <th>Heading 2</th>
  </tr>
  <tr>
    <td>column 11</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>column 22</td>
  </tr>
</table>
""",
        """| Heading 1 | Heading 2 |
| :--- | :--- |
| column 11 |  |
|  | column 22 |
""",
    ),
]


@pytest.mark.parametrize(
    "input_html, expected_md",
    test_data,
    ids=["complete table", "missing headers", "missing cells"],
)
def test_md_table_conversion(input_html, expected_md):
    assert htmltabletomd.convert_table(input_html) == expected_md


html_content_test_data = [
    (
        """
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
""",
        """| Heading __1__ | Heading __2__ |
| :--- | :--- |
| column _11_ | column __12__ |
| column 21 | column ___22___ |
""",
    ),
]


@pytest.mark.parametrize(
    "input_html, expected_md",
    html_content_test_data,
    ids=["table with html content"],
)
def test_html_content_conversion(input_html, expected_md):
    assert (
        htmltabletomd.convert_table(input_html, content_conversion_ind=True)
        == expected_md
    )


newline_pipe_content_test_data = [
    (
        """
<table>
  <tr>
    <th>Heading 1</th>
    <th>Heading 2</th>
  </tr>
  <tr>
    <td>column 11
    2nd line</td>
    <td>column 1|2</td>
  </tr>
  <tr>
    <td>column 2|1
    2nd line</td>
    <td>column 22</td>
  </tr>
</table>
""",
        """| Heading 1 | Heading 2 |
| :--- | :--- |
| column 11<br>    2nd line | column 1&#124;2 |
| column 2&#124;1<br>    2nd line | column 22 |
""",
    ),
]


@pytest.mark.parametrize(
    "input_html, expected_md",
    newline_pipe_content_test_data,
    ids=["table with newline and pipe"],
)
def test_newline_pipe_conversion(input_html, expected_md):
    assert (
        htmltabletomd.convert_table(input_html, content_conversion_ind=True)
        == expected_md
    )


column_alignment_test_data = [
    (
        """
<table>
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
""",
        """| Heading 1 | Heading 2 |
| :--- | :--- |
| column 11 | column 12 |
| column 21 | column 22 |
""",
        "left",
    ),
    (
        """
<table>
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
""",
        """| Heading 1 | Heading 2 |
| :---: | :---: |
| column 11 | column 12 |
| column 21 | column 22 |
""",
        "center",
    ),
    (
        """
<table>
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
""",
        """| Heading 1 | Heading 2 |
| ---: | ---: |
| column 11 | column 12 |
| column 21 | column 22 |
""",
        "right",
    ),
]


@pytest.mark.parametrize(
    "input_html, expected_md, alignment_indicator",
    column_alignment_test_data,
    ids=["left aligned", "center aligned", "right aligned"],
)
def test_column_alignment(input_html, expected_md, alignment_indicator):
    actual_md = htmltabletomd.convert_table(
        input_html, content_conversion_ind=True, all_cols_alignment=alignment_indicator
    )
    assert actual_md == expected_md


invalid_alignment_test_data = [
    (
        """
<table>
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
""",
        "Invalid alignment option for 'all_cols_alignment' arg. "
        "Expected one of: ['left', 'center', 'right']",
        "riight",
    ),
]


@pytest.mark.parametrize(
    "input_html, expected_exception, alignment_indicator",
    invalid_alignment_test_data,
    ids=["invalid alignment"],
)
def test_invalid_column_alignment(input_html, expected_exception, alignment_indicator):
    with pytest.raises(ValueError) as actual_exception:
        actual_md = htmltabletomd.convert_table(
            input_html,
            content_conversion_ind=True,
            all_cols_alignment=alignment_indicator,
        )
    assert expected_exception == str(actual_exception.value)


missing_tr_tag_test_data = [
    (
        "Here is <i>some text</i>",
        "No 'tr' tag found",
        "left",
    ),
]


@pytest.mark.parametrize(
    "input_html, expected_exception, alignment_indicator",
    missing_tr_tag_test_data,
    ids=["No tr tag found"],
)
def test_missing_tr_tag(input_html, expected_exception, alignment_indicator):
    with pytest.raises(ValueError) as actual_exception:
        actual_md = htmltabletomd.convert_table(
            input_html,
            content_conversion_ind=True,
            all_cols_alignment=alignment_indicator,
        )
    assert expected_exception == str(actual_exception.value)


non_html_test_data = [
    (
        "This is a plain text with no html",
        "This is a plain text with no html",
        "right",
    ),
]


@pytest.mark.parametrize(
    "input_string, expected_string, alignment_indicator",
    non_html_test_data,
    ids=["non html input"],
)
def test_non_html_string(input_string, expected_string, alignment_indicator):
    actual_md = htmltabletomd.convert_table(
        input_string,
        content_conversion_ind=True,
        all_cols_alignment=alignment_indicator,
    )
    assert actual_md == expected_string
