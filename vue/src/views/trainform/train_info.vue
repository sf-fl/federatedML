<template>
  <div>
    <el-row :gutter="15">
      <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px" label-position="left">
        <el-col :span="10">
          <el-form-item label="任务ID" prop="taskID">
            <el-input v-model="formData.taskID" placeholder="任务ID" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="任务名称" prop="taskname">
            <el-input v-model="formData.taskname" placeholder="任务名称" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="项目名称" prop="projectname">
            <el-input v-model="formData.projectname" placeholder="项目名称" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="模型名称" prop="modelname">
            <el-input v-model="formData.modelname" placeholder="模型名称" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="机器学习算法" prop="MLA">
            <el-input v-model="formData.MLA" placeholder="机器学习算法" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="对齐字段" prop="alianfeature">
            <el-input v-model="formData.alianfeature" placeholder="对齐字段" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="创建时间" prop="createtime">
            <el-input v-model="formData.createtime" placeholder="创建时间" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="最后操作时间" prop="lastmodify">
            <el-input v-model="formData.lastmodify" placeholder="最后操作时间" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="我方IP:端口" prop="userIPPort">
            <el-input v-model="formData.userIPPort" placeholder="我方IP:端口" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="对方IP:端口" prop="partnerIPPort">
            <el-input v-model="formData.partnerIPPort" placeholder="对方IP:端口" readonly
                      :style="{width: '100%'}"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="数据集描述" prop="datainfo">
            <el-input v-model="formData.datainfo" placeholder="数据集描述" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="训练集比例" prop="trainratio">
            <el-input v-model="formData.trainratio" placeholder="训练集比例" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="KS" prop="fileloc">
            <el-input v-model="formData.ks" placeholder="KS" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="AUC" prop="fileloc">
            <el-input v-model="formData.auc" placeholder="AUC" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="文件结果地址" prop="fileloc">
            <el-input v-model="formData.fileloc" placeholder="文件结果地址" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="数据库地址" prop="dbloc">
            <el-input v-model="formData.dbloc" placeholder="数据库地址" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="19">
          <el-form-item label="下拉选择" prop="feature">
            <el-select v-model="formData.feature" placeholder="请选择下拉选择" filterable clearable
                       :style="{width: '100%'}">
              <el-option v-for="(item, index) in featureOptions" :key="index" :label="item.label"
                         :value="item.value" :disabled="item.disabled"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item size="large">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <el-button type="primary" @click="toPredict">发起预测</el-button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <el-button @click="backToTable">返回列表</el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
  </div>
</template>
<script>

import axios from 'axios'

export default {
  components: {},
  props: [],
  data () {
    return {
      formData: {
        taskID: '',
        taskname: "",
        projectname: "",
        modelname: "",
        MLA: "",
        alianfeature: "",
        createtime: "",
        lastmodify: "",
        userIPPort: "",
        partnerIP: "",
        partnerIPPort: "",
        partnerPort: "",
        datainfo: "",
        trainratio: "",
        fileloc: "",
        ks: "",
        auc: "",
        dbloc: "",
        feature: ""
      },
      rules: {},
      featureOptions: [{
        "label": "选项一",
        "value": 1
      }, {
        "label": "选项二",
        "value": 2
      }, {
        "label": '',
        "value": ''
      }]
    }
  },
  computed: {},
  mounted () {},
  methods: {
    reload () {
      this.id = this.$route.params.id
      console.log(this.id)
      if (this.id === undefined) {
        this.formData.taskID = '暂时无法支持直接输入ID'
        this.formData.taskname = '请从任务列表选择进入'
      }
      axios.post('http://127.0.0.1:5000/traininfo', this.id)
        .then(response => {
          console.log(response.data)
          this.formData = response.data
          return response
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    toPredict () {
      console.log('data =', this.formData)
      this.$router.push({name: 'startpredict',
        params: {model_name: this.formData.modelname,
          MLA: this.formData.MLA,
          ip: this.formData.partnerIP,
          port: this.formData.partnerPort,
          partnername: this.formData.partnername}})
    },
    resetForm () {
      this.$refs['elForm'].resetFields()
    },
    backToTable () {
      this.$router.push('/overall/task')
    },
  },
  watch: {
    '$route' () {
      if (['trainForm'].indexOf(this.$route.name) > -1) {
        this.reload()
      }
      if (this.$route.params.id !== this.formData.id) {
        this.reload()
      }
    }
  },
  created () {
    this.reload()
  }
}

</script>
<style>
</style>
