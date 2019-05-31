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

              <base-input
                @click.native="expand(index)"
                @click.self="collapse(index)"
                v-model="travel[index].location"
                readonly
              ></base-input>
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
          <div class="col-16 dropdown-content" ref="dropdown">
            <div class="col-14">
              <input class="col-8 my-input" type="text" placeholder="查找地点" ref="locStr">
              <button class="my-button" @click="search(index)">查找</button>
              <button class="my-button" @click="collapse(index)">取消</button>
            </div>
            <div
              class="col-8 list-group-item item"
              v-for="(loc,n) in query.result"
              :key="n"
              @click="picked(index, loc)"
            >{{loc}}</div>
            <div class="col-8 list-group-item item">{{query.status}}</div>
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

var search_dummy = ["上海市", "上饶市", "上虞", "北京市", "台北市"];
var query = {
  dummy: search_dummy,
  status: "",
  result: []
};

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
      },
      query: query
    };
  },
  methods: {
    add: function() {
      this.travel.push({ location: "", coordinate: "", start: "", end: "" });
    },
    search: function(index) {
      this.query.result = [];
      this.query.status="";
      var locStr = this.$refs.locStr[index].value;
      if (locStr == "") {
        this.query.status = "无匹配城市";
        return;
      } else {
        this.query.dummy.forEach(element => {
          if (element.match(locStr)) {
            this.query.result.push(element);
          }
        });
        if(this.query.result.empty()){
          this.query.status = "无匹配城市";
        }
      }
    },
    expand: function(index) {
      this.$refs.dropdown[index].style.display = "block";
    },
    collapse: function(index) {
      this.$refs.dropdown[index].style.display = "none";
    },
    picked: function(index, loc){
      this.travel[index].location = loc;
      this.query.result=[];
      this.collapse(index);
    }
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

.input-list {
  width: 30%;
  margin-right: 5px;
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

/* dropdown */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  transition-duration: 0.4s;
  margin-top: -20px;
  display: none;
  position: relative;
  background-color: #ffffff;
}

/* Show the dropdown menu on click */
.dropdown:hover .dropdown-content {
  display: block;
}

/* input and button */
.my-input {
  display: inline-block;
  border-radius: 2px;
}

.my-button {
  display: inline-block;
  background-color: white;
  border-radius: 2px;
}

.my-button:hover {
  background-color:gray /* Green */;
  color: white;
}
</style>