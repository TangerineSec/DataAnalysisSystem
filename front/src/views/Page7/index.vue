<template>
  <div>

    <div class="crumbs">
    </div>
    <div class="container">
      <div class="handle-box">
        <a href="https://musetransfer.com/s/1lktfah6c" target="_black"><el-button type="danger" icon="el-icon-upload" >点击模版下载:密码6156</el-button></a>
        <el-button type="success" icon="el-icon-upload" @click="handleAdd" style="margin: 0px 0px 0px 10px">选择Excel</el-button>
        <el-button type="primary" icon="el-icon-search" v-show="filename !== ''" @click="handleProcess">处理excel</el-button>
        <el-button type="primary" icon="el-icon-search" v-show="exportFileName !== ''" @click="exportFile">导出</el-button>
        <div>使用说明：在需要计算平均值的头部加上最低分数（数字格式），学号和姓名的分数字段保留即可。</div>
      </div>

      <el-table empty-text="导入数据后显示" :data="showTableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
        <el-table-column v-for="(d, index) in showTableHeader" :prop="d.code" :label="d.name"  align="center"></el-table-column>
      </el-table>


      <div>
        <img style="width: 100%" src="@/assets/img/page7/tips.png">
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
</template>

<script>
import axios from 'axios'

export default {
  name: "table",
  data() {
    return {
      diaLogShow: false,
      filename: '',
      exportFileName: '',
      showTableData: [],
      fileList: [],
      showTableHeader: [
          { code: "date", name: "赋分最低分" },
          { code: "date", name: "80" },
          { code: "date", name:"70" },
          { code: "date", name: "65" },
          { code: "date",  name: "60" },
          { code: "date", name: "55" },
      ],
    }
  },
  computed:{
    showTableheader(){
      const maxVisibleHeaders = 6; // 控制前10列
      if (this.showTableHeader.length <= maxVisibleHeaders){
        return this.showTableHeader;
      } else {
        return this.showTableHeader.slice(0,maxVisibleHeaders)
      }
    }
  },
  methods: {
    handleProcess(){
      // 处理excel,本来是加权，现在改为赋权，所以这里要改
      const baseUrl = process.env.VUE_APP_BASE_URL
      console.log(this.filename)
      const url = baseUrl + '/excel_assign?filename=' + this.filename
      axios.get(url).then(response => {
        this.showTableHeader =  response.data.data.headers.slice(1)
        this.showTableData =  response.data.data.data.slice(1)
        this.filename =  ''
        this.exportFileName =  response.data.data.filename
      })

    },
    exportFile() {
      // 本来是导出文件，现在也是导出文件，所以不改
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/excel_export?filename=' + this.exportFileName
      window.open(url)
    },
    submit() {
      // 本来是上传1个文件，现在也是上传一个文件，所以不改
      const baseUrl = process.env.VUE_APP_BASE_URL
      const url = baseUrl + '/upload_and_get_data_sheet'
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
              this.showTableHeader =  response.data.data.headers
              this.showTableData =  response.data.data.data.slice(1)
              this.filename =  response.data.data.filename
              this.exportFileName = ''
              this.$refs.upload.uploadFiles = []
              this.diaLogShow = false
            }
          })

    },

    handleAdd() {
      // 点击选择文件绑定的事件，导入之前操作基本不改
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
  background-image: url("~@/assets/img/page7/bg.png");
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
  height: 720px;
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
