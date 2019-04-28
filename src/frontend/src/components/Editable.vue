<template>
  <div>
    <button class="btn btn-primary btn-sm addBox" @click="addBox">添加</button>
    <button class="btn btn-sm btn-danger delAll" @click="delAll">批量删除</button>
    <table class="table table-bordered">
      <thead>
        <tr>
          <td>
            <input type="checkbox" @click="allSelect" v-model="checked">
          </td>
          <td>行迹</td>
          <td>时间</td>
          <td>操作</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(person,index) in travel" :key="index">
          <td>
            <input type="checkbox" v-model="selected" v-bind:value="person.time">
          </td>
          <td @click="edit(index)" contenteditable="true">{{person.time}}</td>
          <td @click="edit(index)" contenteditable="true">{{person.loc}}</td>
          <td>
            <button @click="del(index)" class="btn btn-danger btn-sm">删除</button>
            <button @click="update(index)" class="btn btn-info btn-sm">编辑</button>
          </td>
        </tr>
      </tbody>
    </table>

    <fieldset v-show="seen">
      <legend>新增行迹</legend>
      <div class>
        <p>
          <label>地点：</label>
          <input type="text" v-model="newTravel.loc">
        </p>
        <p>
          <label>时间：</label>
          <input type="number" v-model="newTravel.time">
        </p>
        <p>
          <button class="btn btn-success btn-sm submit" @click="add">提交</button>
        </p>
      </div>
    </fieldset>
    <!-- 编辑界面 -->
    <fieldset v-show="editSeen">
      <legend>编辑行迹</legend>

      <div class>
        <p>
          <label>地点：</label>
          <input type="text" v-model="editTravel.loc" >
        </p>
        <p>
          <label>时间：</label>
          <input type="number" v-model="editTravel.time" >
        </p>
        <p>
          <button class="btn btn-success btn-sm submit" @click="editSubmit">提交</button>
        </p>
      </div>
    </fieldset>
  </div>
</template>

<script>

export default {

  name: "editable",
  data(){
    return {
              newTravel: {
                loc: "",
                sage: ""
              },
              seen: false,
              editSeen: false,
              checked: false,
              selected: [],
              editTravel: {
                loc: "",
                sage: ""
              }
            }
  }, 
  props: {
    travel: Array
  },
  methods: {
    // 添加
    addBox: function() {
      this.seen = this.seen == false ? true : false;
    },
    //删除
    del: function(index) {
      this.travel.splice(index, 1);
    },
    //提交
    add: function() {
      //插入到travel中
      this.travel.push(this.newTravel);

      this.newTravel = {};
      this.seen = false;
    },
    //全选
    allSelect: function() {
      if (this.selected.length != this.travel.length) {
        this.selected = [];
        for (var i = 0; i < this.travel.length; i++) {
          this.selected.push(this.travel[i].time);
        }
      } else {
        this.selected = [];
      }
    },
    //批量删除
    delAll: function() {
      for (var j = 0; j < this.selected.length; j++) {
        for (var i = 0; i < this.travel.length; i++) {
          if (this.selected[j] == this.travel[i].time) {
            this.travel.splice(i, 1);
          }
        }
      }
    },
    //编辑
    update: function(index) {
      this.editSeen = true;
      this.editTravel = this.travel[index];
    },
    //编辑后提交
    editSubmit: function() {
      this.editSeen = false;
    }
  },
  watch: {
    selected: function() {
      if (this.selected.length == this.travel.length) {
        this.checked = true;
      } else {
        this.checked = false;
      }
    }
  }
};
</script>

<style scoped>
table tr td {
  text-align: center;
}
.btn-info {
  margin-left: 5px;
}

.add,
.addBox {
  margin: 10px 0px 10px 10px;
}
.submit {
  margin-left: 172px;
}
/*全删*/
.delAll {
  margin-left: 10px;
}
/*新增*/
fieldset {
  margin-left: 10px;
}
</style>