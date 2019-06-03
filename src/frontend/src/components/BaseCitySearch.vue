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
          if (this.$session.exists()) {
            this.$http.post('http://139.162.123.242:9000/api/address_to_city_list', {
                address: this.value
          }).then(function (response) {
              if (response.status === 200) {
                if (response.body.status == this.$status['normal']){
                    this.select.show = true;
                    this.select.options = response.body.city_list;
                    this.generate_result();
                } else if (response.body.status == this.$status['user_anthorization_error']) {
                  window.alert('用户登录信息有误, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['user_session_timeout']){
                  window.alert('用户长时间未操作, 自动退出, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else {
                  console.error('获取信息时发生未知错误', response.body);
                }
              } else {
                console.error('网络连接有问题', response.body);
              }
          }, function (err) {
              console.error('err', err);
            }); 
          } else {
            window.alert('用户已退出, 请重新登录');
            this.$router.push('/login');
          }  
        }, 
        generate_result(){
            if (this.select.options.length()==0){
              this.$emit('search-failure', '找不到该城市');
            }
            let best_option = this.select.options[0];
            this.$emit('search-success', best_option['city_id'], best_option['country_name']+' '+best_option['province_name']+' '+best_option['city_name']);
        }
    }
}
</script>
