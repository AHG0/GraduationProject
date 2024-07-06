import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueRouter from 'vue-router';
import VueResourceEsm from "vue-resource";
import App from "../App";
import axios from 'axios';
import cookie from 'vue-cookie';
import animate from "animate.css"
import * as Echarts from 'echarts'
import {Keyframes} from 'vue-keyframes';

axios.defaults.baseURL = 'http://localhost:8080/'

Vue.prototype.$echarts = Echarts
Vue.prototype.$bus = new Vue()
Vue.use(animate)
Vue.use(VueResourceEsm)

Vue.use(Keyframes);

Vue.prototype.$axios = axios
Vue.use(VueRouter)
import {
    Pagination,
    Dialog,
    Autocomplete,
    Dropdown,
    DropdownMenu,
    DropdownItem,
    Menu,
    Submenu,
    MenuItem,
    MenuItemGroup,
    Input,
    InputNumber,
    Radio,
    RadioGroup,
    RadioButton,
    Checkbox,
    CheckboxButton,
    CheckboxGroup,
    Switch,
    Select,
    Option,
    OptionGroup,
    Button,
    ButtonGroup,
    Table,
    TableColumn,
    DatePicker,
    TimeSelect,
    TimePicker,
    Popover,
    Tooltip,
    Breadcrumb,
    BreadcrumbItem,
    Form,
    FormItem,
    Tabs,
    TabPane,
    Tag,
    Tree,
    Alert,
    Slider,
    Icon,
    Row,
    Col,
    Upload,
    Progress,
    Spinner,
    Badge,
    Card,
    Rate,
    Steps,
    Step,
    Carousel,
    CarouselItem,
    Collapse,
    CollapseItem,
    Cascader,
    ColorPicker,
    Transfer,
    Container,
    Header,
    Aside,
    Main,
    Footer,
    Timeline,
    TimelineItem,
    Link,
    Divider,
    Image,
    Calendar,
    Backtop,
    PageHeader,
    CascaderPanel,
    Loading,
    MessageBox,
    Message,
    Notification
} from 'element-ui';
import router from "@/router";

Vue.use(Pagination);
Vue.use(Dialog);
Vue.use(Autocomplete);
Vue.use(Dropdown);
Vue.use(DropdownMenu);
Vue.use(DropdownItem);
Vue.use(Menu);
Vue.use(Submenu);
Vue.use(MenuItem);
Vue.use(MenuItemGroup);
Vue.use(Input);
Vue.use(InputNumber);
Vue.use(Radio);
Vue.use(RadioGroup);
Vue.use(RadioButton);
Vue.use(Checkbox);
Vue.use(CheckboxButton);
Vue.use(CheckboxGroup);
Vue.use(Switch);
Vue.use(Select);
Vue.use(Option);
Vue.use(OptionGroup);
Vue.use(Button);
Vue.use(ButtonGroup);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(DatePicker);
Vue.use(TimeSelect);
Vue.use(TimePicker);
Vue.use(Popover);
Vue.use(Tooltip);
Vue.use(Breadcrumb);
Vue.use(BreadcrumbItem);
Vue.use(Form);
Vue.use(FormItem);
Vue.use(Tabs);
Vue.use(TabPane);
Vue.use(Tag);
Vue.use(Tree);
Vue.use(Alert);
Vue.use(Slider);
Vue.use(Icon);
Vue.use(Row);
Vue.use(Col);
Vue.use(Upload);
Vue.use(Progress);
Vue.use(Spinner);
Vue.use(Badge);
Vue.use(Card);
Vue.use(Rate);
Vue.use(Steps);
Vue.use(Step);
Vue.use(Carousel);
Vue.use(CarouselItem);
Vue.use(Collapse);
Vue.use(CollapseItem);
Vue.use(Cascader);
Vue.use(ColorPicker);
Vue.use(Transfer);
Vue.use(Container);
Vue.use(Header);
Vue.use(Aside);
Vue.use(Main);
Vue.use(Footer);
Vue.use(Timeline);
Vue.use(TimelineItem);
Vue.use(Link);
Vue.use(Divider);
Vue.use(Image);
Vue.use(Calendar);
Vue.use(Backtop);
Vue.use(PageHeader);
Vue.use(CascaderPanel);

Vue.use(Loading.directive);

Vue.prototype.$cookie = cookie;
Vue.prototype.$loading = Loading.service;
Vue.prototype.$msgbox = MessageBox;
Vue.prototype.$alert = MessageBox.alert;
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$prompt = MessageBox.prompt;
Vue.prototype.$notify = Notification;
Vue.prototype.$message = Message;

Vue.use(ElementUI);
Vue.config.productionTip = false

// interceptors -> axios 请求拦截，给所有接口的headers添加token（登录除外）
axios.interceptors.request.use(config => {
    config.headers.Authorization = localStorage.getItem("token")
    return config;
})

const bus = new Vue();//新创建一个实例，用以传值
Vue.prototype.bus = bus//挂载在vue的原型上
const type = new Vue();//新创建一个实例，用以传值
Vue.prototype.type = type//挂载在vue的原型上

const titleVue = new Vue();//新创建一个实例，用以传值
Vue.prototype.titleVue = titleVue//挂载在vue的原型上
const contentVue = new Vue();//新创建一个实例，用以传值
Vue.prototype.contentVue = contentVue//挂载在vue的原型上

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
    data() {
        return {}
    }
});
