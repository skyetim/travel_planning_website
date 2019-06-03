<template>
<div>
    <base-city-search input_placeholder='请输入你的常住地'
                      button_name='搜索'
                      v-model='resident_city'
    />
    <p>{{resident_city}}</p>
</div>
</template>
<script>
    import BaseCitySearch from './BaseCitySearch'
    export default {
        name: 'test',
        data() {
            return {
                resident_city: '北京市',
                fruit: '苹果'
            }
        },
        components: {
            'base-city-search': BaseCitySearch
        }, 
        methods: {
            
        }
    }
</script>
