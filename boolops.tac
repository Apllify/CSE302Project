[
  {
    "proc": "@main",
    "body": [
      {
        "opcode": "const",
        "args": [
          10
        ],
        "result": "%0"
      },
      {
        "opcode": "const",
        "args": [
          20
        ],
        "result": "%1"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%2"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%3"
      },
      {
        "opcode": "sub",
        "args": [
          "%2",
          "%3"
        ],
        "result": "%2"
      },
      {
        "opcode": "jz",
        "args": [
          "%2",
          "%.L0"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L1"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L0"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          0
        ],
        "result": "%4"
      },
      {
        "opcode": "print",
        "args": [
          "%4"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L2"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L1"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L2"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%4"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%5"
      },
      {
        "opcode": "sub",
        "args": [
          "%4",
          "%5"
        ],
        "result": "%4"
      },
      {
        "opcode": "jnz",
        "args": [
          "%4",
          "%.L3"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L4"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L3"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          1
        ],
        "result": "%6"
      },
      {
        "opcode": "print",
        "args": [
          "%6"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L5"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L4"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L5"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%8"
      },
      {
        "opcode": "const",
        "args": [
          2
        ],
        "result": "%9"
      },
      {
        "opcode": "mul",
        "args": [
          "%8",
          "%9"
        ],
        "result": "%6"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%7"
      },
      {
        "opcode": "sub",
        "args": [
          "%6",
          "%7"
        ],
        "result": "%6"
      },
      {
        "opcode": "jz",
        "args": [
          "%6",
          "%.L6"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L7"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L6"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          2
        ],
        "result": "%8"
      },
      {
        "opcode": "print",
        "args": [
          "%8"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L8"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L7"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L8"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L9"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L12"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L9"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L9"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          3
        ],
        "result": "%8"
      },
      {
        "opcode": "print",
        "args": [
          "%8"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L11"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L10"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L11"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          1
        ],
        "result": "%8"
      },
      {
        "opcode": "const",
        "args": [
          1
        ],
        "result": "%9"
      },
      {
        "opcode": "sub",
        "args": [
          "%8",
          "%9"
        ],
        "result": "%8"
      },
      {
        "opcode": "jz",
        "args": [
          "%8",
          "%.L13"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L16"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L16"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L14"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L13"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          4
        ],
        "result": "%10"
      },
      {
        "opcode": "print",
        "args": [
          "%10"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L15"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L14"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L15"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%10"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%11"
      },
      {
        "opcode": "sub",
        "args": [
          "%10",
          "%11"
        ],
        "result": "%10"
      },
      {
        "opcode": "jl",
        "args": [
          "%10",
          "%.L17"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L18"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L17"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          5
        ],
        "result": "%12"
      },
      {
        "opcode": "print",
        "args": [
          "%12"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L19"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L18"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L19"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%12"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%13"
      },
      {
        "opcode": "sub",
        "args": [
          "%12",
          "%13"
        ],
        "result": "%12"
      },
      {
        "opcode": "jnle",
        "args": [
          "%12",
          "%.L20"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L21"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L20"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          6
        ],
        "result": "%14"
      },
      {
        "opcode": "print",
        "args": [
          "%14"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L22"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L21"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L22"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%14"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%15"
      },
      {
        "opcode": "sub",
        "args": [
          "%14",
          "%15"
        ],
        "result": "%14"
      },
      {
        "opcode": "jl",
        "args": [
          "%14",
          "%.L23"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L24"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L23"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          7
        ],
        "result": "%16"
      },
      {
        "opcode": "print",
        "args": [
          "%16"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L25"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L24"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L25"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%16"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%17"
      },
      {
        "opcode": "sub",
        "args": [
          "%16",
          "%17"
        ],
        "result": "%16"
      },
      {
        "opcode": "jle",
        "args": [
          "%16",
          "%.L26"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L27"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L26"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          8
        ],
        "result": "%18"
      },
      {
        "opcode": "print",
        "args": [
          "%18"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L28"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L27"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L28"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%18"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%19"
      },
      {
        "opcode": "sub",
        "args": [
          "%18",
          "%19"
        ],
        "result": "%18"
      },
      {
        "opcode": "jnl",
        "args": [
          "%18",
          "%.L29"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L30"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L29"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          9
        ],
        "result": "%20"
      },
      {
        "opcode": "print",
        "args": [
          "%20"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L31"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L30"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L31"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%20"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%21"
      },
      {
        "opcode": "sub",
        "args": [
          "%20",
          "%21"
        ],
        "result": "%20"
      },
      {
        "opcode": "jle",
        "args": [
          "%20",
          "%.L32"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L33"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L32"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          10
        ],
        "result": "%22"
      },
      {
        "opcode": "print",
        "args": [
          "%22"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L34"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L33"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L34"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%22"
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%23"
      },
      {
        "opcode": "sub",
        "args": [
          "%22",
          "%23"
        ],
        "result": "%22"
      },
      {
        "opcode": "jle",
        "args": [
          "%22",
          "%.L35"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L38"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L38"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%1"
        ],
        "result": "%24"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%25"
      },
      {
        "opcode": "sub",
        "args": [
          "%24",
          "%25"
        ],
        "result": "%24"
      },
      {
        "opcode": "jle",
        "args": [
          "%24",
          "%.L35"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L36"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L35"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          11
        ],
        "result": "%26"
      },
      {
        "opcode": "print",
        "args": [
          "%26"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L37"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L36"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L37"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%26"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%27"
      },
      {
        "opcode": "sub",
        "args": [
          "%26",
          "%27"
        ],
        "result": "%26"
      },
      {
        "opcode": "jz",
        "args": [
          "%26",
          "%.L39"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L40"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L39"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          12
        ],
        "result": "%28"
      },
      {
        "opcode": "print",
        "args": [
          "%28"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L41"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L40"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L41"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%28"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%29"
      },
      {
        "opcode": "sub",
        "args": [
          "%28",
          "%29"
        ],
        "result": "%28"
      },
      {
        "opcode": "jz",
        "args": [
          "%28",
          "%.L43"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L42"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L42"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          13
        ],
        "result": "%30"
      },
      {
        "opcode": "print",
        "args": [
          "%30"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L44"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L43"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L44"
        ],
        "result": null
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%30"
      },
      {
        "opcode": "copy",
        "args": [
          "%0"
        ],
        "result": "%31"
      },
      {
        "opcode": "sub",
        "args": [
          "%30",
          "%31"
        ],
        "result": "%30"
      },
      {
        "opcode": "jnz",
        "args": [
          "%30",
          "%.L46"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L45"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L45"
        ],
        "result": null
      },
      {
        "opcode": "const",
        "args": [
          14
        ],
        "result": "%32"
      },
      {
        "opcode": "print",
        "args": [
          "%32"
        ],
        "result": null
      },
      {
        "opcode": "jmp",
        "args": [
          "%.L47"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L46"
        ],
        "result": null
      },
      {
        "opcode": "label",
        "args": [
          "%.L47"
        ],
        "result": null
      }
    ],
    "temps": [
      "%0",
      "%1",
      "%2",
      "%3",
      "%4",
      "%4",
      "%5",
      "%6",
      "%6",
      "%7",
      "%8",
      "%9",
      "%8",
      "%8",
      "%8",
      "%9",
      "%10",
      "%10",
      "%11",
      "%12",
      "%12",
      "%13",
      "%14",
      "%14",
      "%15",
      "%16",
      "%16",
      "%17",
      "%18",
      "%18",
      "%19",
      "%20",
      "%20",
      "%21",
      "%22",
      "%22",
      "%23",
      "%24",
      "%25",
      "%26",
      "%26",
      "%27",
      "%28",
      "%28",
      "%29",
      "%30",
      "%30",
      "%31",
      "%32"
    ],
    "labels": [
      "%.L0",
      "%.L1",
      "%.L2",
      "%.L3",
      "%.L4",
      "%.L5",
      "%.L6",
      "%.L7",
      "%.L8",
      "%.L9",
      "%.L10",
      "%.L11",
      "%.L12",
      "%.L13",
      "%.L14",
      "%.L15",
      "%.L16",
      "%.L17",
      "%.L18",
      "%.L19",
      "%.L20",
      "%.L21",
      "%.L22",
      "%.L23",
      "%.L24",
      "%.L25",
      "%.L26",
      "%.L27",
      "%.L28",
      "%.L29",
      "%.L30",
      "%.L31",
      "%.L32",
      "%.L33",
      "%.L34",
      "%.L35",
      "%.L36",
      "%.L37",
      "%.L38",
      "%.L39",
      "%.L40",
      "%.L41",
      "%.L42",
      "%.L43",
      "%.L44",
      "%.L45",
      "%.L46",
      "%.L47"
    ]
  }
]
