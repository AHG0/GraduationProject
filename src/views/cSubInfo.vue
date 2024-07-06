<template>
  <el-container style="width: 100%">
    <el-main style="margin: 5px 10px 0;">
      <div style="text-align: center; margin: 0 0 20px">
        <el-button @click="selectHistory()">刷新</el-button>
      </div>
      <el-dialog title="" :visible.sync="dialogTableVisible">
        <div style="display: flex;margin: 0 0 0">
          <transition name="el-fade-in-linear">
            <div style="margin: auto;text-align: center">
              <div>文件列表</div>
              <div class="transition-box">
                <div style="width: 100%;" v-for="item in fNameList" :key="item">
                  <el-link @click="getFileContent(item)" :underline="false">
                    {{ item }}
                  </el-link>
                </div>
              </div>
            </div>
          </transition>

          <transition name="el-fade-in-linear">
            <div style="margin: auto;text-align: center;">
              <div>文件分类情况</div>
              <div id="chart" style="width:300px;height:200px"></div>
            </div>
          </transition>
        </div>
        <div style="text-align: center;">
          <div>
            <el-table
                :data="tableData.slice((currentPage_-1)*PageSize_,currentPage_*PageSize_)"
                style="width: 100%">
              <el-table-column prop="input" label="文件内容"></el-table-column>
              <el-table-column prop="clas" label="分类"></el-table-column>
            </el-table>
          </div>
          <div class="page">
            <!-- 分页控件 -->
            <el-pagination
                :background="true"
                @size-change="handleSizeChange_"
                @current-change="handleCurrentChange_"
                :current-page.sync="currentPage_"
                :page-sizes="pageSizes_"
                :page-size="PageSize_"
                :total="totalCount_"
                layout="total, sizes, prev, pager, next, jumper">
            </el-pagination>
          </div>
        </div>
      </el-dialog>

      <div>
        <el-table
            :data="nameJson.slice((currentPage-1)*PageSize,currentPage*PageSize)" style="width: 100%">
          <el-table-column prop="sub_time" label="提交时间"></el-table-column>
          <el-table-column label="查看">
            <template v-slot="scope">
              <el-button slot="reference" @click="dialogTableVisible = true; getBySubTime(scope.row.sub_time)">查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="page">
        <!-- 分页控件 -->
        <el-pagination
            :background="true"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="pageSizes"
            :page-size="PageSize"
            :total="totalCount"
            layout="total, sizes, prev, pager, next, jumper">
        </el-pagination>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {GetNameRequest} from "@/unity/api";

export default {
  name: "file_home1",
  data() {
    return {
      userid: this.$cookie.get("userid"),
      tableData: [],
      input: '',
      name: '',

      nameJson: [],

      err: "系统错误",
      jsonData: '',
      data: [],
      links: [],
      show: false,

      backData: [],
      x_data: [],
      x_data_num: [],
      fNameList: [],
      sub_time: '',
      dialogTableVisible: false,

      file: "",

      // 默认显示第几页
      currentPage: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount: 0,
      // 个数选择器（可修改）
      pageSizes: [1, 5, 10],
      // 默认每页显示的条数（可修改）
      PageSize: 5,

      // 默认显示第几页
      currentPage_: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount_: 0,
      // 个数选择器（可修改）
      pageSizes_: [1, 5, 10],
      // 默认每页显示的条数（可修改）
      PageSize_: 5,
    }
  },
  created() {
    this.selectHistory()
  },
  mounted() {
    this.drawChart()
  },
  methods: {

    //通过用户id搜索历史记录
    selectHistory() {
      this.$axios.get('http://localhost:8080/file_c_api/getClassResult', {
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((res) => {
        console.log(res.data)
        this.nameJson = []
        const list = res.data.reverse()
        const nameList = []
        for (const element of list) {
          if (nameList.includes(element.sub_time)) {
            continue
          } else {
            nameList.push(element.sub_time)
            this.nameJson.push(element)
          }
        }
        this.historyFileName = nameList
        this.totalCount = this.historyFileName.length
      })
    },

    //点击查询时间获取提交的文件分类结果
    getBySubTime(sub_time) {
      this.sub_time = sub_time
      this.x_data = []
      this.x_data_num = []
      GetNameRequest('http://localhost:8080/file_c_api/selectFCResultRecord', sub_time).then((res) => {
        for (const i of res.data[0].rsl2) {
          if (this.fNameList.includes(i.name)) {
            continue
          } else {
            this.fNameList.push(i.name)
          }
        }
        console.log(this.fNameList)
        this.show = true
        this.$message.success("查询成功")
        this.name = res.data[0].name
        this.backData = JSON.parse(res.data[0].rsl1[0].rsl)
        for (const element of this.backData) {
          this.x_data.push(element.name)
          this.x_data_num.push(element.value)
        }
        this.drawChart();
      })
    },

    getFileContent(name) {
      this.$axios.get("http://localhost:8080/file_c_api/getFileContentRecord", {
        params: {
          sub_time: this.sub_time,
          file_name: name
        },
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((res) => {
        console.log(res.data)
        this.input = res.data
        this.tableData = res.data
        this.totalCount_ = this.tableData.length
      })
    },

    drawChart() {
      // 基于准备好的dom，初始化echarts实例
      let chart = this.$echarts.init(document.getElementById("chart"));
      // 指定图表的配置项和数据
      chart.setOption({
        title: {
          text: '', // 主标题
          subtext: '', // 副标题
          x: 'left' // x轴方向对齐方式
        },

        xAxis: {
          data: this.x_data,
          triggerEvent: true,
          axisLabel: {
            interval: 0,
            formatter: function (value) {
              //x轴的文字改为竖版显示
              var str = value.split("");
              return str.join("\n");
            }
          },

        },
        yAxis: {},
        series: [
          {
            type: 'bar',
            data: this.x_data_num,
            barWidth: '20%'
          }]
      })
    },

    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.PageSize = val
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.currentPage = 1
    },
    // 显示第几页
    handleCurrentChange(val) {
      // 改变默认的页数
      this.currentPage = val
    },
    // 分页
    // 每页显示的条数
    handleSizeChange_(val) {
      // 改变每页显示的条数
      this.PageSize_ = val
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.currentPage_ = 1
    },
    // 显示第几页
    handleCurrentChange_(val) {
      // 改变默认的页数
      this.currentPage_ = val
    },
  }
}
</script>

<style scoped>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0 0;
  padding: 0;
}

</style>