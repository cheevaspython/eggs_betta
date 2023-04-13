export const state = () => ({
  bid: {},
  activeTasks: []
})

export const mutations = {
  activeTasks(state, data) {
    state.activeTasks = data
  }
}

export const actions = {
  async getActiveTasks(context) {
    const token = localStorage.getItem('access_token')
    // TODO: set token to default axios settings
    try {
      const {data} = await this.$axios.get('/bid/activetask/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('activeTasks', data)
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
      }
    }
  }
}
