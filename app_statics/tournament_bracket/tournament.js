const data = {
  teams: [
    ["Temp", null],
    ["GiGiLiA", "nullptr"],
    ["abSANT", "ATP_NMH"],
    ["rahn10ejare700", "CSGO"],
    ["A_BIT_MORE", "MNM_AI"],
    ["Void", "RealXD"],
    ["GOLABI", "X_Boys"],
    ["MHN-AI", null],
    ["AI_Winners", null],
    ["Tea_Shirt", "Coders"],
    ["Bayern", "simple"],
    ["Debugger", "Mosenimoon"],
    ["Pioneer", "UnKnown"],
    ["nanosoft", "Ja_Dared"],
    ["Boolean", "Checodara"],
    ["Soloist", null],
  ],
  results: [
    // Winners
    [
      [
        [null, null],
        [8, 7],
        [13,0],
        [7, 4],
        [1, 0],
        [11, 1],
        [4, 10],
        [null, null],
        [null, null],
        [14, 1],
        [4, 1],
        [3, 7],
        [24, 5],
        [6, 3],
        [3, 7],
        [null, null]
      ],
      [
        [6, 3],
        [4, 5],
        [22, 3],
        [3, 9],
        [28, 4],
        [1, 0],
        [8, 5],
        [7, 6],
      ],
      [
        [2, 4],
        [9, 5],
        [6, 5],
        [8, 6]
      ],
      [
        [7, 8],
        [2, 17]
      ],

      [
        [2, 13]
      ]
    ],
    // Losers
    [
      [
        [null, null],
        [6, 7],
        [1, 5],
        [null, null],
        [null, null],
        [51, 0],
        [11, 5],
        [null, null]
      ],
      [
        [0, 55],
        [3, 10],
        [1, 0],
        [6, 20],
        [3, 11],
        [4, 5],
        [6, 7],
        [4, 6]
      ],
      [
        [12, 6],
        [2, 3],
        [8, 5],
        [5, 3]
      ],
      [
        [6, 2],
        [9, 21],
        [1, 4],
        [7, 5]
      ],
      [
        [7, 5],
        [9, 6]
      ],
      [
        [16, 4],
        [1, 5]
      ],
      [
        [12, 4]
      ],
      [
        [11, 3]
      ]
    ],
    // Finals
    [
      [[4,11], [7,4]],
      [[4,9]]
    ]
  ]
}

$(function () {
  $('.tournament').bracket({
    teamWidth: 110,
    scoreWidth: 40,
    // matchMargin: 10,
    // roundMargin: 50,
    init: data
  })
})