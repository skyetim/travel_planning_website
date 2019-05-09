<template>
  <div class="card shadow">
    <div>{{tableData}}</div>
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">
            {{title}}
            <small padding-left="5px" class="text-muted">点击编辑表格</small>
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
        :thead-classes="thead-light"
        tbody-classes="list"
        :data="tableData"
      >
        <template slot="columns">
          <th>行迹</th>
          <th>开始</th>
          <th>结束</th>
          <th>计划</th>
          <th>行程</th>
          <th>{{edit.del? "": "同伴"}}</th>
          <th></th>
        </template>

        <template slot-scope="{row}">
          <th scope="row" class="show-edit">
            <div>
              <div>
                {{row.name}}
                <i class="ni ni-settings-gear-65 icon-edit" @click="editTravel(row)"></i>
              </div>
            </div>
          </th>

          <td>
            <div>{{row.dates.start}}</div>
          </td>

          <td>
            <div>{{row.dates.end}}</div>
          </td>

          <td class="show-edit">
            <div>
              <div>
                <badge class="badge-dot mr-4" :type="statusType[row.status]">
                  <span class="status">{{status[row.status]}}</span>
                </badge>
              </div>
            </div>
          </td>

          <td>
            <div>{{displayStatus(row.dates)}}</div>
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

          <td class="text-right">
            <i class="ni ni-fat-remove icon-del" v-show="edit.del" @click="del(row)"></i>
          </td>
        </template>
      </editable>
    </div>

    <modal :show.sync="edit.modal">
      <template slot="header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
      </template>
      <form role="form">
        <div class="row">
        <base-input alternative class="mb-3 name-input" v-model="editRow.name" addon-left-icon="ni ni-send"></base-input>
          <i :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']" @click="edit.collapsed=!edit.collapsed"></i>        
        </div>
        <base-input alternative class="mb-3" addon-left-icon="ni ni-calendar-grid-58">
          <flat-picker
            slot-scope="{focus, blur}"
            @on-open="focus"
            @on-close="blur"
            :config="{allowInput: true}"
            class="form-control datepicker"
            v-model="editRow.dates.start"
          ></flat-picker>
        </base-input>
        <base-input alternative class="mb-3" addon-left-icon="ni ni-calendar-grid-58">
          <flat-picker
            slot-scope="{focus, blur}"
            @on-open="focus"
            @on-close="blur"
            :config="{allowInput: true}"
            class="form-control datepicker"
            v-model="editRow.dates.end"
          ></flat-picker>
        </base-input>
        <div class="dropdown">
          <base-input
            alternative
            class="mb-3"
            v-model="status[editRow.status]"
            addon-left-icon="ni ni-tag"
          ></base-input>
          <div class="dropdown-content">
            <li v-for="(n,index) in [0, 1, 2, 3]" :key="index" @click="changeStatus(n, editRow)">
              <a class="dropdown-item">
                <span class="status">{{status[n]}}</span>
              </a>
            </li>
          </div>
        </div>
        <base-input alternative class="mb-3" v-model="editRow.name" addon-left-icon="ni ni-send"></base-input>
      </form>
      <template slot="footer">
        <base-button type="secondary" @click="edit.modal = false">Close</base-button>
        <base-button type="primary">Save changes</base-button>
      </template>
    </modal>
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

var edit = {
  modal: false,
  del: false,
  collapsed: true
};

export default {
  name: "edit-projects-table",
  components: { flatPicker },
  data() {
    return {
      statusType: statusType,
      status: status,
      edit: edit,
      editRow: {
        name: "输入地点",
        travel: [],
        dates: { start: "2019-01-01", end: "2019-01-01" },
        status: 0
      }
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
  methods: {
    addBox: function() {
      var newLine = {
        name: "输入地点",
        travel: [],
        dates: { start: "2019-01-01", end: "2019-01-01" },
        status: 0
      };
      this.tableData.push(newLine);
    },
    displayStatus: function(dates) {
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
    editTravel: function(row) {
      this.edit.modal = true;
      this.editRow = row;
    },
    changeStatus: function(n, row) {
      row.status = n;
    },
    del: function(row) {
      for (var i = 0; i < this.tableData.length; ++i) {
        if (row == this.tableData[i]) {
          this.tableData.splice(i, 1);
          break;
        }
      }
    }
  }
};
</script>

<style>
.name-input{
  width: 90%;
}

.icon-expand{
  margin-top: 10px;
  font-size: 150%;
}

.icon-del {
  padding-top: 10px;
  font-size: 30px;
  color: #ff0000;
  transition: transform 0.2s;
}

.icon-del:hover {
  transform: scale(1.5);
  color: #ff4d4d;
}

.icon-edit {
  position: absolute;
  font-size: 90%;
  display: none;
  transition: transform 0.2s;
}

.icon-edit:hover {
  transform: scale(1.5);
}

.show-edit:hover .icon-edit {
  display: inline-block;
  margin-left: 10px;
  margin-top: 5px;
}

/* table fiexed */
.fixed {
  width: 80px;
}

/* Dropdown Button */
/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {
  background-color: #ddd;
}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {
  display: block;
}
</style>