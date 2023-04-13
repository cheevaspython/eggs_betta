export const state = () => ({
  calculateTasks: [],
  currentTask: {},
})

export const mutations = {
  calculateTasks(state, payload) {
    state.activeTasks = payload
    // state.currentTask = data
  },
  currentTask(state, payload){
    state.currentTask = payload
  }
}

export const actions = {
  setCurrentTask(context, payload){
    context.commit('currentTask', payload)
  },

  async getCalculateTasks(context) {
    const token = localStorage.getItem('access_token')
    // TODO: set token to default axios settings
    try {
      const {data} = await this.$axios.get('/eggs/calculate/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('calculateTasks', data)
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
      }
    }
  },

  async postSellerApp(context, payload) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.post('/eggs/sellerapp/', payload, {headers: {Authorization: `Bearer ${token}`}})
      console.log('####### postSellerApp ', data)
      if (!data) throw new Error('No response')
      return data
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
      }
    }
  }
}
