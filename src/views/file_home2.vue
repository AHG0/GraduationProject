<template>
  <el-container>
    <el-menu>
      <el-table class="show_table" :data="nameJson" highlight-current-row>
        <el-table-column width="180" label="历史记录" prop="date" show-overflow-tooltip>
          <template v-slot="scope">
            <el-link @click="selectFEntityData(scope.row.name); show = true;" :underline="false">
              {{ scope.row.name }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column>
          <template v-slot="scope">
            <el-button type="danger"
                       @click="deleteRow(scope.row.name)"
                       size="mini"
                       icon="el-icon-delete" circle></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-menu>
    <el-main style="padding-bottom: 0">
      <div style="text-align: center; line-height: normal">
        <el-button class="btn-upload" type="primary" @click="handleUpdate">上传文件</el-button>
<!--        <el-button type="primary" @click="testSend">主要按钮</el-button>-->
<!--        {{ queries_num }}-->
<!--        <el-button type="primary" @click="onWebSocketClose">断开连接</el-button>-->
      </div>
      <el-dialog title="上传" :visible.sync="dialogOfUpload" width="50%" style="text-align: center;">
        <el-upload class="upload-demo" action="" drag multiple :auto-upload="false"
                   :file-list="fileList" :on-change="handleChange" :http-request="submitUpload">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">上传txt格式文件</div>
        </el-upload>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogOfUpload = false">取 消</el-button>
          <el-button type="primary" @click="submitUpload()">上 传</el-button>
        </div>
      </el-dialog>
      <div
          style="box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04); margin: 15px 0 15px"
          v-if="show">
        <div class="transition-box-title" style="width: auto; margin-top: 17px;">
          文件内容
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
          <div class="page" style="text-align: center">
            <!-- 分页控件 -->
            <el-pagination
                @current-change="currentPageData"
                :background="true"
                :current-page.sync="currentPage"
                :page-size="pageSize"
                layout="total, prev, pager, next"
                :total="totalPages"
                v-show="showPage"
                :prev-click="prevPage"
                :next-click="nextPage">
            </el-pagination>
          </div>
        </el-tabs>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {GetNameRequest, GetRequestByUserId, PostFile} from "@/unity/api";

export default {
  name: "file_home2",
  data() {
    return {
      nameJson: [],
      nameList: [],
      historyFileName: [],
      input: '',
      name: '',
      people: '',
      time: '',
      thing: '',
      num: '',
      place: '',
      err: "系统错误",
      jsonData: '',
      chart_data: [],
      chart_links: [],
      chart_data2: [],
      chart_links2: [],
      relation: [],
      show: false,

      dialogOfUpload: false,
      fileList: [], //上传文件的所有信息
      fileNameList: [],//上传文件的文件名

      file: "",

      dataList: [], // 后端返回的数组
      pageSize: 1, // 每页显示的数量
      currentPage: 1, // 当前页码
      showPage: false,

      username: this.$cookie.get("username"),
      userid: this.$cookie.get("userid"),

      QueriesNum: -1,

      queries_num: localStorage.getItem("queries_num"),

      websocket: null, // WebSocket对象
      reconnectInterval: 3000, // 重连间隔时间（毫秒）
      restartWebsocket: null, // 重启定时器
      heartbeatInterval: null, // 心跳定时器
    }
  },
  mounted() {
    this.drawChart()
    this.drawChart2()
  },
  created() {
    this.submitUserid()
    this.bus.$on('submitUpload', name => {
      this.queries_num = name
    })
  },
  computed: {
    // 根据数组长度和每页显示数量计算总页数
    totalPages() {
      return Math.ceil(this.dataList.length / this.pageSize);
    },
  },
  methods: {
    testSend() { // 测试
      const send = {
        "toUID": this.userid,
        "queries_num": this.queries_num,
        "file_num": 1,
        "heartbeat": false,
      }
      this.sendMessage(JSON.stringify(send));
    },
    pay() {
      this.$router.push('/pay')
    },
    setQueriesNum() {
      GetRequestByUserId("http://localhost:8080/user_api/select_by_userid", this.userid).then((res) => {
        this.QueriesNum = res.data.queries_num
      })
    },

    // 根据当前页码和每页显示数量计算当前页的数据
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      const dataJson = this.dataList.slice(startIndex, endIndex)[0]
      this.input = dataJson.input
      const jsonData = JSON.parse(dataJson.rsl1)
      this.chart_data = JSON.parse(dataJson.rsl2).result2_1
      this.chart_links = JSON.parse(dataJson.rsl3).result3_1
      this.chart_data2 = JSON.parse(dataJson.rsl2).result2_2
      this.chart_links2 = JSON.parse(dataJson.rsl3).result3_2
      this.people = jsonData.people
      this.time = jsonData.time
      this.thing = jsonData.thing
      this.num = jsonData.num
      this.place = jsonData.place
      this.relation = jsonData.relation
      this.drawChart()
      this.drawChart2()
      return this.dataList.slice(startIndex, endIndex);
    }
    ,
    handleUpdate() {
      this.fileList = []
      this.fileNameList = []
      this.dialogOfUpload = true;
    },

    //文件数量改变
    handleChange(file) {
      this.file = file.raw;
      if (this.fileNameList.includes(file.raw.name)) {
        this.$message.warning("请勿添加重复文件")
      } else {
        this.fileList.push(file);
        this.fileNameList.push(file.raw.name);
      }
    },

    //上传token解析用户id
    submitUserid() {
      this.$axios.get("http://localhost:8080/file_api/submitUserId", {
        headers: {token: localStorage.getItem("token")}
      }).then((res) => {
        console.log(res)
        // this.setQueriesNum()
        this.selectByUserId(this.userid)
      })
    },

    //文件上传
    submitUpload() {
      if (this.fileList.length === 0) {
        this.$message.error("请上传文件")
        return
      }
      //判断提交的文件列表中是否有历史记录中存在的文件
      var count = 0
      var repeatFile = []
      for (const element of this.fileNameList) {
        if (this.historyFileName.includes(element)) {
          repeatFile.push(element)
          count = count + 1
        }
      }
      if (count !== 0) {
        this.$message.error("提交文件中有" + count + "个重复文件：" + repeatFile)
      }
      if (this.queries_num <= 0) {
        this.$message.error("查询次数不足")
      } else if (this.queries_num - this.fileNameList.length < 0) {
        this.$message.error("提交文件数量超过查询次数，还可提交" + this.queries_num + "个文件")
      } else {
        this.dialogOfUpload = false
        this.$message.info("开始上传" + this.fileNameList.length + "个文件......")
        var data = new FormData();
        data.append('usertype', localStorage.getItem("usertype"))
        this.fileList.forEach(val => {
          data.append('files', val.raw);
        });
        PostFile('http://localhost:8089/uploadFile', data).then((res) => {
          switch (res.data) {
            case 0:
              this.$message.success("上传成功")
              this.show = true
              this.selectByUserId(this.userid)
              var send = {
                "toUID": this.userid,
                "queries_num": this.queries_num,
                "file_num": this.fileNameList.length,
                "heartbeat": false,
              }
              this.sendMessage(JSON.stringify(send));
              break
            case 1:
              this.$message.warning("执行失败")
              break
            case 2:
              this.$message.error("token解析失败")
              break
            case 3:
              this.$message.error("提交文件数量过多")
              break
            case 4:
              this.$message.error("单个文件文字数量过多")
              break
            case 5:
              this.$message.error("服务器出错")
              break
          }
        })
      }
    },

    //文件删除
    deleteRow(name) {
      GetNameRequest("http://localhost:8080/file_api/deleteFEName", name).then((res) => {
        if (res) {
          this.$message.success("删除成功")
          this.selectByUserId(this.userid)
        }
      })
    },

    //通过用户id搜索历史记录
    selectByUserId(userid) {
      GetRequestByUserId('http://localhost:8080/file_api/selectFEntityByUserId', userid).then((res) => {
        this.nameJson = []
        const list = res.data.reverse()
        const nameList = []
        for (const element of list) {
          if (nameList.includes(element.name)) {
            continue
          } else {
            nameList.push(element.name)
            this.nameJson.push(element)
          }
        }
        this.historyFileName = nameList
        this.selectFEntityData(this.nameJson[0].name)
      })
    },
    selectName() {
      this.$axios.get('http://localhost:8080/file_api/selectFEName').then((res) => {
        this.nameJson = []
        const list = res.data.reverse()
        const nameList = []
        for (const element of list) {
          if (nameList.includes(element.name)) {
            continue
          } else {
            nameList.push(element.name)
            this.nameJson.push(element)
          }
        }
      })
    },
    selectFEntityData(name) {
      GetNameRequest('http://localhost:8080/file_api/selectFEntityData', name).then((res) => {
        this.$message.success("查询" + name + "成功")
        this.dataList = res.data
        this.show = true
        this.show1 = true
        this.show2 = false
        this.showPage = this.dataList.length !== 1
        this.dataJson = res.data.slice(0, 1)[0]
        this.input = this.dataJson.input
        this.name = this.dataJson.name
        this.jsonData = JSON.parse(this.dataJson.rsl1)
        this.relation = this.jsonData.relation
        this.chart_data = JSON.parse(this.dataJson.rsl2).result2_1
        this.chart_links = JSON.parse(this.dataJson.rsl3).result3_1
        this.chart_data2 = JSON.parse(this.dataJson.rsl2).result2_2
        this.chart_links2 = JSON.parse(this.dataJson.rsl3).result3_2
        this.people = this.jsonData.people
        this.time = this.jsonData.time
        this.thing = this.jsonData.thing
        this.num = this.jsonData.num
        this.place = this.jsonData.place
        this.drawChart()
        this.drawChart2()
      })
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
            data: this.chart_data,
            links: this.chart_links,
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

    // 上一页
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < Math.floor(this.totalPages)) {
        this.currentPage++;
      }
    },
  }
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
  height: 235px;
  word-break: break-word;
  line-height: 45px;
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