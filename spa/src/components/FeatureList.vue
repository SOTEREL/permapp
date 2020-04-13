<template>
  <div class="features">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <fish-tree
      v-else
      :data="treeData"
      multiple
      expand
      @item-checked="categoryCheckedHandler"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      loading: true,
      error: null,
    };
  },

  computed: {
    ...mapState({
      features: state => state.map.features,
      featureTypes: state => state.map.featureTypes,
      categories: state => state.map.categories,
      shownFeatureIds: state => state.map.view.features,
    }),
    treeData() {
      return this.categories.map(this.catToTreeElement);
    },
  },

  created() {
    this.load();
  },

  methods: {
    async load() {
      this.loading = true;
      this.error = null;
      try {
        await this.$store.dispatch("map/loadFeatures");
      } catch (e) {
        this.error = e;
      } finally {
        this.loading = false;
      }
    },

    catToTreeElement(cat) {
      const isType = cat.sub_categories === undefined;
      return {
        title: cat.name,
        key: (isType ? "type" : "category") + "-" + cat.id,
        children: isType
          ? this.getTreeFeatures(cat.id)
          : this.getTreeSubCats(cat),
      };
    },

    getTreeSubCats(cat) {
      let children = [];
      for (let subCat of cat.sub_categories) {
        children.push(this.catToTreeElement(subCat));
      }
      for (let type of cat.feature_types) {
        children.push(this.catToTreeElement(type));
      }
      return children;
    },

    getTreeFeatures(type) {
      return this.$store.getters["map/getTypeFeatures"](type, true).map(
        feat => ({
          title: feat.name,
          key: "feature-" + feat.id,
        })
      );
    },

    getFeatureIdsFromTreeKey(key) {
      let [keyType, id] = key.split("-");
      id = parseInt(id);
      if (keyType === "feature") {
        return [id];
      } else if (keyType === "type") {
        return this.$store.getters["map/getTypeFeatures"](id, true).map(
          feat => feat.id
        );
      }
      return this.$store.getters["map/getCategoryFeatures"](id, true).map(
        feat => feat.id
      );
    },

    categoryCheckedHandler(checkedKeys) {
      const featureIds = checkedKeys
        .map(this.getFeatureIdsFromTreeKey)
        .reduce((acc, ids) => [...acc, ...ids], []);
      this.$store.commit("map/setShownFeatures", []);
      for (let id of featureIds) {
        this.$store.dispatch("map/showFeatureOnTop", id).catch(console.error);
      }
    },
  },
};
</script>

<style scoped></style>
