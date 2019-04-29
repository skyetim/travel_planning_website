<template>
  <div class="table-responsive">
    <table class="table tablesorter" :class="tableClass">
      <thead :class="theadClasses">
        <tr>
          
          <slot name="columns" :columns="columns">
            <th v-for="(column, index) in columns" :key="index">{{column}}</th>
          </slot>
        </tr>
      </thead>
      <tbody class="tbodyClasses">
        <tr v-for="(item,index) in data" :key="index">
          <slot :row="item" :index="index">
            <td v-for="(column, key) in item" :key="key">
              {{item[key]}}
            </td>
          </slot>
        </tr>
      </tbody>
    </table>
    <div>{{this.travel}}</div>
  </div>
</template>

<script>
export default {
  name: "editable",
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
  }
};
</script>

<style scoped>
</style>