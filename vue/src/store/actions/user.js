import {
  SET_USERINFO,
  SET_TOKEN
} from '../mutation-types'
import Vue from 'vue'
import API from '../../api'
import qs from 'qs'

export const login = ({ commit }, form) => {
  // test for login
  // return new Promise((resolve, reject) => {
  //   if (form.account && form.password) {
  //     let session = 'test'
  //     commit(SET_TOKEN, session)
  //     return resolve(session)
  //   }
  //   reject()
  // })
  return Vue.http.post(API.USER_LOGIN, qs.stringify(form))
  // 'http://127.0.0.1:5000/login'
    .then(data => {
      console.log(data)
      commit(SET_TOKEN, data.session)
      return data
    })
}

export const logout = ({ commit }) => {
  commit(SET_TOKEN, '')
}
