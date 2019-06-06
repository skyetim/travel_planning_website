<template>
  <div class="card shadow">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">{{title}}</h3>
        </div>
      </div>
    </div>
    <div class="table-responsive">
      <editable
        ref="editable"
        class="table align-items-center table-flush"
        :thead-classes="thead-light"
        tbody-classes="list"
        :data="travel_group_list"
      >
        <template slot="columns">
          <th></th>
          <th>行迹</th>
          <th>开始</th>
          <th>结束</th>
          <th>行程</th>
          <th>同伴</th>
        </template>

        <template slot-scope="{row}">
          <th scope="row">
            <base-button type="primary" size="sm" @click="showTravel(row)">详细信息</base-button>
          </th>

          <td>
            <div>
              <div>{{row.name}}</div>
            </div>
          </td>

          <td>
            <div>{{row.dates.start}}</div>
          </td>

          <td>
            <div>{{row.dates.end}}</div>
          </td>

          <td>
            <div>{{displayStatus(row.dates)}}</div>
          </td>

          <td>
            <div class="avatar-group">
              <a
                href="#"
                class="avatar avatar-sm rounded-circle"
                data-toggle="tooltip"
                data-original-title="Ryan Tompson"
              >
                <img alt="Image placeholder" src="img/theme/team-1-800x800.jpg">
              </a>
              <a
                href="#"
                class="avatar avatar-sm rounded-circle"
                data-toggle="tooltip"
                data-original-title="Romina Hadid"
              >
                <img alt="Image placeholder" src="img/theme/team-2-800x800.jpg">
              </a>
              <a
                href="#"
                class="avatar avatar-sm rounded-circle"
                data-toggle="tooltip"
                data-original-title="Alexander Smith"
              >
                <img alt="Image placeholder" src="img/theme/team-3-800x800.jpg">
              </a>
              <a
                href="#"
                class="avatar avatar-sm rounded-circle"
                data-toggle="tooltip"
                data-original-title="Jessica Doe"
              >
                <img alt="Image placeholder" src="img/theme/team-4-800x800.jpg">
              </a>
            </div>
          </td>
        </template>
      </editable>
    </div>

    <modal :show.sync="show.modal">
      <template slot="header">
        <h5 class="modal-title" id="exampleModalLabel">他的行迹</h5>
      </template>
      <div>
        <small class="text-muted text-center">行迹名</small>
        <br>
        <div class="row">
          <div class="col-11 inline-div">
            <base-input placeholder="行迹名" v-model="showRow.name" ref="travel_group_name" readonly></base-input>
          </div>
          <div class="inline-div">
            <i
              :class="['ni', show.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
              @click="show.collapsed=!show.collapsed"
            ></i>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <div :class="[show.collapsed?'collapse': 'expand']">
              <read-only-list :travel="showRow.travel" :gid="showRow.travel_group_id"></read-only-list>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <small class="text-muted text-center">行迹笔记</small>
            <br>
            <b-form-textarea v-model="showRow.travel_group_note" placeholder="去让TA说点什么吧~" readonly></b-form-textarea>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <small class="text-muted text-center">行迹颜色</small>
            <br>
            <button
              slot="title"
              class="btn button-text"
              :style="{backgroundColor:showRow.color.hex, opacity:showRow.color.a}"
            ></button>
          </div>
        </div>
      </div>
      <template slot="footer">
        <base-button
          type="primary"
          @click="show.modal = false;"
        >退出</base-button>
      </template>
    </modal>
  </div>
</template>

<script>
import "@/assets/vendor/nucleo/css/nucleo.css";
import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
import "@/assets/scss/argon.scss";
import moment from "moment";
import readOnlyList from "./utils/readOnlyList.vue";

var show = {
  modal: false,
  collapsed: true
};

export default {
  name: "others-projects-table",
  data() {
    return {
      show: show,
      showRow: null,
      showIndex: null
    };
  },
  components:{
    "read-only-list": readOnlyList
  },
  props: {
    type: {
      type: String
    },
    title: String,
    location: String,
    travel_group_list: Array
  },
  methods: {
    displayStatus: function(dates) {
      if (!dates.start || !dates.end) {
        return "";
      }

      var begin = moment(dates.start);
      var end = moment(dates.end);
      var today = moment(Date());

      if (begin.isBefore(today) && today.isBefore(end)) {
        return "行程中";
      } else if (end.isBefore(today)) {
        return "";
      } else {
        return "距离行程开始" + begin.diff(today, "days").toString() + "天";
      }
    },
    showTravel: function(row) {
      this.showRow = this.copy(row);
      // this.showRow = row;
      this.showIndex = this.indexOf(this.travel_group_list, row);
      this.show.modal = true;
    }
  }
};
</script>

<style scoped>
/* icons */

.icon-expand {
  position: relative;
  margin-top: 10px;
  margin-left: 10px;
  font-size: 150%;
  transition: transform 0.2s;
}

.icon-expand:hover {
  transform: scale(1.2);
}

.icon-show {
  font-size: 120%;
  transition: transform 0.2s;
}

.icon-show:hover {
  transform: scale(1.2);
}

/* collapse and expand */
.collapse {
  display: none;
  overflow: hidden;
  background-color: #ffffff;
}

.expand {
  display: block;
  overflow: hidden;
  background-color: #ffffff;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  z-index: 2;
}

/* modal input*/
.inline-div {
  display: inline-block;
}
</style>