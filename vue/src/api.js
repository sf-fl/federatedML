import {
  IS_DEV
} from './config'

const API = {
  // ROOT: IS_DEV ? '/api' : 'http://abc.com/api',
  // ROOT: '/api',

  USER_LOGIN: 'http://10.116.3.81:5000/login',

  TASK_LIST: 'http://127.0.0.1:5000/tasklist',
  APPLY_LIST: 'http://127.0.0.1:5000/applylist',
  TRAIN_FORM: 'http://127.0.0.1:5000/trainform',
  TRAIN_INFO: 'http://127.0.0.1:5000/traininfo',
  UPLOAD: 'http://127.0.0.1:5000/upload',
  ADD_TRAINTASK: 'http://127.0.0.1:5000/add_traintask',
  ADD_PREDICTTASK: 'http://127.0.0.1:5000/add_predicttask',
  APPEND_TRAINTASK: 'http://127.0.0.1:5000/append_traintask',
  APPEND_PREDICTTASK: 'http://127.0.0.1:5000/append_predicttask',
  USER_ADD: '/user/add',
  RECORD_LIST: '/user/getRecords',
  QUERY_LIST: '/user/getRecordsBy'
}

export default API
