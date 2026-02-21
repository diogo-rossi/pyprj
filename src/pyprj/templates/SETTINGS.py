SETTINGS_JSON: str = r"""{
    "[python]": {
        "editor.rulers": [
            {
                "column": {{line_length}},
                "color": "#36a3f0"
            }
        ],
        "rewrap.wrappingColumn": 0
    },
    "black-formatter.args": [
        "--line-length",
        "{{line_length}}"
    ],
    "isort.args": [
        "--line-length",
        "{{line_length}}"
    ],
    "python.testing.pytestArgs": [
        "tests",
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "editor.formatOnType": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "always"
    },
    "[markdown]": {
        "editor.wordWrap": "on",
        "editor.quickSuggestions": {
            "comments": "on",
            "strings": "on",
            "other": "on"
        },
        "files.trimTrailingWhitespace": false,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.rulers": [
            {
                "column": 80,
                "color": "#8a8a8a"
            }
        ],
        "rewrap.wrappingColumn": 0,
        "prettier.proseWrap": "always",
        "prettier.printWidth": 80,
        "prettier.endOfLine": "auto",
    },
}"""
