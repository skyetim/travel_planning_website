<template>
  <div class="table-responsive">
    <table class="table tablesorter" :class="tableClass">
      <thead :class="theadClasses">
        <tr>
          <slot name="columns" :columns="columns">
            <th v-for="(column, index) in columns" :key="index">{{column}}</th>
          </slot>
          <th>操作</th>
        </tr>
      </thead>
      <tbody class="tbodyClasses">
        <tr v-for="(item,index) in data" :key="index">
          <slot :row="item" :index="index">
            <td v-for="(column, key) in item" :key="key">
              {{item[key]}}
              <input v-show="seen" type="text" v-model="data[index][key]">
            </td>
          </slot>
          <td>
            <button @click="del(index)" class="btn btn-danger btn-sm">删除</button>
            <button @click="update()" class="btn btn-info btn-sm">编辑</button>
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
      seen: false
    }
  },
  props: {
    data: {
      type: Array,
      default: () => [],
      description: "Table data"
    },
    columns: {
      type: Array,
      default: () => [],
      description: "Table headers"
    },
    type: {
      type: String, // striped | hover
      default: "",
      description: "Whether table is striped or hover type"
    },
    theadClasses: {
      type: String,
      default: '',
      description: '<thead> css classes'
    },
    tbodyClasses: {
      type: String,
      default: '',
      description: '<tbody> css classes'
    }
  },
  computed: {
    tableClass() {
      return this.type && `table-${this.type}`;
    }
  },
  methods: {
    // 添加
    addBox: function() {
      var newLine = new Array(this.columns);
      for (var i = 0; i < this.columns.length; ++i) {
        newLine[i] = "";
      }
      this.data.push(newLine);
    },
    //删除
    del: function(index) {
      this.data.splice(index, 1);
    },
    update: function(){
      this.seen = true;
    }
  }
};
</script>

<style scoped>
</style>