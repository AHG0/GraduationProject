<template>
  <el-container>
    <el-container>
      <el-menu class="el-menu-vertical-demo">
        <el-table :data="nameJson" style="width: 100%">
          <el-table-column width="180" label="历史记录" prop="date" show-overflow-tooltip>
            <template v-slot="scope">
              <el-link @click="getBySubTime(scope.row.sub_time); show = true;" :underline="false">
                {{ scope.row.sub_time }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column>
            <template v-slot="scope">
              <el-button
                  @click="deleteRow(scope.row.name)"
                  type="text">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-menu>
      <el-main style="height: 584px">
        <div style="text-align: center; line-height: 60px">
          <el-button class="btn-upload" type="primary" @click="handleUpdate">上传文件</el-button>
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

        <div v-show="show" style="display: flex;margin: 20px 0 0">
          <transition name="el-fade-in-linear">
            <div v-show="show" style="margin: auto;">
              <div class="transition-span">文件列表</div>
              <div class="transition-box">
                <div style="width: 100%; margin: 0 10px 0" v-for="item in fNameList" :key="item">
                  <el-link @click="getFileContent(item); show = true;" :underline="false">
                    {{ item }}
                  </el-link>
                </div>
              </div>
            </div>
          </transition>

          <transition name="el-fade-in-linear">
            <div v-show="show" style="margin: auto;">
              <div class="transition-span">文件分类情况</div>
              <div class="transition-box" id="chart"></div>
            </div>
          </transition>
        </div>

        <div v-show="show" style="text-align: center; margin: 20px 30px 0;">
          <div>
            <el-table
                :data="tableData.slice((currentPage-1)*PageSize,currentPage*PageSize)"
                style="width: 100%">
              <el-table-column prop="input" label="文件内容"></el-table-column>
              <el-table-column prop="clas" label="分类"></el-table-column>
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
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import {GetNameRequest, PostFile} from "@/unity/api";

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

      dialogOfUpload: false,
      fileList: [],
      fileNameList: [],

      file: "",

      // 默认显示第几页
      currentPage: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount: 0,
      // 个数选择器（可修改）
      pageSizes: [1, 5, 10],
      // 默认每页显示的条数（可修改）
      PageSize: 5,
    }
  },
  created() {
    this.selectHistory()
    this.currentPageData_()
  },
  mounted() {
    this.drawChart()
  },
  methods: {
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
        console.log(this.fileList);
      }
    },

    //文件上传
    submitUpload() {
      this.dialogOfUpload = false
      this.$message.info("正在上传......")
      var data = new FormData();
      this.fileList.forEach(val => {
        data.append('files', val.raw);
      });
      PostFile('http://localhost:8090/uploadClassFile', data).then((res) => {
        switch (res.data) {
          case 0:
            this.$message.success("上传成功")
            console.log(res.data)
            this.backData = res.data
            this.selectHistory()
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
        }
      }).catch(() => {
        this.$message.error("上传失败")
      });
    },

    deleteRow(name) {
      GetNameRequest("http://localhost:8080/file_c_api/deleteFCName", name).then((res) => {
        if (res) {
          this.$message.success("删除成功")
          this.selectHistory()
        }
      })
    },

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
        this.getBySubTime(this.historyFileName[0])
      })
    },

    //点击查询时间获取提交的文件分类结果
    getBySubTime(sub_time) {
      this.sub_time = sub_time
      this.x_data = []
      this.x_data_num = []
      GetNameRequest('http://localhost:8080/file_c_api/selectFCResult', sub_time).then((res) => {
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
      this.$axios.get("http://localhost:8080/file_c_api/getFileContent", {
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
        this.totalCount = this.tableData.length
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
          data: this.x_data
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
    // 根据当前页码和每页显示数量计算当前页的数据
    currentPageData_() {
      this.sliceData = []
      const startIndex_ = (this.currentPage_ - 1) * this.pageSize_;
      const endIndex_ = startIndex_ + this.pageSize_;
      this.sliceData = this.tableData.slice(startIndex_, endIndex_);
      return this.sliceData;
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
  }
}
</script>


<style scoped>
.el-header {
  background-color: #0e4479;
  color: #303133;
  line-height: 60px;
  align-content: center;
}

.transition-span {
  background-color: #0e4479;
  width: 550px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  color: #f4f4f5;
  border-radius: 7px;
  position: relative;
}

.transition-box {
  text-indent: 0;
  background-color: #fff;
  border-radius: 7px;
  width: 550px;
  height: 255px;
  word-break: break-word;
  line-height: 50px;
  justify-content: center;
}

body {
  margin: 0;
  padding: 0;
}

.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0 0;
  padding: 0;
}


</style>