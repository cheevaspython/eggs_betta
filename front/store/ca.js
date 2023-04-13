export const state = () => ({
  sellers: [],
  buyers: [],
  logists: [],
})

export const mutations = {
  setSellers(state, payload) {
    state.sellers = payload
  },
  setBuyers(state, payload) {
    state.buyers = payload
  },
}

export const actions = {
  setCurrentTask(context, payload){
    context.commit('currentTask', payload)
  },

  async getSellers(context) {
    const token = localStorage.getItem('access_token')
    // TODO: set token to default axios settings
    try {
      const {data} = await this.$axios.get('/ca/seller/eggs/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      context.commit('setSellers', data)
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
      }
    }
  },

  async getBuyers(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/ca/buyer/eggs/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return false
      context.commit('setBuyers', data)
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
      }
    }
  },
}
