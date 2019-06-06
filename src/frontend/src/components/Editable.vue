<template>
    <div class="table-responsive">
        <table :class="tableClass" class="table tablesorter">
            <thead :class="theadClasses">
            <tr>
                <slot :columns="columns" name="columns">
                    <th :key="index" v-for="(column, index) in columns">{{column}}</th>
                </slot>
            </tr>
            </thead>
            <tbody class="tbodyClasses">
            <tr :key="index" v-for="(item,index) in data">
                <slot :index="index" :row="item">
                    <td :key="key" v-for="(column, key) in item">{{item[key]}}</td>
                </slot>
            </tr>
            </tbody>
        </table>
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
                default: "",
                description: "<thead> css classes"
            },
            tbodyClasses: {
                type: String,
                default: "",
                description: "<tbody> css classes"
            }
        },
        computed: {
            tableClass() {
                return this.type && `table-${this.type}`;
            }
        }
    };
</script>

<style>
</style>
