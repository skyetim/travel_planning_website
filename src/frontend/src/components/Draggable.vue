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
            <i class="ni ni-fat-remove icon-rm" @click="del(index)"></i>
          </div>
          <div class="col-16 dropdown-content" ref="dropdown">
            <div class="col-14">
              <input class="col-8 my-input" type="text" placeholder="查找地点" ref="locStr">
              <button class="my-button" @click="search(index)">查找</button>
              <button class="my-button" @click="collapse(index)">取消</button>
            </div>
            <div
              class="col-8 list-group-item item"
              v-for="(r,n) in query.result"
              :key="n"
              @click="picked(index, r)"
            >{{r.country_name + " "+ r.province_name+ " " + r.city_name}}</div>
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

var query = {
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
      },
      query: query
    };
  },
  methods: {
    add: function() {
      var vue = this;
      var session = this.$session;
      this.travel.push({ location: "", coordinate: "", start: "", end: "" });

      this.$backend.add_travel(
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_id: vue.gid,
          city_id: 1,
          date_start: '20090109',
          date_end: '20090109',
          visibility: 1,
          travel_note: ""
        },
        function(response) {
          vue.travel[vue.travel.length - 1].travel_id = response.data.travel_id;
          alert("success remove travel");
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
          alert("success add travel");
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    },
    search: function(index) {
      var vue = this;
      this.query.result = [];
      this.query.status = "";
      var locStr = this.$refs.locStr[index].value;
      if (locStr == "") {
        this.query.status = "无匹配城市";
        return;
      } else {
        this.$backend.address_to_city(
          { address: locStr },
          function(response) {
            vue.query.result.push({
              city_id: response.data.city_id,
              country_name: response.data.country_name,
              province_name: response.data.province_name,
              city_name: response.data.city_name,
              latitude: response.data.latitude,
              longitude: response.data.longitude
            });
            alert("success: address_to_city");
          },
          function(response) {
            alert(response.data.error_message);
          }
        );
      }
    },
    expand: function(index) {
      this.$refs.dropdown[index].style.display = "block";
    },
    collapse: function(index) {
      this.$refs.dropdown[index].style.display = "none";
    },
    picked: function(index, r) {
      this.travel[index].location = r.city_name;
      this.travel[index].city_id = r.city_id;
      this.travel[index].coordinate = [r.latitude, r.longitude];
      this.query.result = [];
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
  background-color: gray /* Green */;
  color: white;
}
</style>