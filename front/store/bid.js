export const state = () => ({
  appsFromBuyer: [],
  appsFromSeller: [],
  calculates: [],
  confCalculates: [],
  deals: [],
  ownerTasks: []
})

export const mutations = {
  ownerTasks(state, data) {
    state.ownerTasks = [].concat(
      data.current_user_deal_eggs,
      data.current_user_confirmed_calculate_eggs,
      data.current_user_calculate_eggs,
      data.current_user_application_from_buyer_eggs,
      data.current_user_application_from_seller_eggs,
    )
  },
  appsFromSeller(state, data) {
    state.appsFromSeller = data
  },
  appsFromBuyer(state, data) {
    state.appsFromBuyer = data
  },
  calculates(state, data) {
    state.calculates = data
  },
  confCalculates(state, data) {
    state.confCalculates = data
  },
  deals(state, data) {
    state.deals = data
  }
}

export const actions = {
  async getOwnerTasks(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/left_side_bar/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('ownerTasks', data)
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token') 
        localStorage.removeItem('username')
        localStorage.removeItem('userId')
        localStorage.removeItem('userRole')
      }
    }
  },

  async getAppsFromSeller(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/application_from_seller/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('appsFromSeller', data)
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token') 
        localStorage.removeItem('username')
        localStorage.removeItem('userId')
        localStorage.removeItem('userRole')
      }
    }
  },

  async getAppsFromBuyer(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/application_from_buyer/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('appsFromBuyer', data)
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token') 
        localStorage.removeItem('username')
        localStorage.removeItem('userId')
        localStorage.removeItem('userRole')
      }
    }
  },

  async getCalculates(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/base_deal/0/list_calculate/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('calculates', data)
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
    }
  },

  async getConfCalculates(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/base_deal/0/list_confirmed_calculate/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('confCalculates', data)
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
    }
  },

  async getDeals(context) {
    const token = localStorage.getItem('access_token')
    try {
      const {data} = await this.$axios.get('/eggs/base_deal/0/list_deal/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) throw new Error('No response')
      context.commit('deals', data)
      return
    } catch (e) {
      if (e.response?.status === 401) {
        await this.$router.push('/login')
        localStorage.clear()
      }
    }
  },
}
