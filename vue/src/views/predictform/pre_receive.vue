<template>
  <section class="user-edit">
    <n3-form
      ref="form"
      validate
    >
      <n3-form-item
        label="任务名"
        need
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          v-model="model.taskname"
          width="320px"
          :custom-validate="tasknameValidate"
        >
        </n3-input>
      </n3-form-item>
      <n3-form-item
        label="模型名"
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          v-model="model.modelname"
          width="320px"
          :custom-validate="modelnameValidate"
          readonly
        >
        </n3-input>
      </n3-form-item>
      <n3-form-item
        label="数据集"
        need
        :label-col="3"
      >
        <!--        <input type="file" @change="inputFileChange">-->
        <input class="file" name="file" type="file"  accept=".csv" @change="update"/>
        <div class="i-tips">
          文件目前只接受csv
        </div>
        <!--        <n3-button @click.native="clicks" type="primary" size="mini" >上传</n3-button>-->
      </n3-form-item>

      <n3-form-item
        label="对齐字段"
        need
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          :custom-validate="alianValidate"
          v-model="model.alian_feature"
          width="320px"
          class="fl"
        >
        </n3-input>
        <n3-select
          v-model="model.alian_feature"
          width="160px"
        >
          <n3-option value="">--敬请期待--</n3-option>
        </n3-select>
      </n3-form-item>
      <n3-form-item
        label="学习类型"
        :label-col="3"
      >
        <n3-select
          v-model="model.learningAlgorithm"
          width="160px"
          readonly
        >
          <n3-option value="VLR">纵向逻辑回归</n3-option>
          <n3-option value="VSB">纵向SecureBoost</n3-option>
          <n3-option value="0">--敬请期待--</n3-option>
        </n3-select>
      </n3-form-item>
      <n3-form-item
        label="目标IP"
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          :custom-validate="ipValidate"
          v-model="model.ip"
          width="320px"
          class="fl"
          readonly
        >
        </n3-input>
        <div class="i-tips">
          形如：0.0.0.0
        </div>
      </n3-form-item>
      <n3-form-item
        label="目标端口"
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          :custom-validate="portValidate"
          v-model="model.port"
          width="320px"
          class="fl"
          readonly
        >
        </n3-input>
        <div class="i-tips">
          形如：8080
        </div>
      </n3-form-item>
      <n3-form-item
        label="参与方名称"
        :label-col="3"
      >
        <n3-input
          :rules="[{type:'required'}]"
          :custom-validate="partnernameValidate"
          v-model="model.partnername"
          width="320px"
          class="fl"
          readonly
        >
        </n3-input>
        <div class="i-tips">
          形如：XXX公司
        </div>
      </n3-form-item>
      <n3-form-item
        :label-col="3"
      >
        <n3-button
          @click.native="submit"
          type="primary"
          :loading="loading"
          class="submit-btn"
        >
          {{ loading ? '操作中' : '保存' }}
        </n3-button>
      </n3-form-item>
      <!--      <div>-->
      <!--        <el-row>-->
      <!--          <el-form>-->
      <!--            <el-col :span="11">-->
      <!--              <el-form-item label="下拉选择" prop="feature">-->
      <!--                <el-select v-model="model.feature" placeholder="请选择下拉选择" filterable clearable-->
      <!--                           :style="{width: '100%'}">-->
      <!--                  <el-option v-for="(item, index) in featureOptions" :key="index" :label="item.label"-->
      <!--                             :value="item.value" :disabled="item.disabled"></el-option>-->
      <!--                </el-select>-->
      <!--              </el-form-item>-->
      <!--            </el-col>-->
      <!--          </el-form>-->
      <!--        </el-row>-->
      <!--      </div>-->
    </n3-form>

  </section>
</template>

<script>
import API from '../../api'
import qs from 'qs'
import { mapState } from 'vuex'
import axios from 'axios'
import { randomPassword, dateFormat } from '../../utils'
// import submitfile from "xxxxxx"

export default {
  computed: {
    ...mapState(['user'])
  },
  data () {
    return {
      model: {
        taskname: '',
        modelname: '',
        alian_feature: '',
        phone: '',
        ip: '',
        port: '',
        partnername: '',
        learningAlgorithm: '',
        cacheExpireTime: '24',
        feature: '',
        expireDate: dateFormat(Date.now(), 'YYYY-MM-DD')
      },
      featureOptions: [{
        "label": "选项一",
        "value": 1
      }, {
        "label": "选项二",
        "value": 2
      }, {
        "label": "",
        "value": ""
      }],
      loading: false,
      files: ''
    }
  },
  methods: {
    reload () {
      console.log(this.$route.params)
      console.log(this.$route.params.model_name)
      // 重置表单
      this.model = {
        taskname: '',
        modelname: this.$route.params.model_name || '',
        alian_feature: '',
        ip: this.$route.params.ip || '',
        port: this.$route.params.port || '',
        partnername: this.$route.params.partnername || '',
        feature: '',
        learningAlgorithm: this.$route.params.MLA || 'VLR',
        cacheExpireTime: '24',
        expireDate: dateFormat(Date.now(), 'YYYY-MM-DD')
      }
      axios.post('http://127.0.0.1:5000/trainform', this.id)
        .then(response => {
          console.log(response.data)
          this.model = response.data
          return response
        })
        .catch(function (error) {
          console.log(error)
        })
      this.loading = false
    },
    inputFileChange (e) {
      this.files = e.target.files[0]  // 当input中选择文件时触发一个事件并让data当中的files拿到所选择的文件
    },
    update (e) {
      this.file = e.target.files[0]
      this.param = new window.FormData() // 创建form对象
      this.param.append('file', this.file) // 通过append向form对象添加数据
      console.log(this.param.get('file')) // FormData私有类对象，访问不到，可以通过get判断值是否传进去
      axios.post('http://127.0.0.1:5000/upload', this.param, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}) // 请求头要为表单
        .then(response => {
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    clicks () {
      if (!this.files) {
        console.print('请选择文件')
      } else {
        //   return
        //   let fd = new FormData ()
        //   fd.append('file',
        //   this.files
        // )
        //   submitfile(fd).then(res => {
        //   })
      }
    },
    // Random Pass
    randomPasswd () {
      this.model.password = randomPassword(18)
    },
    addTask () {
      let cond = Object.assign({}, this.model)
      // cond.expireDate = new Date(cond.expireDate).valueOf()
      this.loading = true
      axios.post('http://127.0.0.1:5000/add_traintask', qs.stringify(cond))
        .then(data => {
          this.loading = false
          this.n3Alert({
            content: data + '\n添加成功~',
            type: 'success',
            placement: 'top-right',
            duration: 5000,
            width: '240px' // 内容不确定，建议设置width
          })
          this.$router.push('/overall/task')
        })
        // eslint-disable-next-line handle-callback-err
        .catch(error => {
          this.loading = false
          this.n3Alert({
            content: '添加失败，请检查表单重试或刷新~',
            type: 'danger',
            placement: 'top-right',
            duration: 5000,
            width: '240px' // 内容不确定，建议设置width
          })
        })
    },
    submit () {
      this.$refs.form.validateFields(result => {
        if (!result.isvalid) {
          return
        }
        return this.addTask()
      })
    },
    passwordValidate (val) {
      if (val && val.length > 5 && val.length < 19) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '密码长度为6-18位'
        }
      }
    },
    tvValidate (val) {
      if (/^0.\d{1,3}$/.test(val)) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '请输入正确的训练集占比'
        }
      }
    },
    alianValidate (val) {
      if (val) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '请输入正确的训练集占比'
        }
      }
    },
    ipValidate (val) {
      if (/^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$/.test(val)) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '请输入正确的IP地址'
        }
      }
    },
    portValidate (val) {
      if (/^\d{1,5}$/.test(val) && Number(val) > 0) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '请输入正确端口'
        }
      }
    },
    partnernameValidate (val) {
      if (val && val.length > 3 && val.length < 19) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '参与方名称长度为4-18位'
        }
      }
    },
    modelnameValidate (val) {
      if (val && val.length > 3 && val.length < 19) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '模型名长度为4-18位'
        }
      }
    },
    tasknameValidate (val) {
      if (val && val.length > 3 && val.length < 19) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '任务名长度为4-18位'
        }
      }
    },
    usernameValidate (val) {
      if (val && val.length > 5 && val.length < 19) {
        return {
          validStatus: 'success'
        }
      } else {
        return {
          validStatus: 'error',
          tips: '账户名长度为6-18位'
        }
      }
    }
  },
  watch: {
    '$route' () {
      if (this.$route.name === 'startpredict') {
        this.reload()
      }
      if (['trainForm'].indexOf(this.$route.name) > -1) {
        this.reload()
      }
    }
  },
  created () {
    this.reload()
  }
}
</script>

<style lang="less">
.user-edit {
  background: #fff;
  .submit-btn {
    width: 320px;
  }
  .refresh {
    cursor: pointer;
  }
  .i-tips {
    float: left;
    padding-left: 10px;
    color: #999;
  }
}
</style>
