import os
import re
import string


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    files_list = []
    for root, dirs, files in os.walk(root):
        for f in files:
            f_path = os.path.join(root, f)
            files_list.append(f_path)
    return files_list

def get_text(fileName):
    f = open(fileName, encoding='latin-1')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    result_count = 0
    html_str = [f"<html>\n<body>\n<h2>Search results for <b>{', '.join(terms)}</b> in {len(docs)} files</h2>\n"]
    matching_files = []

    for doc in docs:
        if result_count >= 100:
            break
        
        lines = []

        with open(doc, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                for term in terms:
                    if re.search(re.escape(term), line, re.IGNORECASE):
                        lines.append(line.strip())
                        break
                if len(lines) >= 2:
                    break

        if lines:
            result_count += 1
            html_str.append(f"<a href='file://{doc}'>{doc}</a>")
            matching_files.append(os.path.basename(doc))
            for line in lines:
                for term in terms:
                    for word in line.split(" "):
                        if words(word) !=[] and words(word)[0] == term:
                            line = line.replace(word,f"<b>{word}</b>")
            # lines_html = "<br>".join(lines_with_terms)
            # formatted_html = f"<p>{href}<br>{lines_html}</p>"
            # html_str.append(formatted_html)
                html_str.append(f"{line}")
            html_str.append("</p><br><br>\n")

    html_str.append(f"</body>\n</html>")
    # html_str = " ".join(html_str)
    # print(html_str)
    return " ".join(html_str)

    # with open('results.html', 'w', encoding='utf-8') as html_file:
    #     html_file.write("<html><body>")
    #     html_file.write(f"<h2>Search results for <b>{', '.join(terms)}</b> in {result_count} files</h2>")
    #     html_file.write("".join(html_results))
    #     html_file.write("</body></html>")


def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
