<template>
  <draggable
    tag="transition-group"
    :componentData="componentData"
    :list="travel"
    class="list-group"
    draggable=".item"
    :animation="100"
    @start="dragging = false"
    @end="dragging = false"
  >
    <div class="list-group-item item" v-for="(element,index) in travel" :key="index">
      <div class="row">
        <div class="col-10">
          <div class="row">
            <div class="col">
              <small class="text-muted text-center">地点</small>
              <br>

              <base-input v-model="travel[index].location" readonly></base-input>
            </div>

            <div class="col">
              <small class="text-muted text-center">开始</small>
              <br>
              <base-input v-model="travel[index].date_start" readonly></base-input>
            </div>
            <div class="col">
              <small class="text-muted text-center">结束</small>
              <br>
              <base-input v-model="travel[index].date_end" readonly></base-input>
            </div>
          </div>
        </div>
      </div>
    </div>
  </draggable>
</template>

<script>
import draggable from "vuedraggable";

export default {
  name: "readonly-list",
  display: "Footer slot",
  order: 12,
  components: {
    draggable
  },
  props: {
    travel: Array,
    gid: Number
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
  }
};
</script>
<style scoped>
.item {
  margin-top: 0px;
  margin-bottom: 0px;
  padding-top: 0px;
  padding-bottom: 0px;
  cursor: pointer;
}

.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
</style>