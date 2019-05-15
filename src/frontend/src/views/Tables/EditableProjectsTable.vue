<template>
  <div class="card shadow">
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
          <th></th>
          <th>行迹</th>
          <th>开始</th>
          <th>结束</th>
          <th>计划</th>
          <th>行程</th>
          <th>同伴</th>
        </template>

        <template slot-scope="{row}">
          <th scope="row">
            <i class="ni ni-settings-gear-65 icon-edit" @click="editTravel(row)"></i>
            <i class="ni ni-fat-remove icon-del" @click="del(row)"></i>
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

    <modal :show.sync="edit.modal">
      <template slot="header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
      </template>
      <div>
        <div class="row">
          <base-input alternative class="mb-3" v-model="editRow.name" addon-left-icon="ni ni-send"></base-input>
          <i
            :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
            @click="edit.collapsed=!edit.collapsed"
          ></i>
          <div :class="[edit.collapsed?'collapse': 'expand']">
            <div class="col">
              <draggablelist :travel="editRow.travel"></draggablelist>
            </div>
          </div>
        </div>

        <div class="row">
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
        </div>
      </div>
      <template slot="footer">
        <base-button type="secondary" @click="edit.modal = false">Close</base-button>
        <base-button type="primary">Save changes</base-button>
      </template>
    </modal>
  </div>
</template>

<script>

import "@/assets/vendor/nucleo/css/nucleo.css";
import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
import "@/assets/scss/argon.scss";
import moment from "moment";

var statusType = ["success", "info", "warning", "danger"];
var status = ["completed", "on schedule", "pending", "delayed"];

var edit = {
  modal: false,
  collapsed: true
};

export default {
  name: "edit-projects-table",
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
      this.editRow = this.tableData[this.tableData.length - 1];
      this.edit.modal = true;
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
      this.editRow = row;
      this.edit.modal = true;
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

<style scoped>
.mb-3 {
  width: 400px;
}
.col {
  width: 400px;
}

/* icons */
.icon-expand {
  position: relative;
  margin: 10px;
  font-size: 150%;
  transition: transform 0.2s;
}

.icon-expand:hover {
  transform: scale(1.2);
}

.icon-del {
  font-size: 150%;
  color: #ff0000;
  transition: transform 0.2s;
}

.icon-del:hover {
  transform: scale(1.2);
  color: #ff4d4d;
}

.icon-edit {
  font-size: 120%;
  transition: transform 0.2s;
}

.icon-edit:hover {
  transform: scale(1.2);
}

/* collapse and expand */
.collapse {
  padding: 18px;
  display: none;
  overflow: hidden;
  background-color: #ffffff;
}

.expand {
  padding: 18px;
  display: block;
  overflow: hidden;
  background-color: #ffffff;
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
  background-color: #ffffff;
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

/* modal input*/
</style>