<template>
    <div>
        <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
        <div class="container-fluid d-flex align-items-center">
                <div class="col-lg-7 col-md-10">
                    <h1 class="display-2 text-white">Hi {{this.$session.get('user_name')}}, </h1>
                    <p class="text-white mt-0 mb-5">你可以在这里找到你的好友</p>
                </div>
        </div>
        </base-header>


        <div class="container-fluid mt-5 div-table">
            <div class='input-group'>
                <input type="text" class="form-control" placeholder="请输入他的用户名" aria-label="请输入他的用户名" aria-describedby="button-addon2" v-model="query_user_name">
                <div class="input-group-append">
                    <button class="btn btn-primary" type="button" id="button-addon2" @click="search_friend()">搜索</button>
                </div>
            </div>
        </div>
        <div class="container-fluid mt-5 div-table">
            <div class="row mt-5">
                <div class="col">

                </div>
            </div>
        </div>

    </div>
</template>
<script>
    export default {
        name: 'test',
        data() {
            return {
                query_user_name: ''
            }
        },
        components: {
        }, 
        methods: {
            search_friend(){
                var that = this;
                var data = {
                    query_user_name: this.query_user_name
                }; 
                function success(response){
                    console.log(response.data);
                };
                function fail(response){
                    console.error('获取信息时发生未知错误', response.body);
                };
                this.$backend_conn('get_user_list_by_user_name', data, that, success, fail);
            }

        }
    }
</script>
