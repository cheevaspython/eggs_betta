export const state = () => ({
  user: null,
  notifications: []
})

export const mutations = {
  user(state, data) {
    state.user = data
  },
  notifications(state, data) {
    state.notifications = data
  }
}

export const actions = {
  async whoami(context) {
    try {
      // localStorage.removeItem('userId')
      // localStorage.removeItem('userRole')
      const token = localStorage.getItem('access_token')
      const user = await this.$axios.get('/users/whoami/', {headers: {Authorization: `Bearer ${token}`}})
        // .then(response => {
        //   console.log(response.data)
        //   localStorage.setItem('userId', response.data.user_id)
        //   localStorage.setItem('userRole', response.data.user_role)
        //   const fullName = response.data.user_first_name + ' ' + response.data.user_last_name
        //   localStorage.setItem('fullName', fullName)
        // })
      if (!user) return 
      localStorage.setItem('userId', user.data.user_id)
      localStorage.setItem('userRole', user.data.user_role)
      const fullName = user.data.user_first_name + ' ' + user.data.user_last_name
      localStorage.setItem('fullName', fullName)
      return
    } catch (e) {
      throw new Error(e)
    }
  },

  async masterPassword(context, password) {
    try {
      const token = localStorage.getItem('access_token')
      const access = await this.$axios.post('/users/whoami/', {entered_password: password}, {headers: {Authorization: `Bearer ${token}`}})
      if (!access) return 
      return access.data.entered_password
    } catch (e) {
      throw new Error(e)
    }
  },

  async getUserNotifications(context) {
    try {
      const token = localStorage.getItem('access_token')
      const {data} = await this.$axios.get('/eggs/request_user_message/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
      context.commit('notifications', data)
      return data
    } catch (e) {
      throw new Error(e)
    }
  },

  async readNotification(context, id) {
    try {
      const token = localStorage.getItem('access_token')
      const {data} = await this.$axios.patch(`/eggs/message_to_user/${id}/`, {not_read: false}, {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
    } catch (e) {
      throw new Error(e)
    }
  }
}