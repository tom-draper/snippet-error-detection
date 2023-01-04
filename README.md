# Code Snippet Error Detection

A project to search GitHub repo's for README.md containing snippets that contain syntax errors. A Python script crawls through the results of a GitHub search for README files containing snippets, checking whether the snippets can be evaluated. If evaluation fails, the snippet is flagged as a potential error. Currently only a handful of programming languages are considered.

It was found that many code snippets in READMEs use pseudo-correct syntax, or a mix of languages, often displaying expected results and other relevant information within the snippet. Therefore, some work is required to find a good balance for the sensitivity of error detection.
