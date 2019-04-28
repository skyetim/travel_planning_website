<template>
  <div>
    <button class="btn btn-primary btn-sm addBox" @click="addBox">添加</button>
    <button class="btn btn-sm btn-danger delAll" @click="delAll">批量删除</button>
    <table class="table table-bordered">
      <thead>
        <tr>
          <td>
            <input type="checkbox" @click="allSelect" v-model="allChecked">
          </td>
          <td v-for="(header, index) in headers" :key="index" >{{header}}</td>
          <td>操作</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(person,index) in travel" :key="index">
          <td>
            <input type="checkbox" v-model="selected" v-bind:value="index">
          </td>
          <td v-for="(value, key) in person" :key="key">
            <input type="text" v-model="travel[index][key]">
          </td>
          <td>
            <button @click="del(index)" class="btn btn-danger btn-sm">删除</button>
            <button @click="update(index)" class="btn btn-info btn-sm">编辑</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div>{{this.travel}}</div>
  </div>
</template>

<script>

export default {

  name: "editable",
  data(){
    return {
              allChecked: false,
              selected: [],
            }
  }, 
  props: {
    travel: Array,
    headers: Array,
  },
  methods: {
    // 添加
    addBox: function() {
      var newLine = new Array(this.headers);
      for(var i=0; i<this.headers.length; ++i){
        newLine[i] = "";
      }
      this.travel.push(newLine);
    },
    //删除
    del: function(index) {
      this.travel.splice(index, 1);
    },
    //全选
    allSelect: function() {
      if (this.selected.length != this.travel.length) {
        this.selected = [];
        for (var i = 0; i < this.travel.length; i++) {
          this.selected.push(i);
        }
      } else {
        this.selected = [];
      }
    },
    //批量删除
    delAll: function() {
      this.selected = this.selected.sort();
      for (var j = this.selected.length - 1; j > -1; j--) {
          this.travel.splice(this.selected[j], 1);
      }
      this.selected = [];
      this.allChecked = false;
    }
  },
  watch: {
    selected: function() {
      if (this.selected.length == this.travel.length) {
        this.allChecked = true;
      } else {
        this.allChecked = false;
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
</style>