<template>
  <div class="card shadow">
    <div class="card-header border-0">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0">{{title}}</h3>
        </div>
        <div class="col text-right">
          <base-button
            type="primary"
            size="sm"
            @click="edit.addMode = true;edit.modal = true;editRow=newTravelGroup();"
          >添加新的行程</base-button>
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
        <h5 class="modal-title" id="exampleModalLabel">{{edit.addMode? "新建行迹" : "修改行迹"}}</h5>
      </template>
      <div>
        <small class="text-muted text-center">行迹名</small>
        <br>
        <div class="row">
          <div class="col-11 inline-div">
            <base-input placeholder="行迹名" v-model="editRow.name" ref="travel_group_name"></base-input>
          </div>
          <div class="inline-div">
            <i
              :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
              @click="edit.collapsed=!edit.collapsed"
            ></i>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <div :class="[edit.collapsed?'collapse': 'expand']">
              <draggablelist :travel="editRow.travel" :gid="editRow.travel_group_id"></draggablelist>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <small class="text-muted text-center">行迹笔记</small>
            <br>
            <b-form-textarea v-model="editRow.travel_group_note" placeholder="说点什么吧~"></b-form-textarea>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <small class="text-muted text-center">行迹颜色</small>
            <br>
            <base-dropdown>
              <button
                slot="title"
                class="btn button-text"
                :style="{backgroundColor:editRow.color.hex, opacity:editRow.color.a}"
              ></button>
              <div>
                <swatches v-model="editRow.color"></swatches>
              </div>
            </base-dropdown>
          </div>
        </div>
      </div>
      <template slot="footer">
        <base-button
          type="primary"
          @click="edit.addMode?add_travel_group(editRow):set_travel_group(editRow, row);edit.modal = false;"
        >保存</base-button>
      </template>
    </modal>
  </div>
</template>

<script>
import "@/assets/vendor/nucleo/css/nucleo.css";
import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
import "@/assets/scss/argon.scss";
import moment from "moment";

var edit = {
  addMode: false,
  modal: false,
  collapsed: true
};

export default {
  name: "edit-projects-table",
  data() {
    return {
      edit: edit,
      editRow: this.newTravelGroup(),
      editIndex: null
    };
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
    editTravel: function(row) {
      this.editRow = this.copy(row);
      // this.editRow = row;
      this.editIndex = this.indexOf(this.travel_group_list, row);
      this.edit.addMode = false;
      this.edit.modal = true;
    },

    del: function(row) {
      var vue = this;
      for (var i = 0; i < this.travel_group_list.length; ++i) {
        if (row == this.travel_group_list[i]) {
          this.$backend_conn(
            "remove_travel_group",
            {
              user_id: this.$session.get("user_id"),
              session_id: this.$session.id().replace("sess:", ""),
              travel_group_id: row.travel_group_id
            },
            vue,
            function(response) {
              vue.travel_group_list.splice(i, 1);
              vue.$emit("update", vue.travel_group_list);
              console.log(response);
            },
            function(response) {
              alert(response.data.error_message);
            },
            false
          );
          break;
        }
      }
    },

    // ajax
    add_travel_group: function(row) {
      var vue = this;
      var backend = this.$backend_conn;
      var session = this.$session;

      backend(
        "add_travel_group",
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_name: row.name,
          travel_group_note: row.travel_group_note,
          travel_group_color: row.color.hex
        },
        vue,
        function(response) {
          row.travel.forEach(travel => {
            backend(
              "add_travel",
              {
                user_id: session.get("user_id"),
                session_id: session.id().replace("sess:", ""),
                travel_group_id: response.data.travel_group_id,
                city_id: travel.city_id,
                date_start: travel.date_start,
                date_end: travel.date_end,
                visibility: travel.visibility,
                travel_note: ""
              },
              vue,
              function(response) {
                travel.travel_id = response.data.travel_id;
                console.log(response);
              },
              function(response) {
                alert(response.data.error_message);
              },
              false
            );
          });
          row.travel_group_id = response.data.travel_group_id;
          vue.travel_group_list.push(vue.copy(row));
          vue.$emit("update", vue.travel_group_list);
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        },
        false
      );
    },

    set_travel_group: function(editRow) {
      var vue = this;
      var backend = this.$backend_conn;
      var session = this.$session;

      backend(
        "set_travel_group_info",
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_id: editRow.travel_group_id,
          travel_group_name: editRow.name,
          travel_group_note: editRow.travel_group_note,
          travel_group_color: editRow.color.hex
        },
        vue,
        function(response) {
          editRow.travel.forEach(travel => {
            backend(
              "set_travel_info",
              {
                user_id: session.get("user_id"),
                session_id: session.id().replace("sess:", ""),
                travel_id: travel.travel_id,
                city_id: travel.city_id,
                date_start: travel.date_start,
                date_end: travel.date_end,
                visibility: travel.visibility,
                travel_note: ""
              },
              vue,
              function(response) {
                console.log(response);
              },
              function(response) {
                alert(response.data.error_message);
              },
              false
            );
          });

          vue.travel_group_list[vue.editIndex] = editRow;
          vue.$emit("update", vue.travel_group_list);
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        },
        false
      );
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
</style>