#set page(width: 1200pt, height: 675pt, margin: 46pt, fill: white)
#set text(font: "Noto Sans JP", size: 24pt, fill: rgb("#172033"))

#align(center + horizon)[
  #block(
    width: 1080pt,
    inset: 32pt,
    radius: 12pt,
    fill: rgb("#F8FAFD"),
    stroke: 2pt + rgb("#314B6E"),
  )[
    #text(size: 25pt, weight: "bold")[ディレクトリツリーの例（抜粋）]
    #v(24pt)
    #text(font: "Consolas", size: 26pt, fill: rgb("#172033"))[
      #raw("/\n├── home\n│   └── ssm-user\n│       └── jdu-lab\n│           └── m1\n│               └── errors.txt\n├── etc\n└── srv\n    └── jdu-share\n        └── README.txt", block: true)
    ]
  ]
]
