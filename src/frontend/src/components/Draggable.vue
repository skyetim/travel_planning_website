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
              <small class="text-muted text-center">仅好友可见</small>
              <br>
              <label class="custom-toggle" style="margin-top:10px;">
                <input
                  type="checkbox"
                  v-model="travel[index].vbool"
                  @click="newChangeStatus(travel, index)"
                >
                <span class="custom-toggle-slider rounded-circle"></span>
              </label>
              <!-- <base-input
                v-model="visibility_list[travel[index].visibility]"
                @click.native="expandPicker(index)"
                ref="travel_group_visibility"
                readonly
              ></base-input>-->
            </div>
          </div>
        </div>
        <div class="col-2">
          <i class="ni ni-fat-remove icon-rm" @click="del(index)"></i>
        </div>
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
      <div>
        <small class="text-muted text-center">{{city_check(travel, index)?"邀请同行好友吧~": "同行好友"}}</small>
        <br>
        <friend-list :friend_info_list="friend_info_list"  :travel_id="travel[index].travel_id"></friend-list>
        <div class="row">
          <div class="col">
            <base-alert type="warning" v-show="city_check(travel, index)">
              <span class="alert-inner--icon" margin-right="10px">
                <i class="ni ni-bell-55"></i>
              </span>
              <span class="alert-inner--text">
                <strong>注意!</strong> 请点击查找城市名!
              </span>
            </base-alert>

            <base-alert type="warning" v-show="time_check(travel, index)">
              <span class="alert-inner--icon">
                <i class="ni ni-bell-55" style="{margin-right:10px;}">
                  <strong>注意!</strong>
                </i>
              </span>
              <span class="alert-inner--text">行程开始日期应在结束日期之前!</span>
            </base-alert>
          </div>
        </div>
      </div>
    </div>

    <div
      slot="footer"
      class="btn-group list-group-item"
      role="group"
      aria-label="Basic example"
      key="footer"
    >
      <button class="btn btn-secondary" @click="add">添加城市</button>
    </div>
  </draggable>
</template>

<script>
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import draggable from "vuedraggable";
import moment from "moment";
import FriendList from "./FriendList";

var query = {
  content: "",
  status: "",
  searchMode: false,
  result: []
};

export default {
  name: "draggablelist",
  display: "Footer slot",
  order: 12,
  components: {
    draggable,
    flatPicker,
    "friend-list": FriendList
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
      query: query,
      friend_info_list: []
    };
  },
  created: function() {
    var backend = this.$backend_conn;
    var vue = this;
    backend(
      "get_friend_list",
      {},
      vue,
      function(response) {
        response.data.friend_list.forEach(friend => {
          backend(
            "get_friend_user_info",
            { friend_user_id: friend.user_id },
            vue,
            function(response1) {
              vue.friend_info_list.push({
                user_id: friend.user_id,
                user_name: response1.data.user_name,
                avatar_url: response1.data.avatar_url
              });
            },
            function(response1) {
              alert(response1.data.error_message);
            }
          );
        });
      },
      function(response) {
        alert(response.data.error_message);
      }
    );
  },
  methods: {
    time_check: function(travel, index) {
      return travel[index].date_start > travel[index].date_end;
    },
    city_check: function(travel, index) {
      return travel[index].location == "";
    },
    newChangeStatus: function(travel, index) {
      travel[index].vbool = !travel[index].vbool;
      travel[index].visibility = travel[index].vbool ? "F" : "P";
    },
    add: function() {
      var vue = this;
      var session = this.$session;
      this.travel.push(this.newTravel());
      this.$set(
        this.travel,
        this.travel.length - 1,
        this.travel[this.travel.length - 1]
      );

      if (vue.gid != null) {
        this.$backend_conn(
          "add_travel",
          {
            user_id: session.get("user_id"),
            session_id: session.id().replace("sess:", ""),
            travel_group_id: vue.gid,
            city_id: 3,
            date_start: moment(Date()).format("YYYY-MM-DD"),
            date_end: moment(Date()).format("YYYY-MM-DD"),
            visibility: "P",
            travel_note: ""
          },
          vue,
          function(response) {
            vue.travel[vue.travel.length - 1].travel_id =
              response.data.travel_id;
            vue.$set(vue.travel, vue.travel.length-1, vue.travel[vue.travel.length - 1]);
            console.log(response);
          },
          function(response) {
            alert(response.data.error_message);
          },
          false
        );
      }
    },
    del: function(index) {
      var vue = this;
      var session = this.$session;
      this.$backend_conn(
        "remove_travel",
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_id: vue.gid,
          travel_id: vue.travel[index].travel_id
        },
        vue,
        function(response) {
          vue.travel.splice(index, 1);
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        },
        false
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
        this.$backend_conn(
          "address_to_city",
          { address: vue.query.content },
          vue,
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
          },
          false
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
/* .item {
  margin-top: 0px;
  margin-bottom: 0px;
  padding-top: 0px;
  padding-bottom: 0px;
  cursor: pointer;
} */

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

.custom-alert {
  height: 20px;
}
</style>