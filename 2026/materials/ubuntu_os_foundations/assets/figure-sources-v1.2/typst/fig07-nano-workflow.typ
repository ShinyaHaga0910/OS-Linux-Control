#set page(width: 1200pt, height: 675pt, margin: 46pt, fill: white)
#set text(font: "Noto Sans JP", size: 22pt, fill: rgb("#172033"))
#set par(leading: 0.7em)

#let card(number, command, body, fill, stroke) = block(
  width: 184pt,
  height: 310pt,
  inset: 20pt,
  radius: 12pt,
  fill: fill,
  stroke: 2pt + stroke,
  [
    #align(center)[
      #circle(radius: 19pt, fill: stroke)[#text(fill: white, weight: "bold")[#number]]
      #v(14pt)
      #box(inset: (x: 10pt, y: 7pt), radius: 5pt, fill: white, stroke: 1pt + stroke)[
        #text(font: "Consolas", size: 18pt, weight: "bold")[#command]
      ]
      #v(17pt)
      #text(size: 20pt, weight: "bold")[#body]
    ]
  ]
)

#align(center + horizon)[
  #grid(
    columns: (184pt, 34pt, 184pt, 34pt, 184pt, 34pt, 184pt, 34pt, 184pt),
    align: center + horizon,
    card("1", "nano notes.txt", [ファイルを開く], rgb("#E8F1FF"), rgb("#2563A6")),
    text(size: 28pt, fill: rgb("#314B6E"))[→],
    card("2", "文字を入力", [内容を編集する], rgb("#E5F5EA"), rgb("#23834D")),
    text(size: 28pt, fill: rgb("#314B6E"))[→],
    card("3", "Ctrl+O  Enter", [保存する], rgb("#FFF0D6"), rgb("#B66516")),
    text(size: 28pt, fill: rgb("#314B6E"))[→],
    card("4", "Ctrl+X", [nanoを終了する], rgb("#F0E8FF"), rgb("#6941A5")),
    text(size: 28pt, fill: rgb("#314B6E"))[→],
    card("5", "cat notes.txt", [保存結果を読み直す], rgb("#F2F4F7"), rgb("#657187")),
  )
]
