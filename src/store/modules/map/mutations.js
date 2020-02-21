import Vue from "vue";

// Mutations beginning with "_" must be called by an action
export default {
  setup(state, cfg) {
    state.setup = { ...state.setup, ...cfg };
  },
  setBorders(state, borders) {
    state.borders = borders;
  },
  setTiles(state, tiles) {
    Vue.set(state.view, "tiles", tiles);
  },
  _addTiles(state, uniqueTiles) {
    Vue.set(state.view, "tiles", [...state.view.tiles, ...uniqueTiles]);
  },
  removeTiles(state, keysToRemove) {
    let key;
    let tiles = [];
    for (let tile of state.view.tiles) {
      key = typeof tile === "string" ? tile : tile.key;
      if (!keysToRemove.includes(key)) {
        tiles.push(tile);
      }
    }
    Vue.set(state.view, "tiles", tiles);
  },
};
