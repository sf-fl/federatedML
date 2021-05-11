import {
  IS_DEV
} from './config'

const API = {
  // ROOT: IS_DEV ? '/api' : 'http://abc.com/api',
  // ROOT: '/api',

  USER_LOGIN: '/flp/login',

  TASK_LIST: '/flp/tasklist',
  APPLY_LIST: '/flp/applylist',
  TRAIN_FORM: '/flp/trainform',
  TRAIN_INFO: '/flp/traininfo',
  TRAIN_DETAIL: '/flp/traindetail',
  UPLOAD: '/flp/upload',
  ADD_TRAINTASK: '/flp/add_traintask',
  ADD_PREDICTTASK: '/flp/add_predicttask',
  APPEND_TRAINTASK: '/flp/append_traintask',
  APPEND_PREDICTTASK: '/flp/append_predicttask',
  USER_ADD: '/user/add',
  RECORD_LIST: '/user/getRecords',
  QUERY_LIST: '/user/getRecordsBy'
}

export default API
