export const state = () => ({
  user: null,
})

export const mutations = {
  user(state, data) {
    state.user = data
  }
}

export const actions = {

  async getUserInfo(context) {
    try {
      const token = localStorage.getItem('access_token')
      const {data} = await this.$axios.get('/users/usrdetail/', {headers: {Authorization: `Bearer ${token}`}})
      if (!data) return
      console.log('####### user ', data)
      context.commit('user', data)
      return data
    } catch (e) {
      throw new Error(e)
    }

  }
}
