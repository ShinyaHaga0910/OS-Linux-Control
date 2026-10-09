#set page(width: 1200pt, height: 675pt, margin: 46pt, fill: white)
#set text(font: "Noto Sans JP", size: 20pt, fill: rgb("#172033"))

#let note(term, body, fill, stroke) = block(
  width: 250pt,
  height: 150pt,
  inset: 16pt,
  radius: 10pt,
  fill: fill,
  stroke: 2pt + stroke,
  [
    #align(center)[
      #text(font: "Consolas", size: 18pt, weight: "bold", fill: stroke)[#term]
      #v(10pt)
      #text(size: 18pt, weight: "bold")[#body]
    ]
  ]
)

#align(center)[
  #image("../generated/fig16-terminal.svg", width: 1080pt)
  #v(28pt)
  #grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    gutter: 16pt,
    align: center + horizon,
    note("LISTEN", [接続を待ち受けている状態], rgb("#E8F1FF"), rgb("#2563A6")),
    note("0.0.0.0:8080", [ローカルIPアドレスとポート番号], rgb("#FFF0D6"), rgb("#B66516")),
    note("python3", [ソケットを所有するプログラム], rgb("#E5F5EA"), rgb("#23834D")),
    note("pid=2143", [実行中プロセスのPID], rgb("#F0E8FF"), rgb("#6941A5")),
  )
]
