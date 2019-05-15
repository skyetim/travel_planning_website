<template>
  <div class="row">
    <div class="col-16">
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
          <div class="col-16">
            <div class="input-list">
              <small class="text-muted text-center">地点</small>
              <br>
              <base-input v-model="travel[index].location"></base-input>
            </div>
            <div class="input-list">
              <small class="text-muted text-center">开始</small>
              <br>
              <base-input>
                <flat-picker
                  slot-scope="{focus, blur}"
                  @on-open="focus"
                  @on-close="blur"
                  :config="{allowInput: true}"
                  class="form-control datepicker"
                  v-model="travel[index].start"
                ></flat-picker>
              </base-input>
            </div>
            <div class="input-list">
              <small class="text-muted text-center">结束</small>
              <br>
              <base-input>
                <flat-picker
                  slot-scope="{focus, blur}"
                  @on-open="focus"
                  @on-close="blur"
                  :config="{allowInput: true}"
                  class="form-control datepicker"
                  v-model="travel[index].end"
                ></flat-picker>
              </base-input>
            </div>
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
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import draggable from "vuedraggable";

export default {
  name: "draggablelist",
  display: "Footer slot",
  order: 12,
  components: {
    draggable,
    flatPicker
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
      this.travel.push({ location: "", coordinate: "", start: "", end: "" });
    }
  }
};
</script>
<style scoped>
.item {
  padding: 10px;
}

.input-list {
  width: 30%;
  margin-right: 5px;
  margin-top: 5px;
  margin-bottom: 0px;
  display: inline-block;
  position: relative;
}

.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}

.icon-rm {
  display: none;
  position: absolute;
  padding-top: 35px;
  padding-left: 5px;
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