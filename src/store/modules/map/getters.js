export default {
  getTileKey: state => tile => (typeof tile === "string" ? tile : tile.key),
  getTileProps: state => tile => (typeof tile === "string" ? {} : tile.props),
  tilesAsObjects: (state, getters) =>
    state.view.tiles.map(t => ({
      key: getters.getTileKey(t),
      props: getters.getTileProps(t),
    })),
  tilesKeys: state =>
    state.view.tiles.map(t => {
      return typeof t === "string" ? t : t.key;
    }),
  hasTile: (state, getters) => key => getters.tilesKeys.includes(key),
};
