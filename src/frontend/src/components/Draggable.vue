<template>
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
      <div class="row">
        <div class="col-10">
          <div class="row">
            <div class="col">
              <small class="text-muted text-center">地点</small>
              <br>

              <base-input
                @click.native="expand(index)"
                @click.self="collapse(index)"
                v-model="travel[index].location"
                readonly
              ></base-input>
            </div>

            <div class="col">
              <small class="text-muted text-center">开始</small>
              <br>
              <base-input>
                <flat-picker
                  slot-scope="{focus, blur}"
                  @on-open="focus"
                  @on-close="blur"
                  :config="{allowInput: true}"
                  class="form-control datepicker"
                  v-model="travel[index].date_start"
                ></flat-picker>
              </base-input>
            </div>
            <div class="col">
              <small class="text-muted text-center">结束</small>
              <br>
              <base-input>
                <flat-picker
                  slot-scope="{focus, blur}"
                  @on-open="focus"
                  @on-close="blur"
                  :config="{allowInput: true}"
                  class="form-control datepicker"
                  v-model="travel[index].date_end"
                ></flat-picker>
              </base-input>
            </div>
            <div class="col">
              <small class="text-muted text-center">可见</small>
              <br>
              <base-input
                v-model="visibility_list[travel[index].visibility]"
                @click.native="expandPicker(index)"
                ref="travel_group_visibility"
                readonly
              ></base-input>
            </div>
          </div>
        </div>
        <div class="col-1">
          <i class="ni ni-fat-remove icon-rm" @click="del(index)"></i>
        </div>
      </div>
      <div ref="picker" class="dropdown-content">
        <div
          class="list-group-item item"
          v-for="(v,n) in ['F', 'P']"
          :key="n"
          @click="changeStatus(v, travel,index)"
        >{{visibility_list[v]}}</div>
      </div>
      <div class="dropdown-content" ref="dropdown">
        <div class="row">
          <div class="col-5">
            <base-input v-model="query.content" placeholder="查找地点"></base-input>
          </div>
          <div class="col-5">
            <div class="row">
              <div class="col">
                <button dislplay="inline-block" class="btn btn-primary" @click="search()">查找</button>
                <button
                  dislplay="inline-block"
                  class="btn btn-primary"
                  @click="collapse(index)"
                >取消</button>
              </div>
            </div>
          </div>
        </div>
        <div
          class="row list-group-item item"
          v-for="(r,n) in query.result"
          :key="n"
          @click="picked(index, r)"
        >{{r.country_name + " "+ r.province_name+ " " + r.city_name}}</div>
        <div class="row list-group-item item">{{query.status}}</div>
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
</template>

<script>
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import draggable from "vuedraggable";

var query = {
  content: "",
  status: "",
  searchMode: false,
  result: []
};

var visibility_list = {
  F: "仅好友可见",
  P: "所有人可见"
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
    travel: Array,
    gid: Number
  },
  data() {
    return {
      visibility_list: visibility_list,
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
    expandPicker: function(index) {
      this.$refs.picker[index].style.display = "block";
    },
    changeStatus: function(v, travel, index) {
      travel[index].visibility = v;
      this.$refs.picker[index].style.display = "none";
    },
    add: function() {
      var vue = this;
      var session = this.$session;
      this.travel.push({
        location: "",
        coordinate: "",
        date_start: "",
        date_end: ""
      });

      this.$backend.add_travel(
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_id: vue.gid,
          city_id: 3,
          date_start: "2009-01-09",
          date_end: "2009-01-09",
          visibility: "P",
          travel_note: ""
        },
        function(response) {
          vue.travel[vue.travel.length - 1].travel_id = response.data.travel_id;
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    },
    del: function(index) {
      var vue = this;
      var session = this.$session;
      this.$backend.remove_travel(
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_id: vue.gid,
          travel_id: vue.travel[index].travel_id
        },
        function(response) {
          vue.travel.splice(index, 1);
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    },
    search: function() {
      var vue = this;
      this.query.result = [];
      this.query.status = "";

      if (this.query.content == "") {
        this.query.status = "无匹配城市";
        return;
      } else {
        this.$backend.address_to_city(
          { address: vue.query.content },
          function(response) {
            vue.query.result.push({
              city_id: response.data.city_id,
              country_name: response.data.country_name,
              province_name: response.data.province_name,
              city_name: response.data.city_name,
              latitude: response.data.latitude,
              longitude: response.data.longitude
            });
            console.log(response);
          },
          function(response) {
            alert(response.data.error_message);
          }
        );
      }
    },
    expand: function(index) {
      if (!this.query.searchMode) {
        this.query.searchMode = true;
        this.$refs.dropdown[index].style.display = "block";
      }
    },
    collapse: function(index) {
      this.query.searchMode = false;
      this.$refs.dropdown[index].style.display = "none";
    },
    picked: function(index, r) {
      this.travel[index].location = r.city_name;
      this.travel[index].city_id = r.city_id;
      this.travel[index].coordinate = [r.latitude, r.longitude];
      this.query.result = [];
      this.query.content = "";
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
  border-radius: 2px;
}

.my-button {
  display: inline-block;
  background-color: white;
  border-radius: 2px;
}

.my-button:hover {
  background-color: gray /* Green */;
  color: white;
}

.dropdown-absolute {
  display: none;
  position: absolute;
  z-index: 2;
}
</style>