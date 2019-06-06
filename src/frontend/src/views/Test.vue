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
    <friend-table/>
</div>
</template>
<script>
    import FriendTable from './FriendTable'
    export default {
        name: 'test',
        data() {
            return {
                post_data : {
                    email: 'w@w.edu', 
                    pswd_hash : this.$md5('w')
                }
            }
        },
        components: {
            'friend-table': FriendTable
        }, 
        methods: {
            login(){
                let success = function (response){
                    console.log('success');
                    console.log(response);
                };
                let fail = function (response){
                    console.log('success');
                    console.log(response);
                };
                this.$backend_conn('get_user_info', {}, this, success, fail, true);
            }
        }
    }
</script>
