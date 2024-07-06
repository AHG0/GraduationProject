<template>
  <el-container style="width: 100%">
    <el-main style="margin: 5px 10px 0;">
<!--      <div style="text-align: center; margin: 0 0 20px">-->
<!--        <el-button @click="selectOrderById()">刷新</el-button>-->
<!--      </div>-->
      <el-dialog title="详细" :visible.sync="dialogTableVisible">
        <div style="text-align: center">
          <div>
            <div class="title">文件内容</div>
            <div style="text-align: left">{{ input }}</div>
          </div>
          <div style="display: flex; margin-top: 20px; margin-bottom: 20px">
            <transition name="el-fade-in-linear">
              <div style="margin: auto">
                <div class="title">信息抽取</div>
                <div style="text-align: left">
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
          </div>
          <div style="display: flex; margin-top: 20px; margin-bottom: 20px">
            <transition name="el-fade-in-linear">
              <div style="margin: auto">
                <div class="title">关系抽取</div>
                <div style="text-align: left">
                  <div class="tripe">
                    {{ relation }}
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </el-dialog>

      <div>
        <el-table
            :data="tableData.slice((currentPage-1)*PageSize,currentPage*PageSize)"
            style="width: 100%">
          <el-table-column show-overflow-tooltip:true prop="name" label="文件名" width="180px"></el-table-column>
          <el-table-column show-overflow-tooltip:true prop="input" label="文件内容" width="880px"></el-table-column>
          <el-table-column prop="sub_time" label="提交时间"></el-table-column>
          <el-table-column label="查看">
            <el-button slot="reference" @click="check">查看</el-button>
            <template>
              <el-button @click="check">查看</el-button>
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
import {GetRequestByUserId} from "@/unity/api";

export default {
  name: "test3",
  created() {
    this.currentPageData_()
    this.selectOrderById()
  },
  data() {
    return {
      tableData: [],
      dialogTableVisible: false,
      userid: this.$cookie.get("userid"),
      input: '',
      name: '',
      people: '',
      time: '',
      thing: '',
      num: '',
      place: '',
      jsonData: '',
      chart_data: [],
      chart_links: [],
      chart_data2: [],
      chart_links2: [],
      relation: [],

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
  methods: {
    check() {
      this.dialogTableVisible = true
    },
    selectOrderById() {
      GetRequestByUserId("http://localhost:8080/file_api/selectFERecordByUserId", this.userid).then((res) => {
        console.log(res.data)
        this.tableData = res.data
        this.totalCount = this.tableData.length
        this.dataList = res.data
        this.show = true
        this.show1 = true
        this.show2 = false
        console.log(this.show, this.show1, this.show2)
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
      })
    },

    // 根据当前页码和每页显示数量计算当前页的数据
    currentPageData_() {
      this.sliceData = []
      const startIndex_ = (this.currentPage - 1) * this.PageSize;
      const endIndex_ = startIndex_ + this.PageSize;
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
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0 0;
  padding: 0;
}
.title{
  color: #9b9b9b;
  font-size: 18px;
}
</style>