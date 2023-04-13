export const state = () => ({
  auth: {},
})

export const mutations = {
  auth(state, data) {
    state.auth = data
  },
  user(state,data) {
    state.user = data
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
      this.$axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`

      this.$axios.setHeader('Authorization', 'Bearer ' + data.access)
      await this.$router.push('/')
      return data
    } catch (e) {
      throw new Error(e)
    }

  }
}
export const getters = {
  auth: state => state.auth
}
