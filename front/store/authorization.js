export const state = () => ({
  auth: {},
})

export const mutations = {
  auth(state, data) {
    state.auth = data
  }
}

export const actions = {
  async postAuth(context, {username, password}) {
    try {
      const {data} = await this.$axios.post('/token/', {username, password})
      if (!data) return
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      context.commit('auth', data)
      localStorage.setItem('username', username)
      const user = await this.$axios.get('/users/whoami/', {headers: {Authorization: `Bearer ${data.access}`}})
      if (!user) return 
      localStorage.setItem('userId', user.data.user_id)
      localStorage.setItem('userRole', user.data.user_role)
      const fullName = user.data.user_first_name + ' ' + user.data.user_last_name
      localStorage.setItem('fullName', fullName)
      // this.$axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
      // this.$axios.setHeader('Authorization', 'Bearer ' + data.access)
      await this.$router.push('/')
      return
    } catch (e) {
      if (e.response?.status === 401) {
        localStorage.clear()
        await this.$router.push('/login')
        return "Введен неправильный логин или пароль"
      }
      // throw new Error(e)
    }
  },

  async refreshToken() {
    const refresh = localStorage.getItem('refresh_token')
    try {
      const {data} = await this.$axios.post('/token/refresh/', {refresh: refresh})
      if (!data) return
      localStorage.removeItem('access_token')
      localStorage.setItem('access_token', data.access)
      return
    } catch (e) {
      this.$router.push('/login')
      throw new Error(e)
    }
  },

  async logOut(){
    localStorage.clear()
    await this.$router.push('/login')
  },
}

export const getters = {
  auth: state => state.auth
}
