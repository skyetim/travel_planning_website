<template>
  <div class="container">
    <div class="card">
      <h3 class="card-header text-center font-weight-bold text-uppercase py-4">Editable table</h3>
      <div class="card-body">
        <mdb-table-editable
          :columns="columns"
          :rows="rows"
          class="text-center"
          striped
          bordered/>
      </div>
    </div>
  </div>
</template>

<script>
  import { mdbTableEditable } from 'mdbvue';
  export default {
    name: 'editable',
    components: {
      mdbTableEditable
    },
    props:{
        row: Array,
        columns: Array
    }
  }
</script>