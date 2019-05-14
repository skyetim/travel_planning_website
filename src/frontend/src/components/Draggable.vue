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
            <base-input v-model="travel[index].location" class="input-list"></base-input>
            <base-input class="input-list">
              <flat-picker
                slot-scope="{focus, blur}"
                @on-open="focus"
                @on-close="blur"
                :config="{allowInput: true}"
                class="form-control datepicker"
                v-model="travel[index].start"
              ></flat-picker>
            </base-input>
            <base-input class="input-list">
              <flat-picker
                slot-scope="{focus, blur}"
                @on-open="focus"
                @on-close="blur"
                :config="{allowInput: true}"
                class="form-control datepicker"
                v-model="travel[index].end"
              ></flat-picker>
            </base-input>
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
  margin: 5px;
  width: 30%;
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
  padding-top: 10px;
  padding-left: 10px;
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