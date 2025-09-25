<template>
  <keep-alive>
  <div>
    <div class="crumbs">
    </div>
    <div class="container">
      <div class="handle-box">

        <a href="https://musetransfer.com/s/1lktfah6c" target="_black"><el-button type="danger" icon="el-icon-upload" >点击模版下载:密码6156</el-button></a>
        <el-button type="success" icon="el-icon-upload" @click="handleAdd" style="margin: 0px 0px 0px 10px">选择Excel</el-button>
        <el-button type="primary" icon="el-icon-search" v-show="filename !== ''" @click="handleProcess">处理excel</el-button>
        <el-button type="primary" icon="el-icon-search" v-show="exportFileName !== ''" @click="exportFile">导出</el-button>
        <a href=https://musetransfer.com/s/bhknln2ji target="_black"><el-button style="margin: 0px 0px 0px 10px" type="danger" icon="el-icon-upload" >所有模版下载</el-button></a>

      </div>

      <el-table :style="getTableContainStyle" empty-text="导入数据后显示" :data="showTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
       <el-table-column v-for="(header, index) in tableHeaders" :key="index" :prop="header.code" :label="header.name"  align="center"></el-table-column>
      </el-table>

      <div>
            <img style="width: 100%" src="@/assets/img/page1/tips.png">
      </div>

    </div>

    <!-- 编辑弹出框 -->
    <el-dialog title="点击方框或拖拽文件，可导入文件" v-model="diaLogShow"   width="30%" >
      <el-form style="height: 100px">

        <el-form-item label="文件" prop="file">
          <el-upload
              class="upload-import"
              ref="upload"
              action=""
              :file-list="fileList"
              v-model="fileList"
              :drag="true"
              :limit="1"
              :auto-upload="false">
          </el-upload>
        </el-form-item>

      </el-form>
      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="diaLogShow = false">取 消</el-button>
                    <el-button type="primary" @click="submit">确 定</el-button>
                </span>
      </template>
    </el-dialog>
  </div>
  </keep-alive>
</template>

<script>
import axios from 'axios'
import bg from "../../assets/img/page1/bg.png"

export default {
  name: "table",
  data() {
    return {
      diaLogShow: false,
      filename: '',
      exportFileName: '',
      showTableData: [],
      fileList: [],
      tableHeaders: [
          { code: "date", name: "姓名" },
          { code: "date", name: "学号" },
          { code: "date", name:"SPOC成绩" },
          { code: "date", name: "雨课堂成绩（课前测，课中、课后测）" },
          { code: "date",  name: "PTA作业" },
          { code: "date", name: "PTA测试" },
          { code: "date", name: "project成绩" },
          { code: "date", name: "平时总成绩" },
          { code: "date", name: "终结性成" },
          { code: "date", name: "总评成绩" }
      ],
    }
  },
  computed:{
    showTableheader(){
      const maxVisibleHeaders = 10; // 控制前9列
      if (this.tableHeaders.length <= maxVisibleHeaders){
        return this.tableHeaders;
      } else {
        return this.tableHeaders.slice(0,maxVisibleHeaders)
      }
    },
    getTableContainStyle(){ //控制函数
        if (this.showTableData.length>0){
          return "height:100%";
        }else {
          return "height:700px;overflow-y=auto";
        }
      }
  },
  methods: {
    handleProcess(){
      // 处理excel
      const baseUrl = process.env.VUE_APP_BASE_URL
      console.log(this.filename)
      const url = baseUrl + '/excel_proportion?filename=' + this.filename
      axios.get(url).then(response => {
        this.TableHeaders =  response.data.data.headers
        this.showTableData =  response.data.data.data
        this.filename =  ''
        this.exportFileName =  response.data.data.filename
      })

    },
    exportFile() {
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/excel_export?filename=' + this.exportFileName
      window.open(url)
    },
    submit() {
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/upload_and_get_data1'
      let formData = new FormData();
      const files = this.$refs.upload.uploadFiles
      if (files.length === 0) {
        alert('文件为空')
        return
      }
      let file = files[0].raw
      formData.append('file', file)
      formData.append('pictureCategory','articleCover')
      console.log(url);
      // 添加请求头
      axios.post(url,formData,{
        'Content-type' : 'multipart/form-data'
      })
          .then(response => {
            console.log(response.data)
            if (response.data.code === 200) {
              this.tableHeaders =  response.data.data.headers.slice(0)
              this.showTableData =  response.data.data.data.slice(1)
              this.filename =  response.data.data.filename
              this.exportFileName = ''
              this.$refs.upload.uploadFiles = []
              this.diaLogShow = false
            }
          })

    },

    handleAdd() {
      // 点击选择文件绑定的事件
      this.form = {}
      this.diaLogShow = true
      this.$refs.upload.uploadFiles = []
    },
  },
  mounted() {
  }
}
</script>

<style scoped>
.container { /*page1_bg.png图片文件放置在Vue项目的静态资源目录中，引入背景*/
  /*background-image: url("~@/assets/img/page1/bg.png");*/
  background-image: url("~@/assets/img/page1/bg.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}

.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}

.handle-input {
  width: 300px;
  display: inline-block;
}
.table {
  width: 100%;
  font-size: 14px;
}
.red {
  color: #ff0000;
}
.mr10 {
  margin-right: 10px;
}
.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}
</style>
