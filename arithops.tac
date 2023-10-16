[
  {
    "proc": "@main",
    "body": [
      {
        "opcode": "const",
        "args": [
          42
        ],
        "result": "%0"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%2"
      },
      {
        "opcode": "const",
        "args": [
          1
        ],
        "result": "%3"
      },
      {
        "opcode": "shr",
        "args": [
          "%2",
          "%3"
        ],
        "result": "%1"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%3"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%4"
      },
      {
        "opcode": "add",
        "args": [
          "%3",
          "%4"
        ],
        "result": "%2"
      },
      {
        "opcode": "print",
        "args": [
          "%2"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%3"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%4"
      },
      {
        "opcode": "sub",
        "args": [
          "%3",
          "%4"
        ],
        "result": "%2"
      },
      {
        "opcode": "print",
        "args": [
          "%2"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%5"
      },
      {
        "opcode": "const",
        "args": [
          3
        ],
        "result": "%6"
      },
      {
        "opcode": "mul",
        "args": [
          "%5",
          "%6"
        ],
        "result": "%3"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%4"
      },
      {
        "opcode": "add",
        "args": [
          "%3",
          "%4"
        ],
        "result": "%2"
      },
      {
        "opcode": "copy",
        "args": [
          "%2"
        ],
        "result": "%4"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%5"
      },
      {
        "opcode": "mod",
        "args": [
          "%4",
          "%5"
        ],
        "result": "%3"
      },
      {
        "opcode": "print",
        "args": [
          "%3"
        ],
        "result": null
      }
    ]
  }
]
