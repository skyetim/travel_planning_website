<template>
  <div class="card shadow" :class="type === 'dark' ? 'bg-default': ''">
    <div class="card-header border-0" :class="type === 'dark' ? 'bg-transparent': ''">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0" :class="type === 'dark' ? 'text-white': ''">
            {{title}}
            <small
              padding-left="5px"
              class="text-muted"
            >点击编辑表格</small>
          </h3>
        </div>
        <div class="col text-right">
          <base-button type="primary" size="sm" @click="addBox()">添加新的行程</base-button>
          <base-button
            type="primary"
            size="sm"
            @click="edit.del=!edit.del"
          >{{edit.del? "删除完成": "选择删除"}}</base-button>
        </div>
      </div>
    </div>

    <div class="table-responsive">
      <editable
        ref="editable"
        class="table align-items-center table-flush"
        :class="type === 'dark' ? 'table-dark': ''"
        :thead-classes="type === 'dark' ? 'thead-dark': 'thead-light'"
        tbody-classes="list"
        :data="tableData"
      >
        <template slot="columns">
          <th>行迹</th>
          <th>时间</th>
          <th>计划</th>
          <th>行程</th>
          <th></th>
          <th>{{edit.del? "": "同伴"}}</th>
        </template>

        <template slot-scope="{row}">
          <th scope="row">
            <div class="media align-items-center">
              <div class="media-body">
                <base-dropdown :title="row.name">
                  <li 
                    v-for="(place,index) in row.travel" 
                    :key="index"
                    @mouseover="editNames[index]=true"
                    @mouseleave="editNames[index]=false"
                  >
                    <a class="dropdown-item">
                      <span>{{place.location}}</span>
                    </a>
                    <i class="ni ni-ruler-pencil icon-edit" v-show="editNames[index]" @click="editTravel(row)"></i>
                    <i class="ni ni-fat-add icon-edit" v-show="editNames[index]" @click="editTravel(row)"></i>
                    <i class="ni ni-ruler-pencil " v-show="editNames[index]" @click="editTravel(row)"></i>
                  </li>
                </base-dropdown>
              </div>
            </div>
          </th>

          <td>
            <base-input class="inputclick" addon-left-icon="ni ni-calendar-grid-58">
              <flat-picker
                slot-scope="{focus, blur}"
                @on-open="focus"
                @on-close="blur"
                :config="{allowInput: false, mode: 'range'}"
                class="form-control datepicker"
                v-model="row.dates.range"
              ></flat-picker>
            </base-input>
          </td>

          <td>
            <base-dropdown>
              <base-button slot="title" type="secondary" class="dropdown-toggle">
                <badge class="badge-dot mr-4" :type="statusType[row.status]">
                  <i :class="`bg-${statusType[row.status]}`"></i>
                  <span class="status">{{status[row.status]}}</span>
                </badge>
              </base-button>
              <li v-for="(n,index) in [0, 1, 2, 3]" :key="index" @click="changeStatus(n, row)">
                <a class="dropdown-item">
                  <i :class="`bg-${statusType[n]}`"></i>
                  <span class="status">{{status[n]}}</span>
                </a>
              </li>
            </base-dropdown>
          </td>

          <td>
            <div>{{displayStatus(row.dates.range)}}</div>
          </td>

          <td class="text-right">
            <i class="ni ni-fat-remove icon-del" v-show="edit.del" @click="del(row)"></i>
          </td>

          <td>
            <div class="avatar-group" v-show="!edit.del">
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
    <div
      class="card-footer d-flex justify-content-end"
      :class="type === 'dark' ? 'bg-transparent': ''"
    >
      <base-pagination total="30"></base-pagination>
    </div>
    <div>{{tableData}}</div>
  </div>
</template>

<script>
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import "@/assets/vendor/nucleo/css/nucleo.css";
import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
import "@/assets/scss/argon.scss";
import moment from "moment";

var statusType = ["success", "info", "warning", "danger"];
var status = ["completed", "on schedule", "pending", "delayed"];

var show = {
  travel: false
};

var edit = {
  name: [],
  budget: false,
  del: false,
  prog: false,
  completion: 0
};

function compareRow(row1, row2) {
  if (Object.keys(row1).length != Object.keys(row2).length) {
    return false;
  } else {
    var isEqual = true;
    var keys = Object.keys(row1);
    keys.forEach(function(key) {
      if (row1[key] != row2[key]) {
        isEqual = false;
      }
    });

    return isEqual;
  }
}

export default {
  name: "edit-projects-table",
  components: { flatPicker },
  data() {
    return {
      statusType: statusType,
      status: status,
      edit: edit,
      show: show
    };
  },
  props: {
    type: {
      type: String
    },
    title: String,
    location: String,
    tableData: Array
  },
  computed: {
    editNames: function(){
      var names = [];
      for(var i=0; i<this.tableData.travel.length; ++i){
        names.push(false);
      }
      return(names);
    }
  },
  methods: {
    addBox: function() {
      var newLine = {
        location: "输入地点",
        dates: { range: "2018-07-17 to 2018-07-19" },
        status: 0,
        coordinate: []
      };
      this.tableData.push(newLine);
    },
    displayStatus: function(range) {
      var begin = moment(range.split(" ")[0]);
      var end = begin;
      if (range.split(" ").length == 3) {
        end = moment(range.split(" ")[2]);
      }
      var today = moment(Date());
      if (begin.isBefore(today) && today.isBefore(end)) {
        return "行程中";
      } else if (end.isBefore(today)) {
        return "";
      } else {
        return "距离行程开始" + begin.diff(today, "days").toString() + "天";
      }
    },
    editTravel: function(row){
      alert(row);
    },
    changeStatus: function(n, row) {
      row.status = n;
    },
    del: function(row) {
      for (var i = 0; i < this.tableData.length; ++i) {
        if (compareRow(row, this.tableData[i]) == true) {
          this.tableData.splice(i, 1);
          break;
        }
      }
    }
  }
};
</script>

<style>
.inputclick {
  padding-top: 10px;
  width: 240px;
  height: 40px;
  align-self: center；;
}

.icon-del {
  padding-top: 10px;
  font-size: 30px;
  color: #ff0000;
}

.icon-del:hover {
  padding-top: 5px;
  font-size: 35px;
  color: #ff4d4d;
}

.icon-edit:hover{
  padding-top: 5px;
  font-size: 15px;
}
</style>