<template>
  <div class="row">
    <div class="col-8">
      <draggable
        tag="transition-group"
        :componentData="componentData"
        :list="travel"
        class="list-group"
        draggable=".item"
        :animation="100"
        @start="dragging = true"
        @end="dragging = false"
      >
        <div class="list-group-item item show-rm" v-for="(element,index) in travel" :key="index">
          <div width="400px">
          <base-input v-model="travel[index].location" class="input-list"></base-input>
          <base-input v-model="travel[index].location" class="input-list"></base-input>
          <base-input v-model="travel[index].location" class="input-list"></base-input>
          <i class="ni ni-fat-remove icon-rm" @click="travel.splice(index, 1)"></i>
          </div>
        </div>

        <div
          slot="footer"
          class="btn-group list-group-item"
          role="group"
          aria-label="Basic example"
          key="footer"
        >
          <button class="btn btn-secondary" @click="add">Add</button>
        </div>
      </draggable>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
export default {
  name: "draggablelist",
  display: "Footer slot",
  order: 12,
  components: {
    draggable
  },
  props: {
    travel: Array
  },
  data() {
    return {
      dragging: false,
      componentData: {
        props: {
          type: "transition",
          name: "flip-list"
        }
      }
    };
  },
  methods: {
    add: function() {
      this.travel.push({ location: "", coordinate: "" });
    }
  }
};
</script>
<style scoped>
.input-list{
  width: 50%;
}

.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}

.icon-rm {
  display: none;
  position: relative;
  margin-top: 10px;
  margin-left: 10px;
  font-size: 150%;
  transition: transform 0.2s;
}

.icon-rm:hover {
  transform: scale(1.2);
}

.show-rm:hover .icon-rm {
  display: inline-block;
}
</style>