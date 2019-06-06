<template>
    <div>
        <div :key="key" class="text-default component-name" v-for="(comp, key) in $docs">
            - {{comp.name}}
        </div>
    </div>
</template>

<script>
    export default {
        name: ''
    }
</script>

<style lang="scss" scoped>
    .component-name {
        height: 30px;
        font-size: 24px;
    }

    .components-table {
        width: 100%;
    }
</style>
