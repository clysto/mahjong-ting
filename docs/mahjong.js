const SUITS = '条饼万东西南北中发白';
const NUMS = '一二三四五六七八九';

const TILES_TEXT = [
  ['一条', '二条', '三条', '四条', '五条', '六条', '七条', '八条', '九条'],
  ['一饼', '二饼', '三饼', '四饼', '五饼', '六饼', '七饼', '八饼', '九饼'],
  ['一万', '二万', '三万', '四万', '五万', '六万', '七万', '八万', '九万'],
  ['东'],
  ['西'],
  ['南'],
  ['北'],
  ['中'],
  ['发'],
  ['白'],
];

function handCount(hand) {
  return hand.reduce((sum, suit) => sum + suit.reduce((suitSum, count) => suitSum + count, 0), 0);
}

function parseTile(str) {
  if (str.length === 1) {
    return [SUITS.indexOf(str), 0];
  } else {
    return [SUITS.indexOf(str[1]), NUMS.indexOf(str[0])];
  }
}

let TAB3N, TAB3N2;

function gen3n(a, level, table) {
  if (level > 4) {
    return;
  }
  // add a triplet
  for (let i = 0; i < 9; i++) {
    if (a[i] + 3 > 4) {
      continue;
    }
    const b = a.slice();
    b[i] += 3;
    table.add(b.join(','));
    gen3n(b, level + 1, table);
  }
  // add a sequence
  for (let i = 0; i < 7; i++) {
    if (a[i] + 1 > 4 || a[i + 1] + 1 > 4 || a[i + 2] + 1 > 4) {
      continue;
    }
    const b = a.slice();
    b[i] += 1;
    b[i + 1] += 1;
    b[i + 2] += 1;
    table.add(b.join(','));
    gen3n(b, level + 1, table);
  }
}

function gen3n2(table) {
  for (let i = 0; i < 9; i++) {
    const a = Array(9).fill(0);
    a[i] += 2;
    table.add(a.join(','));
    gen3n(a, 1, table);
  }
}

function initTables() {
  const cachedTab3N = localStorage.getItem('TAB3N');
  const cachedTab3N2 = localStorage.getItem('TAB3N2');

  if (cachedTab3N && cachedTab3N2) {
    TAB3N = new Set(JSON.parse(cachedTab3N));
    TAB3N2 = new Set(JSON.parse(cachedTab3N2));
  } else {
    TAB3N = new Set();
    TAB3N2 = new Set();
    TAB3N.add(Array(9).fill(0).join(','));
    gen3n(Array(9).fill(0), 1, TAB3N);
    gen3n2(TAB3N2);

    localStorage.setItem('TAB3N', JSON.stringify(Array.from(TAB3N)));
    localStorage.setItem('TAB3N2', JSON.stringify(Array.from(TAB3N2)));
  }
}

function checkWin(hand) {
  let have3n2 = false;
  for (let s = 0; s < 10; s++) {
    const a = hand[s].join(',');
    if (TAB3N2.has(a)) {
      if (have3n2) {
        return false;
      } else {
        have3n2 = true;
      }
    } else if (!TAB3N.has(a)) {
      return false;
    }
  }
  return true;
}

initTables();

function winTile(hand) {
  let tiles = [];
  // 条 饼 万
  for (let s = 0; s < 3; s++) {
    for (let rank = 0; rank < 9; rank++) {
      if (hand[s][rank] >= 4) {
        continue;
      }
      let handCopy = hand.map((suit) => suit.slice());
      handCopy[s][rank] += 1;
      if (checkWin(handCopy)) {
        tiles.push([TILES_TEXT[s][rank], 4 - hand[s][rank]]);
      }
    }
  }
  // 东 西 南 北 中 发 白
  for (let s = 3; s < 10; s++) {
    if (hand[s][0] >= 4) {
      continue;
    }
    let handCopy = hand.map((suit) => suit.slice());
    handCopy[s][0] += 1;
    if (checkWin(handCopy)) {
      tiles.push([TILES_TEXT[s][0], 4 - hand[s][0]]);
    }
  }
  return tiles;
}

function suggest(hand) {
  let tiles = [];
  for (let s = 0; s < 10; s++) {
    for (let rank = 0; rank < 9; rank++) {
      if (hand[s][rank] < 1) {
        continue;
      }
      let handCopy = hand.map((suit) => suit.slice());
      handCopy[s][rank] -= 1;
      let winTiles = winTile(handCopy);
      if (winTiles.length > 0) {
        let count = 0;
        for (let i = 0; i < winTiles.length; i++) {
          count += winTiles[i][1];
        }
        tiles.push([TILES_TEXT[s][rank], count]);
      }
    }
  }
  tiles.sort((a, b) => b[1] - a[1]);
  return tiles;
}
