<template>
  <div class="card shadow">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">{{title}}</h3>
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
          <th>可见</th>
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
        <h5 class="modal-title" id="exampleModalLabel">新建行迹</h5>
      </template>
      <div>
        <small class="text-muted text-center">行迹名</small>
        <br>
        <div class="row">
          <div class="col-11 inline-div">
            <base-input placeholder="行迹名" v-model="editRow.name"></base-input>
          </div>
          <div class="inline-div">
            <i
              :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
              @click="edit.collapsed=!edit.collapsed"
            ></i>
          </div>
        </div>
        <div class="row">
          <div :class="[edit.collapsed?'collapse': 'expand']">
            <div class="col-11">
              <draggablelist :travel="editRow.travel"></draggablelist>
            </div>
          </div>
        </div>

        <small class="text-muted text-center">行程状态</small>
        <br>
        <div class="row">
          <div class="col-11">
            <base-input @click.native="expandPicker()" v-model="status[editRow.status]" readonly></base-input>
          </div>
        </div>
        <div class="row" margin-top="-30px">
          <div ref="picker" class="col-11 dropdown-content">
            <div
              class="list-group-item item"
              v-for="(n,index) in [0, 1, 2]"
              :key="index"
              @click="changeStatus(n, editRow)"
            >{{status[n]}}</div>
          </div>
        </div>
      </div>
      <template slot="footer">
        <base-button type="primary" @click="edit.modal = false">Save changes</base-button>
      </template>
    </modal>
  </div>
</template>

<script>
import "@/assets/vendor/nucleo/css/nucleo.css";
import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
import "@/assets/scss/argon.scss";
import moment from "moment";

var statusType = ["danger", "info", "success"];
var status = ["仅自己可见", "好友可见", "所有可见"];

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
        name: "",
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
      this.$refs.picker.style.display = "none";
    },
    del: function(row) {
      for (var i = 0; i < this.tableData.length; ++i) {
        if (row == this.tableData[i]) {
          this.tableData.splice(i, 1);
          break;
        }
      }
    },
    expandPicker: function() {
      this.$refs.picker.style.display = "block";
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

.item {
  margin-top: 0px;
  margin-bottom: 0px;
  padding-top: 0px;
  padding-bottom: 0px;
  cursor: pointer;
}
</style>