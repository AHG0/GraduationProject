<template>
  <el-container>
    <el-menu class="el-menu-vertical-demo">
      <div style="text-align: center">
        <el-button style="width: 90%" @click="show=false; input=''; disabled=false; v=true"> New Question</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column width="180" label="历史记录" prop="date" show-overflow-tooltip>
          <template v-slot="scope">
            <el-link @click="selectData(scope.row.input); show=true; v=false" :underline="false">
              {{ scope.row.input }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column>
          <template v-slot="scope">
            <el-button
                @click="deleteRow(scope.row.input)"
                type="text">
              移除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-menu>
    <el-main style="height: 584px; padding: 0 20px 0">
      <div v-show="v">
        <div style="text-align: center">
          <el-input type="textarea" style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); width: 1166px" id="input"
                    :rows="6" v-model="input" :disabled="disabled"
                    placeholder="please enter the question" clearable>
          </el-input>
        </div>
        <div style="text-align: center; line-height: 80px">
          <el-button type="primary" @click="submit(input);" style="height: 45px">提交</el-button>
        </div>
      </div>
      <div
          style="box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04); margin: 0 0 15px"
          v-if="show">
        <div class="transition-box-title" style="width: auto; margin-top: 17px;">
          文本内容
        </div>
        <div class="transition-box-content"
             style="line-height: 30px;padding: 0 20px 0;  width: auto; height: 90px; text-indent:2em;">
          {{ this.input }}
        </div>
      </div>
      <div style="text-align: center" v-if="show">
        <el-tabs style="width: auto" stretch>
          <el-tab-pane label="实体">
            <div v-show="show" style="display: flex; margin-top: 20px; margin-bottom: 20px">
              <transition name="el-fade-in-linear">
                <div class="transition-box">
                  <div class="transition-box-title">信息抽取</div>
                  <div class="transition-box-content">
                    <div class="tripe">
                      人物：{{ people }}
                    </div>
                    <div class="tripe">
                      时间：{{ time }}
                    </div>
                    <div class="tripe">
                      地点：{{ place }}
                    </div>
                    <div class="tripe">
                      物品：{{ thing }}
                    </div>
                    <div class="tripe">
                      数量：{{ num }}
                    </div>
                  </div>
                </div>
              </transition>
              <transition name="el-fade-in-linear">
                <div class="transition-box">
                  <div class="transition-box-title">信息可视化</div>
                  <div class="transition-box-content" style="overflow:hidden" id="chart"></div>
                </div>
              </transition>
            </div>
          </el-tab-pane>
          <el-tab-pane label="实体关系">
            <div v-show="show" style="display: flex; margin-top: 20px; margin-bottom: 20px">
              <transition name="el-fade-in-linear">
                <div class="transition-box">
                  <div class="transition-box-title">关系抽取</div>
                  <div class="transition-box-content">
                    <div class="tripe" v-for="(item, index) in relation" :key="index">
                      关系{{ index + 1 }}：【{{ item[0] }}】和【{{ item[1] }}】的关系是：{{ item[2] }}
                      <div>
                        句子：{{ item[3] }}
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
              <transition name="el-fade-in-linear">
                <div class="transition-box">
                  <div class="transition-box-title">信息可视化</div>
                  <div class="transition-box-content" style="overflow:hidden" id="chart2"></div>
                </div>
              </transition>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {GetRequest, PostRequest} from "@/unity/api";

export default {
  data() {
    return {
      tableData: [],
      input: '',
      people: '',
      time: '',
      thing: '',
      num: '',
      place: '',
      err: "系统错误",
      jsonData: '',
      data: [],
      links: [],
      chart_data2: [],
      chart_links2: [],
      relation: [],
      show: false,
      disabled: false,
      v: false,
      userid: this.$cookie.get("userid")
    }
  },
  mounted() {
    this.selectInput()
  },
  methods: {
    deleteRow(input) {
      GetRequest("http://localhost:8080/api/deleteEntity", input).then((res) => {
        if (res) {
          this.$message.success("删除成功")
          this.selectInput()
        }
      })
    },
    empty() {
      this.jsonData = '';
      this.input = '';
    },
    selectInput() {
      this.$axios.get('http://localhost:8080/api/selectEntity').then((res) => {
        console.log(res.data)
        this.tableData = res.data.reverse()
      })
    },
    selectData(input) {
      this.disabled = true;
      GetRequest('http://localhost:8080/api/selectEntityData', input).then((res) => {
        this.$message.success("查询成功")
        this.input = res.data.input;
        var dataJson = res.data
        this.jsonData = JSON.parse(res.data.rsl1);
        this.data = JSON.parse(dataJson.rsl2).result2_1
        this.links = JSON.parse(dataJson.rsl3).result3_1
        this.people = this.jsonData.people;
        this.time = this.jsonData.time;
        this.thing = this.jsonData.thing;
        this.num = this.jsonData.num;
        this.place = this.jsonData.place;
        this.relation = this.jsonData.relation
        this.chart_data2 = JSON.parse(dataJson.rsl2).result2_2
        this.chart_links2 = JSON.parse(dataJson.rsl3).result3_2
        this.drawChart()
        this.drawChart2()
      })
    },

    submit(input) {
      if (input === '') {
        this.$message.warning("请输入")
      } else {
        let arr = []
        for (let a of this.tableData) {
          arr.push(a.input)
        }
        if (arr.includes(input)) {
          this.$message.error("数据重复，无法提交")
        } else {
          this.$message.success("提交成功")
          this.disabled = true;
          PostRequest('/api/Entity', this.input, this.userid).then((res) => {
            this.show = true;
            if (JSON.stringify(res.data) !== '{}') {
              this.selectInput()
              this.v = false
              this.input = res.data.input;
              var dataJson = res.data
              this.jsonData = JSON.parse(dataJson.rsl1);
              this.data = JSON.parse(dataJson.rsl2).result2_1
              this.links = JSON.parse(dataJson.rsl3).result3_1
              this.people = this.jsonData.people;
              this.time = this.jsonData.time;
              this.thing = this.jsonData.thing;
              this.num = this.jsonData.num;
              this.place = this.jsonData.place;
              this.relation = this.jsonData.relation
              this.chart_data2 = JSON.parse(dataJson.rsl2).result2_2
              this.chart_links2 = JSON.parse(dataJson.rsl3).result3_2
              this.drawChart()
              this.drawChart2()
              this.selectData(this.tableData[0])
              this.$message.success("数据处理完成")
            } else {
              this.people = this.err;
              this.time = this.err;
              this.place = this.err;
              this.thing = this.err;
              this.num = this.err;
            }
          })
        }
      }
    },
    drawChart() {
      // 基于准备好的dom，初始化echarts实例
      let chart = this.$echarts.init(document.getElementById("chart"));
      // 指定图表的配置项和数据
      let option = {
        title: {
          text: ""
        },
        tooltip: {
          formatter: function (param) {
            return param.data.des;
          }
        },
        series: [
          {
            type: "graph",
            layout: "force",
            symbolSize: 50,
            focusNodeAdjacency: true, //是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。
            roam: true, //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            edgeSymbol: ["none", "arrow"], //边两端的标记类型，可以是一个数组分别指定两端，也可以是单个统一指定。默认不显示标记，常见的可以设置为箭头
            edgeSymbolSize: [10, 10],
            force: {
              repulsion: 2000, //节点之间的斥力因子
              edgeLength: [10, 10]
            },
            draggable: true,
            //定义节点的样式
            itemStyle: {
              color: "#eba844"
            },
            //连线的样式
            lineStyle: {
              width: 2,
              color: "#000"
            },
            //连线上的标记样式
            edgeLabel: {
              show: true,
              formatter: function (param) {
                //tooltip这里的formatter参数param可以得到series中的data数据
                return param.data.value;
              },
              color: "#000"
            },
            //节点上是否显示文字
            label: {
              show: true,
              fontWeight: "bold",
              fontSize: 18
            },
            data: this.data,
            links: this.links,
          },
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      chart.setOption(option);
    },
    drawChart2() {
      // 基于准备好的dom，初始化echarts实例
      let chart = this.$echarts.init(document.getElementById("chart2"));
      // 指定图表的配置项和数据
      let option = {
        title: {
          text: ""
        },
        tooltip: {
          formatter: function (param) {
            return param.data.des;
          }
        },
        series: [
          {
            type: "graph",
            layout: "force",
            symbolSize: 50,
            focusNodeAdjacency: true, //是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。
            roam: true, //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            edgeSymbol: ["none", "arrow"], //边两端的标记类型，可以是一个数组分别指定两端，也可以是单个统一指定。默认不显示标记，常见的可以设置为箭头
            edgeSymbolSize: [10, 10],
            force: {
              repulsion: 2000, //节点之间的斥力因子
              edgeLength: [10, 100]
            },
            draggable: true,
            //定义节点的样式
            itemStyle: {
              color: "#eba844"
            },
            //连线的样式
            lineStyle: {
              opacity: 0.9,
              curveness: 0.4,
              length: 50,
              width: 2,
              color: "#969696"
            },
            //连线上的标记样式
            edgeLabel: {
              show: true,
              formatter: function (param) {
                //tooltip这里的formatter参数param可以得到series中的data数据
                return param.data.value;
              },
              color: "#000"
            },
            //节点上是否显示文字
            label: {
              show: true,
              fontWeight: "bold",
              fontSize: 18
            },
            data: this.chart_data2,
            links: this.chart_links2,
          },
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      chart.setOption(option);
    },
  },
}

</script>

<style scoped>
.btn-upload {
  margin: 0;
}

.transition-box {
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  margin: auto;
  width: auto;
  height: 330px;
}

.transition-box-title {
  background-color: #ffffff; /*背景颜色*/
  width: 600px;
  height: 30px;
  line-height: normal;
  vertical-align: middle;
  text-align: center;
  color: #838383; /*字体颜色*/
  border-radius: 7px;
  padding-top: 0;
  margin: auto;
}

.transition-box-content {
  text-indent: 0;
  background-color: #fff;
  border-radius: 7px;
  width: 600px;
  height: 300px;
  word-break: break-word;
  line-height: 55px;
  justify-content: center;
  margin: auto;
  overflow: auto;
  text-align: left;
}

body {
  margin: 0;
  padding: 0;
}

.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}

.show_table {
  position: relative;
  width: 100%;
  overflow: auto;
  height: 585px;
}

.tripe {
  padding-left: 20px;
}
</style>