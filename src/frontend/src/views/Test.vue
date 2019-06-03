<template>
<div>
    {{login()}}
</div>
</template>
<script>
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
