import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import ArgonDashboard from './plugins/argon-dashboard'
import { Icon } from "leaflet";
import 'leaflet/dist/leaflet.css';
import VueSession from 'vue-session';
import VueResource from 'vue-resource';
import md5 from 'js-md5';
import {status} from './status';
import {backend} from './backend_config';
import Vuelidate from 'vuelidate';


Vue.use(VueSession);
Vue.use(VueResource);
Vue.use(Vuelidate);
Vue.prototype.$md5 = md5;
Vue.prototype.$status = status;
Vue.prototype.$backend = backend;
Vue.prototype.compare = function(id) {
  return function(obj1, obj2) {
    if (obj1[id] < obj2[id]) {
      return -1;
    } else if (obj1[id] > obj2[id]) {
      return 1;
    } else {
      return 0;
    }
  };
}
Vue.config.silent = true;

Vue.http.options.emulateJSON = true;

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.config.productionTip = false

Vue.use(ArgonDashboard)

new Vue({
  router,
  render: h => h(App), 
  created() {
    this.checkLogin();
  }, 
  methods: {
    checkLogin(){
      if (!this.$session.exists() && this.$route.name!='register') { // 如果没有login且不在register页自动跳转
        this.$router.push('/login');
      } else if (this.$session.exists() && (this.$route.name=='login' || this.$route.name=='register')){ // 如果已经login进入login页自动跳转
        this.$router.push('/');
      }
    }
  }, 
  watch:{
    '$route': 'checkLogin'
  }
}).$mount('#app')
