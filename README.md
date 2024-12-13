# Ergo

> [!IMPORTANT]
> A work in progress.

Ergo is an attempt at a shell language that is designed with ease of use in mind
for smartphone users. Please have a look under [`samples/`](samples/) for
examples. For now the implementation will be done in Python, however if the
attempt succeeds, it will eventually will be ported to Kotlin for use with
Android SDK.

## Demo
[`samples/hello-world.ergo`](samples/hello-world.ergo) should generate an AST
like this:

```py
[Token(type=<TokenType.IDENT: 1>, literal='cmd-here', children=[]),
 Token(type=<TokenType.ARG: 5>, literal='arg without key here', children=[]),
 Token(type=<TokenType.ARG: 5>,
       literal='another arg without key here "with quotes" and 1 2 4 numbers, '
               'and so on.',
       children=[]),
 Token(type=<TokenType.KEY: 4>,
       literal='arg1',
       children=[Token(type=<TokenType.STRING: 2>,
                       literal='arg1 value',
                       children=[])]),
 Token(type=<TokenType.KEY: 4>,
       literal='arg2',
       children=[Token(type=<TokenType.STRING: 2>,
                       literal='arg2 value',
                       children=[]),
                 Token(type=<TokenType.STRING: 2>,
                       literal="arg2's another value here",
                       children=[]),
                 Token(type=<TokenType.STRING: 2>,
                       literal="arg2's third value is here",
                       children=[])]),
 Token(type=<TokenType.KEY: 4>,
       literal='arg3',
       children=[Token(type=<TokenType.STRING: 2>,
                       literal="arg3's value",
                       children=[])])]
```
## Building
After cloning the repo, you can do the following with `uv` (a package manager)
from the source tree's root:

```
uv sync
uv run ergo samples/hello-world.ergo
```

You may use any build backend you desire as long it understands a
`pyproject.toml` file.
