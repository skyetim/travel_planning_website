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
                <div class="input-group-prepend">
                    <span class="input-group-text">输入姓名搜索用户</span>
                </div>
                <input type="text" class="form-control" placeholder="姓" v-model="query_last_name" @focus="table.alertShow=false">
                <input type="text" class="form-control" placeholder="名" aria-describedby="button-addon2" v-model="query_first_name" @focus="table.alertShow=false">
                <div class="input-group-append">
                    <button class="btn btn-primary" type="button" id="button-addon2" @click="search_friend()">搜索</button>
                </div>
            </div>
        </div>
        <div class="container-fluid mt-5 div-table">
            <!-- <card shadow type='secondary'>
                <div slot="header" class="bg-white border-0">
                    <div class="row align-items-center">
                        <div class="col-8">
                            <h3 class="mb-0">好友搜索结果</h3>
                        </div>
                    </div>
                </div> -->

                <search-table :type='table.type' :title='table.title' :tableData='table.tableData' v-if='table.show'/>
                <base-alert type='default' v-if='table.alertShow' :dismissible='true'> {{table.alertMessage}} </base-alert>
            <!-- </card> -->
        </div>

    </div>
</template>
<script>
import SearchTable from './SearchTable';
    export default {
        name: 'test',
        data() {
            return {
                query_first_name: '', 
                query_last_name: '', 
                table: {
                    type: 'light', 
                    title: '好友搜索结果', 
                    tableData: [], 
                    show: false, 
                    alertShow: false, 
                    alertMessage: ''
                }
            }
        },
        computed: {
            query_user_name () {
                return this.query_last_name + ' ' + this.query_first_name;
            }
        }, 
        components: {
            'search-table': SearchTable
        }, 
        methods: {
            search_friend(){
                var that = this;
                var data = {
                    query_user_name: this.query_user_name
                }; 
                function success(response){
                    if (response.data.count == 0){
                        that.table.show = false;
                        that.table.alertShow = true;
                        that.table.alertMessage = '未找到相关用户! ';
                        return;
                    }
                    that.table.show = true;
                    that.alertShow = false;
                    that.table.tableData = response.data.user_info_list.map(function(user_info_dict){
                        user_info_dict['gender'] = that.$gender[user_info_dict['gender']];
                        user_info_dict['city_name'] = user_info_dict['resident_city']['city_name'];
                        return user_info_dict;
                    });
                };
                function fail(response){
                    console.error('获取信息时发生未知错误', response.body);
                };
                this.$backend_conn('search_user_info_list_by_user_name', data, that, success, fail);
            }

        }
    }
</script>
