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
    ["Pionear", "UnKnown"],
    ["nanosoft", "Ja_Dared"],
    ["Boolean", "Checodara"],
    ["Soloist", null],
  ],
  results: [
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
        [],
        [],
        [3, 9],
        [28, 4],
        [],
        [],
        [7, 6],
      ]
    ],
    [],
    []
  ]
  // results: [
  //   [
  //     [
  //       []
  //     ]
  //   ],
  //   [],
  //   []
  // ]
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