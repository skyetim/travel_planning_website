<template>
    <div class="input-group mb-3">
        <input type="text" class="form-control" :placeholder="input_placeholder" aria-describedby="search" :value='value' @input="$emit('update', $event.target.value)"/>
        <div class="input-group-append">
            <button class="btn btn-outline-primary" type="button" id="search" @click="search()">{{button_name}}</button>
        </div>
        <!-- <v-select :options='select.options' class='form-control'/> -->
    </div>
</template>
<script>
export default {
    name: 'base-city-search', 
    props: {
        input_placeholder: {
            type: String,
            default: '', 
            description: "Input label (text before input)"
        }, 
        button_name: {
            type: String,
            default: 'Button', 
            description: "Button name"
        }, 
        value: {
            type: String, 
            description: 'Input value'
        }
    }, 
    data(){
        return {
            select: {
                show: false, 
                options: []
            }, 
            search_result: null
        };
    }, 
    model: {
        prop: 'value',
        event: 'update'
    }, 
    computed: {

    }, 
    methods: {
        search(){
            var that = this;
            function success(response){
                that.select.show = true;
                that.select.options = response.data.city_list;
                that.generate_result();
            };
            function fail(response){
                console.error('获取信息时发生未知错误', response.data);
            };
            this.$backend_conn('address_to_city_list', {address: this.value}, that, success, fail, false);
        }, 
        generate_result(){
            if (this.select.options.length==0){
              this.$emit('search-failure', '找不到该城市');
            }
            let best_option = this.select.options[0];
            this.$emit('search-success', best_option['city_id'], best_option['country_name']+' '+best_option['province_name']+' '+best_option['city_name']);
        }
    }
}
</script>
