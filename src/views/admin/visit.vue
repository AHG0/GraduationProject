<template>
  <div>
    <div style="display: flex; margin: 20px 0 0">
      <div style="width:500px;height:300px;margin: auto" ref="visit_count_sum"></div>
      <div style="width:500px;height:300px; margin: auto" ref="day_add_user"></div>
      <div style="width:500px;height:300px; margin: auto" ref="submit_count_sum"></div>
      <div style="width:500px;height:300px; margin: auto" ref="c_submit_count_sum"></div>
    </div>
    <div style="display: flex; margin: 20px 0 0">
      <div style="width:500px;height:300px;margin: auto" ref="day_pay_count"></div>
      <div style="width:500px;height:300px;margin: auto" ref="day_pay_sum"></div>
    </div>
  </div>
</template>

<script>
//局部引用
const echarts = require('echarts');
export default {
  data() {
    return {
      x_data_1: [],
      x_data_num_1: [],
      x_data_num_e: [],
      x_data_num_c: [],
      x_data_2: [],
      x_data_num_2: [],
      x_data_3: [],
      x_data_num_3: [],
      x_data_4: [],
      x_data_num_4: [],
    }
  },
  created() {
    this.getVisitCount()
    this.getDayAddUser()
    this.getDayPayCount()
    this.getDayPaySum()
  },
  methods: {
    getVisitCount() {
      this.$axios.get("http://localhost:8080/login_api/selectVisitCount", {
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((resp) => {
        var data = resp.data
        for (const element of data) {
          this.x_data_1.push(element.visit_day)
          this.x_data_num_1.push(element.visit_count_sum)
          this.x_data_num_e.push(element.submit_count_sum)
          this.x_data_num_c.push(element.c_submit_count_sum)
        }
        this.initChart1()
        this.initChartE()
        this.initChartC()
      })
    },
    getDayAddUser() {
      this.$axios.get("http://localhost:8080/login_api/selectDayAddUser", {
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((resp) => {
        var data = resp.data
        console.log(data)
        for (const element of data) {
          this.x_data_2.push(element.registration_day)
          this.x_data_num_2.push(element.day_add_user)
        }
        this.initChart2()
      })
    },
    getDayPayCount() {
      this.$axios.get("http://localhost:8080/pay_api/getDayPayCount", {
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((resp) => {
        var data = resp.data
        console.log(data)
        for (const element of data) {
          this.x_data_3.push(element.pay_day)
          this.x_data_num_3.push(element.pay_day_count)
        }
        this.initChart3()
      })
    },
    getDayPaySum() {
      this.$axios.get("http://localhost:8080/pay_api/getDayPaySum", {
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((resp) => {
        var data = resp.data
        console.log(data)
        for (const element of data) {
          this.x_data_4.push(element.pay_day)
          this.x_data_num_4.push(element.pay_day_sum)
        }
        this.initChart4()
      })
    },

    initChart1() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(this.$refs.visit_count_sum);
      // 绘制图表
      myChart.setOption({
        title: {
          text: '网站每日访问量',
          left: 'center',
        },
        tooltip: {},
        xAxis: {
          data: this.x_data_1
        },
        yAxis: {},
        series: [{
          name: '日访问量',
          type: 'line',
          data: this.x_data_num_1,
          smooth: true,
          label: {
            show: true,
            position: 'top',
            textStyle: {
              fontSize: 12
            }
          }
        }]
      });
    },
    initChart2() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(this.$refs.day_add_user);
      // 绘制图表
      myChart.setOption({
        title: {
          text: '网站每日用户增长量',
          left: 'center'
        },
        tooltip: {},
        xAxis: {
          data: this.x_data_2
        },
        yAxis: {},
        series: [{
          name: '日增用户',
          type: 'line',
          data: this.x_data_num_2,
          smooth: true,
          label: {
            show: true,
            position: 'top',
            textStyle: {
              fontSize: 12
            }
          }
        }]
      });
    },
    initChartE() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(this.$refs.submit_count_sum);
      // 绘制图表
      myChart.setOption({
        title: {
          text: '抽取接口日提交量',
          left: 'center'
        },
        tooltip: {},
        xAxis: {
          data: this.x_data_1
        },
        yAxis: {},
        series: [{
          name: '日提交量',
          type: 'line',
          data: this.x_data_num_e,
          smooth: true,
          label: {
            show: true,
            position: 'top',
            textStyle: {
              fontSize: 12
            }
          }
        }]
      });
    },
    initChartC() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(this.$refs.c_submit_count_sum);
      // 绘制图表
      myChart.setOption({
        title: {
          text: '分类接口日提交量',
          left: 'center'
        },
        tooltip: {},
        xAxis: {
          data: this.x_data_1
        },
        yAxis: {},
        series: [{
          name: '日提交量',
          type: 'line',
          data: this.x_data_num_c,
          smooth: true,
          label: {
            show: true,
            position: 'top',
            textStyle: {
              fontSize: 12
            }
          }
        }]
      });
    },
    initChart3() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(this.$refs.day_pay_count);
      // 绘制图表
      myChart.setOption({
        title: {
          text: '网站每日支付订单量',
          left: 'center'
        },
        tooltip: {},
        xAxis: {
          data: this.x_data_3
        },
        yAxis: {},
        series: [{
          name: '日支付订单',
          type: 'line',
          data: this.x_data_num_3,
          smooth: true,
          label: {
            show: true,
            position: 'top',
            textStyle: {
              fontSize: 12
            }
          }
        }]
      });
    },
    initChart4() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(this.$refs.day_pay_sum);
      // 绘制图表
      myChart.setOption({
        title: {
          text: '网站每日支付总额',
          left: 'center'
        },
        tooltip: {},
        xAxis: {
          data: this.x_data_4
        },
        yAxis: {},
        series: [{
          name: '日支付总额',
          type: 'line',
          data: this.x_data_num_4,
          smooth: true,
          label: {
            show: true,
            position: 'top',
            textStyle: {
              fontSize: 12
            }
          }
        }]
      });
    },
  },
  //一加载页面就调用
  mounted() {
    this.initChart1();
    this.initChart2();
    this.initChart3();
    this.initChart4();
  }
}
</script>
<style>
</style>